from importlib.metadata import version, PackageNotFoundError
from pathlib import Path


def _get_version() -> str:
    try:
        return version("pdf-flattening")
    except PackageNotFoundError:
        pass

    # Fallback for development: search VERSION in parent directories
    current = Path(__file__).parent
    for _ in range(5):
        version_file = current / "VERSION"
        if version_file.exists():
            return version_file.read_text().strip()
        current = current.parent

    return "0.0.0"


__version__ = _get_version()