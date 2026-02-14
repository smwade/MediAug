"""SIPaKMeD dataset downloading and setup.

Fixes all bugs from the original ``download.py``:
- Missing commas causing string concatenation (lines 24, 33)
- Broken extraction loop iterating chars of string (line 42)
- ``zipfile.ZipFile`` passed a list instead of path (line 44)
- ``dir`` builtin used as path variable (line 45)
"""

from __future__ import annotations

import logging
import urllib.request
from pathlib import Path

from tqdm import tqdm

logger = logging.getLogger(__name__)

# SIPaKMeD archive URLs — one 7z per cell type
_FILE_URLS: dict[str, str] = {
    "metaplastic": "http://cs.uoi.gr/~marina/SIPAKMED/im_Metaplastic.7z",
    "dyskeratotic": "http://cs.uoi.gr/~marina/SIPAKMED/im_Dyskeratotic.7z",
    "koilocytotic": "http://cs.uoi.gr/~marina/SIPAKMED/im_Koilocytotic.7z",
    "parabasal": "http://cs.uoi.gr/~marina/SIPAKMED/im_Parabasal.7z",
    "superficial-intermediate": "http://cs.uoi.gr/~marina/SIPAKMED/im_Superficial-Intermediate.7z",
}


def get_data_cache() -> Path:
    """Return the default data cache directory (``~/.mediaug``), creating it if needed."""
    p = Path.home() / ".mediaug"
    p.mkdir(exist_ok=True)
    return p


def download_sipakmed(data_dest: str | Path | None = None) -> Path:
    """Download the SIPaKMeD dataset.

    The dataset is hosted at http://cs.uoi.gr/~marina as 7z archives.
    Each archive contains cell images for one of five cell types.

    Args:
        data_dest: Directory to download into. Defaults to
            ``~/.mediaug/sipakmed_raw``.

    Returns:
        Path to the download directory.

    Raises:
        ValueError: If the destination already exists.

    Note:
        Extraction of 7z files requires the ``py7zr`` package.  If not
        installed, the archives are downloaded but not extracted, and a
        warning is logged.
    """
    dest = Path(data_dest) if data_dest is not None else get_data_cache() / "sipakmed_raw"

    if dest.exists():
        raise ValueError(f"Destination already exists: {dest}")

    dest.mkdir(parents=True, exist_ok=True)

    logger.info("Downloading SIPaKMeD to: %s", dest)

    for cell_type, url in tqdm(_FILE_URLS.items(), desc="Downloading"):
        file_name = f"{cell_type}.7z"
        file_path = dest / file_name
        logger.info("Downloading %s...", cell_type)
        urllib.request.urlretrieve(url, str(file_path))

    # Attempt extraction
    try:
        import py7zr
    except ImportError:
        logger.warning(
            "py7zr not installed — archives downloaded but not extracted. "
            "Install with: pip install py7zr"
        )
        return dest

    for archive in tqdm(sorted(dest.glob("*.7z")), desc="Extracting"):
        logger.info("Extracting %s...", archive.name)
        with py7zr.SevenZipFile(archive, mode="r") as z:
            z.extractall(path=dest)
        archive.unlink()  # Remove archive after extraction

    logger.info("Finished downloading SIPaKMeD.")
    return dest
