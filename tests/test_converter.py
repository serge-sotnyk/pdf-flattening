import pypdfium2 as pdfium

from pdf_flattening.converter import (
    MAX_DPI,
    MIN_DPI,
    detect_page_dpi,
    flatten_pdf,
)


# flatten_pdf tests

def test_flatten_creates_output_file(sample_pdf_with_image, output_pdf_path):
    input_pdf = sample_pdf_with_image(dpi=150)
    flatten_pdf(input_pdf, output_pdf_path, dpi=100)
    assert output_pdf_path.exists()


def test_flatten_with_fixed_dpi(sample_pdf_with_image, output_pdf_path):
    input_pdf = sample_pdf_with_image(dpi=150)
    flatten_pdf(input_pdf, output_pdf_path, dpi=200)
    assert output_pdf_path.exists()
    assert output_pdf_path.stat().st_size > 0


def test_flatten_with_auto_dpi(sample_pdf_with_image, output_pdf_path):
    input_pdf = sample_pdf_with_image(dpi=150)
    flatten_pdf(input_pdf, output_pdf_path, dpi=None)
    assert output_pdf_path.exists()


def test_flatten_output_is_valid_pdf(sample_pdf_with_image, output_pdf_path):
    input_pdf = sample_pdf_with_image(dpi=150)
    flatten_pdf(input_pdf, output_pdf_path, dpi=100)

    pdf = pdfium.PdfDocument(output_pdf_path)
    assert len(pdf) == 1
    pdf.close()


# detect_page_dpi tests

def test_detect_dpi_from_pillow_pdf(sample_pdf_with_image):
    input_pdf = sample_pdf_with_image(dpi=150)
    pdf = pdfium.PdfDocument(input_pdf)
    page = pdf[0]
    dpi = detect_page_dpi(page)
    page.close()
    pdf.close()

    assert dpi > 0
    assert dpi <= MAX_DPI


def test_detect_dpi_rounds_to_nearest_50(sample_pdf_with_image):
    input_pdf = sample_pdf_with_image(dpi=167)
    pdf = pdfium.PdfDocument(input_pdf)
    page = pdf[0]
    dpi = detect_page_dpi(page)
    page.close()
    pdf.close()

    assert dpi % 50 == 0


def test_detect_dpi_caps_at_max(sample_pdf_with_image):
    input_pdf = sample_pdf_with_image(width=1000, height=1000, dpi=800)
    pdf = pdfium.PdfDocument(input_pdf)
    page = pdf[0]
    dpi = detect_page_dpi(page)
    page.close()
    pdf.close()

    assert dpi <= MAX_DPI


def test_detect_dpi_floors_at_min(sample_pdf_with_image):
    input_pdf = sample_pdf_with_image(width=10, height=10, dpi=50)
    pdf = pdfium.PdfDocument(input_pdf)
    page = pdf[0]
    dpi = detect_page_dpi(page)
    page.close()
    pdf.close()

    assert dpi >= MIN_DPI
