"""CellDataset — manages collections of cell image/mask pairs organized by class.

Replaces the original ``Dataset`` class from ``dataset.py`` with:
- ``pathlib.Path`` throughout
- LRU-cached image loading (no re-reads from disk on every access)
- Both integer and string indexing
- Proper error handling and logging
"""

from __future__ import annotations

import logging
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path
from typing import overload

import numpy as np

from mediaug._types import CellSample
from mediaug.io.readers import read_image
from mediaug.io.writers import save_image

logger = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def _cached_read(path: str) -> np.ndarray:
    """Read an image with LRU caching to avoid re-reading from disk."""
    return read_image(path)


class CellDataset:
    """A dataset of cell images and masks organized by cell class.

    Expected directory layout::

        data_path/
        ├── class_a/
        │   ├── image/
        │   │   ├── 001.png
        │   │   └── ...
        │   └── mask/
        │       ├── 001.png
        │       └── ...
        └── class_b/
            ├── image/
            └── mask/

    Args:
        data_path: Root directory containing class subdirectories.
        classes: If given and *data_path* does not exist, create an empty
            dataset skeleton with these class directories.

    Raises:
        ValueError: If *data_path* does not exist and *classes* is ``None``.
    """

    def __init__(
        self,
        data_path: str | Path,
        classes: list[str] | None = None,
    ) -> None:
        self.data_path = Path(data_path)

        if not self.data_path.exists() and classes is not None:
            self._create_empty_dataset(classes)
        elif not self.data_path.exists():
            raise ValueError(f"Path does not exist and no classes given: {self.data_path}")

        self._data: dict[str, list[_CellRef]] = {}
        self._parse()

    def _parse(self) -> None:
        """Scan the directory tree and index all image/mask pairs."""
        self._data = {}
        for entry in sorted(self.data_path.iterdir()):
            if not entry.is_dir() or entry.name.startswith("."):
                continue
            class_name = entry.name
            image_dir = entry / "image"
            mask_dir = entry / "mask"
            if not image_dir.is_dir():
                logger.warning("Missing image/ directory for class '%s', skipping", class_name)
                continue
            refs: list[_CellRef] = []
            for img_file in sorted(image_dir.iterdir()):
                if img_file.name.startswith("."):
                    continue
                mask_file = mask_dir / img_file.name
                refs.append(
                    _CellRef(
                        img_path=img_file,
                        mask_path=mask_file if mask_file.exists() else None,
                        cell_class=class_name,
                        id=img_file.stem,
                    )
                )
            self._data[class_name] = refs
            logger.debug("Found %d samples for class '%s'", len(refs), class_name)

    def _create_empty_dataset(self, classes: list[str]) -> None:
        """Create the directory skeleton for an empty dataset."""
        for cls in classes:
            (self.data_path / cls / "image").mkdir(parents=True, exist_ok=True)
            (self.data_path / cls / "mask").mkdir(parents=True, exist_ok=True)

    # --- Properties ---

    @property
    def classes(self) -> list[str]:
        """List of class names in the dataset."""
        return list(self._data.keys())

    @property
    def size(self) -> int:
        """Total number of samples across all classes."""
        return sum(len(v) for v in self._data.values())

    # --- Iteration and indexing ---

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Iterator[CellSample]:
        for cls in self._data:
            for ref in self._data[cls]:
                yield ref.load()

    @overload
    def __getitem__(self, key: str) -> list[CellSample]: ...

    @overload
    def __getitem__(self, key: int) -> CellSample: ...

    def __getitem__(self, key: str | int) -> list[CellSample] | CellSample:
        """Index by class name (returns list) or integer index (returns single sample)."""
        if isinstance(key, str):
            if key not in self._data:
                raise KeyError(f"Unknown class: {key!r}. Available: {self.classes}")
            return [ref.load() for ref in self._data[key]]
        if isinstance(key, int):
            if key < 0:
                key = self.size + key
            offset = 0
            for cls in self._data:
                refs = self._data[cls]
                if key < offset + len(refs):
                    return refs[key - offset].load()
                offset += len(refs)
            raise IndexError(f"Index {key} out of range for dataset of size {self.size}")
        raise TypeError(f"Key must be str or int, got {type(key)}")

    def random_sample(self, rng: np.random.Generator | None = None) -> CellSample:
        """Return a random sample from the dataset.

        Args:
            rng: NumPy random generator for reproducibility. If ``None``,
                a default generator is used.
        """
        if rng is None:
            rng = np.random.default_rng()
        cls = self.classes[rng.integers(len(self.classes))]
        refs = self._data[cls]
        return refs[rng.integers(len(refs))].load()

    # --- Mutation ---

    def add_data(
        self,
        img: np.ndarray,
        mask: np.ndarray,
        cell_class: str,
        name: str,
    ) -> None:
        """Save an image/mask pair to disk and register it in the dataset."""
        img_path = self.data_path / cell_class / "image" / f"{name}.png"
        mask_path = self.data_path / cell_class / "mask" / f"{name}.png"
        save_image(img, img_path)
        save_image(mask, mask_path)
        if cell_class not in self._data:
            self._data[cell_class] = []
        self._data[cell_class].append(
            _CellRef(
                img_path=img_path,
                mask_path=mask_path,
                cell_class=cell_class,
                id=name,
            )
        )

    def __repr__(self) -> str:
        class_info = ", ".join(f"{k}: {len(v)}" for k, v in self._data.items())
        return f"CellDataset(path={self.data_path!r}, size={self.size}, classes={{{class_info}}})"


class _CellRef:
    """Lightweight reference to a cell on disk — loaded on demand with caching."""

    __slots__ = ("img_path", "mask_path", "cell_class", "id")

    def __init__(
        self,
        img_path: Path,
        mask_path: Path | None,
        cell_class: str,
        id: str,
    ) -> None:
        self.img_path = img_path
        self.mask_path = mask_path
        self.cell_class = cell_class
        self.id = id

    def load(self) -> CellSample:
        img = _cached_read(str(self.img_path))
        if self.mask_path is not None and self.mask_path.exists():
            mask = _cached_read(str(self.mask_path))
        else:
            mask = np.zeros_like(img)
        return CellSample(
            image=img,
            mask=mask,
            cell_class=self.cell_class,
            id=self.id,
        )
