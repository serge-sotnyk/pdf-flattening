import argparse
import sys
from pathlib import Path

from tqdm import tqdm

from pdf_flattening import __version__
from pdf_flattening.converter import flatten_pdf


def get_default_output_path(input_path: Path) -> Path:
    return input_path.with_suffix(".flat.pdf")


def find_pdfs(directory: Path) -> list[Path]:
    return sorted(directory.rglob("*.pdf"))


def is_same_directory(path1: Path, path2: Path) -> bool:
    return path1.resolve() == path2.resolve()


def get_batch_output_path(
    input_file: Path,
    input_root: Path,
    output_root: Path | None,
) -> Path:
    if output_root is None:
        return input_file.with_suffix(".flat.pdf")

    relative = input_file.relative_to(input_root)
    return output_root / relative.with_suffix(".flat.pdf")


def process_single_file(
    input_path: Path,
    output_path: Path,
    dpi: int,
    show_progress: bool,
) -> None:
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    if output_path.exists():
        print(f"Warning: Output file exists and will be overwritten: {output_path}", file=sys.stderr)

    try:
        flatten_pdf(input_path, output_path, dpi=dpi, show_progress=show_progress)
        print(f"Created: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def process_batch(
    input_dir: Path,
    output_dir: Path | None,
    dpi: int,
    show_progress: bool,
    force: bool,
) -> None:
    if output_dir is not None and is_same_directory(input_dir, output_dir):
        if not force:
            print(
                "Error: Input and output directories are the same.\n"
                "This will overwrite original files. Use --force to proceed.",
                file=sys.stderr,
            )
            sys.exit(1)

    pdf_files = find_pdfs(input_dir)

    if not pdf_files:
        print(f"Error: No PDF files found in {input_dir}", file=sys.stderr)
        sys.exit(1)

    errors: list[tuple[Path, str]] = []
    processed = 0

    files_iter = tqdm(pdf_files, desc="Files", unit="file") if show_progress else pdf_files

    for pdf_file in files_iter:
        output_path = get_batch_output_path(pdf_file, input_dir, output_dir)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            flatten_pdf(pdf_file, output_path, dpi=dpi, show_progress=show_progress)
            processed += 1
            if not show_progress:
                print(f"Created: {output_path}")
        except Exception as e:
            errors.append((pdf_file, str(e)))
            if not show_progress:
                print(f"Error processing {pdf_file}: {e}", file=sys.stderr)

    print(f"\nProcessed {processed} files, {len(errors)} errors")

    if errors:
        print("\nFailed files:", file=sys.stderr)
        for path, error in errors:
            print(f"  {path}: {error}", file=sys.stderr)
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDF to image-only PDF (one raster image per page)."
    )
    parser.add_argument(
        "input_path",
        help="Path to input PDF file or directory",
    )
    parser.add_argument(
        "output_path",
        nargs="?",
        default=None,
        help="Path to output PDF or directory (default: <input>.flat.pdf)",
    )
    parser.add_argument(
        "-d", "--dpi",
        type=int,
        default=300,
        help="Rendering DPI (default: 300)",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress progress output",
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Force overwrite when input and output directories are the same",
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    input_path = Path(args.input_path)
    if not input_path.exists():
        print(f"Error: Input path not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    show_progress = not args.quiet

    if input_path.is_dir():
        output_dir = Path(args.output_path) if args.output_path else None
        process_batch(input_path, output_dir, args.dpi, show_progress, args.force)
    else:
        output_path = Path(args.output_path) if args.output_path else get_default_output_path(input_path)
        process_single_file(input_path, output_path, args.dpi, show_progress)


if __name__ == "__main__":
    main()