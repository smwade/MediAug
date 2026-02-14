"""MediAug — medical image augmentation for histology and cytology slides.

Provides cell-level augmentation (inserting cells with blending, histogram
matching, and mask propagation) alongside standard geometric and intensity
transforms, all with full reproducibility via seeded RNG.

Quick start::

    import mediaug
    import numpy as np

    ds = mediaug.CellDataset("path/to/cells")

    pipeline = mediaug.Compose([
        mediaug.Rotate(max_angle=30, p=0.5),
        mediaug.FlipHorizontal(p=0.5),
        mediaug.RandomBrightness(limit=0.2, p=0.3),
        mediaug.InsertCell(cell_source=ds, num_cells=(1, 5), p=0.8),
    ])

    rng = np.random.default_rng(42)
    sample = ds.random_sample(rng=rng)
    augmented = pipeline(sample, rng=rng)
"""

from __future__ import annotations

from mediaug._types import CellSample
from mediaug.datasets.base import CellDataset
from mediaug.datasets.sipakmed import download_sipakmed
from mediaug.io.masks import generate_cell_mask, generate_cell_mask_list
from mediaug.io.readers import read_dat, read_image
from mediaug.io.writers import save_image
from mediaug.transforms.base import Compose, OneOf, Transform
from mediaug.transforms.cell import InsertCell
from mediaug.transforms.geometric import (
    ElasticDistortion,
    FlipHorizontal,
    FlipVertical,
    RandomCrop,
    RandomScale,
    Resize,
    Rotate,
)
from mediaug.transforms.intensity import (
    GaussianNoise,
    HistogramMatching,
    RandomBrightness,
    RandomContrast,
    StainNormalization,
)

try:
    from importlib.metadata import version

    __version__ = version("mediaug")
except Exception:
    __version__ = "0.0.0.dev0"

__all__ = [
    "CellDataset",
    "CellSample",
    "Compose",
    "ElasticDistortion",
    "FlipHorizontal",
    "FlipVertical",
    "GaussianNoise",
    "HistogramMatching",
    "InsertCell",
    "OneOf",
    "RandomBrightness",
    "RandomContrast",
    "RandomCrop",
    "RandomScale",
    "Resize",
    "Rotate",
    "StainNormalization",
    "Transform",
    "download_sipakmed",
    "generate_cell_mask",
    "generate_cell_mask_list",
    "read_dat",
    "read_image",
    "save_image",
]
