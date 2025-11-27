# pdf-flattening

Command-line utility that converts PDFs into image-only PDFs (one raster image per page).

## Purpose

Ensures no hidden sensitive data remains in anonymized documents. Information that appears hidden by overlays (dark rectangles) may still exist in the PDF structure. This tool "flattens" the PDF by rendering each page to a raster image, eliminating all text layers, annotations, and vector objects.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (includes `uvx`).

## Usage

Basic usage (output: `document.flat.pdf`):
```bash
uvx pdf-flattening document.pdf
```

Custom output path:
```bash
uvx pdf-flattening document.pdf output.pdf
```

Custom DPI (default: 300):
```bash
uvx pdf-flattening document.pdf --dpi 400
```

## Development

```bash
# Install dependencies
uv sync

# Run the tool
uv run pdf-flatten input.pdf

# Run with custom DPI
uv run pdf-flatten input.pdf --dpi 400
```

## License

MIT