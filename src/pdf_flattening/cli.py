import argparse
import sys
from pathlib import Path

from pdf_flattening import __version__
from pdf_flattening.converter import flatten_pdf


def get_default_output_path(input_path: Path) -> Path:
    return input_path.with_suffix(".flat.pdf")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PDF to image-only PDF (one raster image per page)."
    )
    parser.add_argument("input_pdf", help="Path to input PDF")
    parser.add_argument(
        "output_pdf",
        nargs="?",
        default=None,
        help="Path to output PDF (default: <input>.flat.pdf)",
    )
    parser.add_argument(
        "--dpi",
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
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    args = parser.parse_args()

    input_path = Path(args.input_pdf)
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    output_path = Path(args.output_pdf) if args.output_pdf else get_default_output_path(input_path)

    if output_path.exists():
        print(f"Warning: Output file exists and will be overwritten: {output_path}", file=sys.stderr)

    try:
        flatten_pdf(input_path, output_path, dpi=args.dpi, show_progress=not args.quiet)
        print(f"Created: {output_path}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()