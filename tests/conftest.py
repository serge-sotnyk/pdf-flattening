import pytest
from PIL import Image


@pytest.fixture
def sample_pdf_with_image(tmp_path):
    """Factory fixture to create test PDFs with images at specified DPI."""

    def _create(width: int = 100, height: int = 100, dpi: int = 150):
        img = Image.new("RGB", (width, height), color="red")
        pdf_path = tmp_path / f"test_{dpi}dpi.pdf"
        img.save(pdf_path, format="PDF", resolution=dpi)
        return pdf_path

    return _create


@pytest.fixture
def output_pdf_path(tmp_path):
    """Temporary path for output PDF."""
    return tmp_path / "output.pdf"
