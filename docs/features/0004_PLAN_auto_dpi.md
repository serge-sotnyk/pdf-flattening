# 0004: Auto-DPI Detection and JPEG Quality Control

## Description

Optimize output PDF file sizes by:
1. Auto-detecting optimal DPI per page based on embedded image resolutions
2. Adding JPEG quality control parameter

## Behavior

- **Auto-DPI enabled by default** — analyzes each page's images and renders at optimal resolution
- `--dpi N` overrides auto-detection with fixed value (backward compatible)
- `--quality N` controls JPEG compression (default: 85)

## Files Modified

### 1. `src/pdf_flattening/converter.py`

- Added `detect_page_dpi(page) -> int` function
- Modified `flatten_pdf()` signature: `dpi: int | None = None`, `quality: int = 85`
- Per-page DPI detection when `dpi` is None
- JPEG quality control via `encoderinfo`

### 2. `src/pdf_flattening/cli.py`

- `--dpi` default changed to None (auto-detect)
- Added `--quality` parameter (default: 85)
- Quality validation (1-100)

### 3. `README.md`

- Updated options documentation
- Added note about auto-DPI behavior

## Algorithm: Per-Page Rendering with Auto-DPI

```
1. Open PDF
2. For each page:
   a. If dpi parameter is None:
      - Scan page for image objects via get_objects()
      - Extract DPI from metadata or calculate from bounds
      - Use max DPI (rounded to 50, capped at 600)
   b. Else: use provided dpi
   c. Render page at determined DPI
   d. Set quality in image encoderinfo
   e. Append to images list
3. Save all images as PDF with quality settings
```

## Edge Cases

- **No images on page** (pure text/vectors): Use 300 DPI default
- **Very high DPI images** (>600): Cap at 600 to prevent huge files
- **Very low DPI images** (<72): Floor at 72
- **Mixed DPI on single page**: Use maximum to preserve quality
- **Metadata unavailable**: Fallback to bounds calculation
- **Both fail**: Use 300 DPI default
