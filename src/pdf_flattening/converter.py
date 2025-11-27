from pathlib import Path

import pypdfium2 as pdfium
from PIL import Image
from tqdm import tqdm


def flatten_pdf(
    input_path: str | Path,
    output_path: str | Path,
    dpi: int = 300,
    show_progress: bool = False,
) -> None:
    """
    Render each page of input PDF to a raster image and save as a new PDF.
    Resulting PDF contains exactly one raster image per page (no text/vectors).
    """
    pdf = pdfium.PdfDocument(input_path)
    images: list[Image.Image] = []
    scale = dpi / 72.0

    try:
        page_range = range(len(pdf))
        if show_progress:
            page_range = tqdm(page_range, desc="Processing", unit="page")

        for i in page_range:
            page = pdf[i]
            bitmap = page.render(scale=scale)
            pil_image = bitmap.to_pil()

            if pil_image.mode not in ("RGB", "L"):
                pil_image = pil_image.convert("RGB")

            images.append(pil_image)
            bitmap.close()
            page.close()

        if not images:
            raise ValueError("Input PDF has no pages")

        first, rest = images[0], images[1:]
        first.save(
            output_path,
            format="PDF",
            save_all=True,
            append_images=rest,
            resolution=dpi,
        )
    finally:
        pdf.close()