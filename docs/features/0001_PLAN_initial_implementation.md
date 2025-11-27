# 0001: Initial Implementation - PDF Flattening Utility

## Description

Command-line utility that converts PDFs into image-only PDFs (one raster image per page). This ensures no hidden sensitive data (text layers, annotations, vector objects behind overlays) can remain in anonymized documents.

**Key guarantee:** resulting PDF contains only pixel data — no text, annotations, or vector layers.

## Dependencies

Add to `pyproject.toml`:
- `pypdfium2` — PDF rendering (Apache-2.0 / BSD-like, no AGPL)
- `Pillow` — image manipulation and PDF assembly (PIL license)

## Files to Create/Modify

### 1. `VERSION`
- Plain text file with version string (e.g., `0.1.0`)
- Single source of truth for package version

### 2. `src/pdf_flattening/__init__.py`
- Package marker
- Read and export `__version__` from VERSION file

### 3. `src/pdf_flattening/cli.py`
- Entry point function `main()`
- Argument parsing via `argparse`:
  - `input_pdf` (positional) — path to source PDF
  - `output_pdf` (optional positional) — path for result
    - **Default**: `{input_filename}.flat.pdf` in the same directory as input
    - Example: `document.pdf` → `document.flat.pdf`
  - `--dpi` (optional, default=300) — rendering resolution
- Output file handling:
  - If output file exists, overwrite it and print a warning message
- Call core conversion function
- Handle errors with user-friendly messages

### 4. `src/pdf_flattening/converter.py`
- Core function `flatten_pdf(input_path: str, output_path: str, dpi: int = 300) -> None`
- All PDF processing logic isolated here

### 5. `pyproject.toml`
- Dynamic version from VERSION file:
  ```toml
  [project]
  name = "pdf-flattening"
  dynamic = ["version"]

  [tool.setuptools.dynamic]
  version = { file = "VERSION" }

  [build-system]
  requires = ["setuptools>=61", "wheel"]
  build-backend = "setuptools.build_meta"
  ```
- Add dependencies: `pypdfium2`, `Pillow`
- Configure script entry point:
  ```toml
  [project.scripts]
  pdf-flatten = "pdf_flattening.cli:main"
  ```

### 6. `README.md`
- Project description and purpose
- Prerequisites section:
  - End-user must install `uv` (includes `uvx`): link to https://docs.astral.sh/uv/getting-started/installation/
- Installation section:
  - End-user: `uvx pdf-flattening input.pdf` (output defaults to `input.flat.pdf`)
  - Developer: `uv sync`, `uv run pdf-flatten ...`
- Usage examples:
  - Basic: `uvx pdf-flattening document.pdf` → `document.flat.pdf`
  - Custom output: `uvx pdf-flattening document.pdf custom_output.pdf`
  - With DPI: `uvx pdf-flattening document.pdf --dpi 400`
- License info

## Algorithm: `flatten_pdf()`

1. Open source PDF with `pypdfium2.PdfDocument(input_path)`
2. Calculate scale factor: `scale = dpi / 72.0` (PDF uses 72 DPI)
3. For each page in document:
   - Render page to bitmap: `page.render(scale=scale)`
   - Convert bitmap to PIL Image: `bitmap.to_pil()`
   - Convert to RGB if needed (PDF compatibility)
   - Append to images list
   - Close bitmap and page resources
4. Validate at least one page exists
5. Save all images as multi-page PDF via Pillow:
   ```
   first_image.save(output_path, format="PDF", save_all=True,
                    append_images=rest, resolution=dpi)
   ```

## Project Structure

```
pdf-flattening/
├── src/
│   └── pdf_flattening/
│       ├── __init__.py
│       ├── cli.py
│       └── converter.py
├── VERSION
├── pyproject.toml
├── README.md
└── ...
```

## Notes

- **uvx usage**: Yes, `uvx pdf-flattening` is the recommended way for end-users. uvx creates an isolated environment, installs the package, and runs it — similar to `npx` for Node.js.
- **Unit tests**: Deferred to future iteration. When added, use `pytest` with sample PDFs.
- **DPI recommendations**: 300 for standard documents, 400-600 for fine details.