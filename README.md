# pdf-flattening

Command-line utility that converts PDFs into image-only PDFs (one raster image per page).

## Purpose

Ensures no hidden sensitive data remains in anonymized documents. Information that appears hidden by overlays (dark rectangles) may still exist in the PDF structure. This tool "flattens" the PDF by rendering each page to a raster image, eliminating all text layers, annotations, and vector objects.

## Prerequisites

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) (includes `uvx`).

## Usage

### Single file

Basic usage (output: `document.flat.pdf`):
```bash
uvx pdf-flattening document.pdf
```

Custom output path:
```bash
uvx pdf-flattening document.pdf output.pdf
```

Force specific DPI (default: auto-detect from source images):
```bash
uvx pdf-flattening document.pdf --dpi 300
```

Adjust JPEG quality (default: 85):
```bash
uvx pdf-flattening document.pdf --quality 90
```

### Batch mode (directory)

Process all PDFs in a directory recursively (output next to originals):
```bash
uvx pdf-flattening documents/
```

Process to a separate output directory (preserves folder structure):
```bash
uvx pdf-flattening documents/ output/
```

### Options

| Option | Description |
|--------|-------------|
| `-d, --dpi N` | Rendering DPI (default: auto-detect from source images) |
| `-q, --quality N` | JPEG quality 1-100 (default: 85) |
| `-u, --quiet` | Suppress progress output |
| `-f, --force` | Force overwrite when input and output directories are the same |
| `-v, --version` | Show version |

By default, the tool analyzes embedded images in the source PDF and renders each page at optimal resolution to avoid unnecessary file size increase. Use `--dpi 300` to force a fixed resolution.

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

[Apache License 2.0](LICENSE)