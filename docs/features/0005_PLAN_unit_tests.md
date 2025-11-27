# 0005: Unit Tests with pytest

## Description

Minimal unit tests for `converter.py` using pytest. Test PDFs generated dynamically using Pillow.

## Files Created/Modified

### 1. `pyproject.toml`

Added pytest as dev dependency:
```toml
[project.optional-dependencies]
dev = ["pytest"]
```

### 2. `tests/conftest.py`

Fixtures:
- `sample_pdf_with_image(width, height, dpi)` — creates test PDF with image
- `output_pdf_path` — temp path for output

### 3. `tests/test_converter.py`

**Tests for `flatten_pdf()`:**
- `test_creates_output_file` — basic smoke test
- `test_with_fixed_dpi` — explicit DPI parameter
- `test_with_auto_dpi` — dpi=None
- `test_output_is_valid_pdf` — output can be opened as PDF

**Tests for `detect_page_dpi()`:**
- `test_detects_dpi_from_pillow_pdf` — finds DPI from image
- `test_rounds_to_nearest_50` — 167 → 200
- `test_caps_at_max_dpi` — >600 → 600
- `test_floors_at_min_dpi` — <72 → 72

## Running Tests

```bash
uv sync --extra dev
uv run pytest -v
```
