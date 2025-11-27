# 0002: Progress Indicator

## Description

Show progress during PDF processing. Currently large files cause a silent pause with no feedback.

## Approach

Use `tqdm` library for progress bar display.

## Dependencies

Add to `pyproject.toml`:
- `tqdm` — progress bar (MIT license)

## Files to Modify

### 1. `src/pdf_flattening/converter.py`

- Add `show_progress: bool = False` parameter to `flatten_pdf()`
- Wrap page loop with `tqdm` when enabled:
  ```python
  pages = tqdm(range(len(pdf)), desc="Processing", unit="page") if show_progress else range(len(pdf))
  ```

### 2. `src/pdf_flattening/cli.py`

- Pass `show_progress=True` to `flatten_pdf()` by default
- Add `--quiet` / `-q` flag to disable progress output

### 3. `pyproject.toml`

- Add `tqdm` to dependencies

## Result

```
$ pdf-flatten large_document.pdf
Processing: 100%|████████████████| 120/120 [00:45<00:00,  2.67page/s]
Created: large_document.flat.pdf
```