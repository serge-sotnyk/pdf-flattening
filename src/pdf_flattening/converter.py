from pathlib import Path

import pypdfium2 as pdfium
import pypdfium2.raw as pdfium_c
from PIL import Image
from tqdm import tqdm

DEFAULT_DPI = 300
MIN_DPI = 72
MAX_DPI = 600


def detect_page_dpi(page) -> int:
    """Detect optimal DPI for a page based on embedded images."""
    dpi_values: list[float] = []

    for obj in page.get_objects(filter=[pdfium_c.FPDF_PAGEOBJ_IMAGE]):
        try:
            metadata = obj.get_metadata()
            if metadata.horizontal_dpi > 0:
                dpi_values.append(metadata.horizontal_dpi)
            if metadata.vertical_dpi > 0:
                dpi_values.append(metadata.vertical_dpi)
        except Exception:
            pass

        if not dpi_values:
            # Fallback: calculate from pixel size and bounds
            try:
                px_w, px_h = obj.get_px_size()
                l, b, r, t = obj.get_bounds()
                if r - l > 0:
                    dpi_values.append(px_w * 72 / (r - l))
                if t - b > 0:
                    dpi_values.append(px_h * 72 / (t - b))
            except Exception:
                pass

    if not dpi_values:
        return DEFAULT_DPI

    max_dpi = max(dpi_values)
    rounded = int((max_dpi + 49) // 50) * 50
    return min(max(rounded, MIN_DPI), MAX_DPI)


def flatten_pdf(
    input_path: str | Path,
    output_path: str | Path,
    dpi: int | None = None,
    quality: int = 85,
    show_progress: bool = False,
) -> None:
    """
    Render each page of input PDF to a raster image and save as a new PDF.
    Resulting PDF contains exactly one raster image per page (no text/vectors).

    Args:
        input_path: Source PDF file
        output_path: Output PDF file
        dpi: Rendering DPI. None = auto-detect per page from embedded images
        quality: JPEG quality 1-100 (default: 85)
        show_progress: Show progress bar
    """
    pdf = pdfium.PdfDocument(input_path)
    images: list[Image.Image] = []
    max_used_dpi = 0

    try:
        page_range = range(len(pdf))
        if show_progress:
            page_range = tqdm(page_range, desc="Processing", unit="page")

        for i in page_range:
            page = pdf[i]

            if dpi is None:
                page_dpi = detect_page_dpi(page)
            else:
                page_dpi = dpi

            max_used_dpi = max(max_used_dpi, page_dpi)
            scale = page_dpi / 72.0

            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()

            if pil_image.mode not in ("RGB", "L"):
                pil_image = pil_image.convert("RGB")

            images.append(pil_image)
            bitmap.close()
            page.close()

        if not images:
            raise ValueError("Input PDF has no pages")

        # Set JPEG quality for all images
        for img in images:
            img.encoderinfo = {"quality": quality}

        first, rest = images[0], images[1:]
        first.save(
            output_path,
            format="PDF",
            save_all=True,
            append_images=rest,
            resolution=max_used_dpi or DEFAULT_DPI,
        )
    finally:
        pdf.close()
