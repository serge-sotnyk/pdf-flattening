# 0003: Batch Mode

## Description

Process multiple PDFs when input path is a directory. Recursively find all PDFs and flatten them with two-level progress indication.

## Usage Scenarios

```bash
# Process folder, output next to originals
pdf-flatten documents/

# Process folder, output to separate directory (preserve structure)
pdf-flatten documents/ output/
```

**Structure preservation example:**
```
Input:                          Output (with output dir):
documents/                      output/
├── report.pdf                  ├── report.flat.pdf
├── 2024/                       ├── 2024/
│   ├── q1.pdf                  │   ├── q1.flat.pdf
│   └── q2.pdf                  │   └── q2.flat.pdf
```

## Files to Modify

### 1. `src/pdf_flattening/cli.py`

**Changes to argument handling:**
- Rename `input_pdf` → `input_path` (can be file or directory)
- Rename `output_pdf` → `output_path` (can be file or directory)
- Update help text to reflect both modes

**Add batch processing logic:**
- Detect if input is directory → batch mode
- `find_pdfs(directory: Path) -> list[Path]` — recursive glob `**/*.pdf`
- `get_output_path_batch(input_file: Path, input_root: Path, output_root: Path | None) -> Path`
  - If `output_root` is None → `input_file.with_suffix(".flat.pdf")`
  - If `output_root` exists → preserve relative structure

**Same directory safety check:**
- `is_same_directory(path1: Path, path2: Path) -> bool` — compare resolved absolute paths
- If input dir == output dir in batch mode → error and abort
- Add `--force` flag to override and allow overwriting originals

**Two-level progress:**
- Outer: files progress (tqdm, desc="Files", unit="file")
- Inner: pages progress (existing, from converter)

### 2. `src/pdf_flattening/converter.py`

- No changes needed — `flatten_pdf()` already handles single file with progress

### 3. `README.md`

- Add batch mode usage examples
- Document `--force` flag

## Algorithm: Batch Processing

```
1. If input_path is file:
   → existing single-file logic

2. If input_path is directory:
   a. Safety check: if output_path given and resolves to same dir as input_path:
      - If --force not set → error: "Input and output directories are the same.
        This will overwrite original files. Use --force to proceed."
   b. Find all PDFs: input_path.rglob("*.pdf")
   c. If no PDFs found → error and exit
   d. For each PDF (with outer tqdm):
      - Calculate output path (preserve structure if output_root given)
      - Create parent directories if needed
      - Call flatten_pdf() with inner progress
      - Print result or collect errors
   e. Print summary: "Processed X files, Y errors"
```

## Progress Display

```
Files: 40%|████      | 4/10 [00:30<00:45]
Processing: 100%|██████████| 25/25 [00:05<00:00, 5.00page/s]
Created: output/2024/report.flat.pdf
```

## Error Handling

- Continue processing other files if one fails
- Collect errors and print summary at the end
- Exit code: 0 if all succeeded, 1 if any failed