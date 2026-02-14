"""Visualization functions for samples, augmentations, and dataset summaries.

Matplotlib is imported lazily so the ``[viz]`` extra is only required
when these functions are actually called.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from mediaug._types import CellSample
    from mediaug.datasets.base import CellDataset
    from mediaug.transforms.base import Transform


def _ensure_matplotlib() -> None:
    try:
        import matplotlib  # noqa: F401
    except ImportError:
        raise ImportError(
            "matplotlib is required for visualization. "
            "Install it with: pip install mediaug[viz]"
        ) from None


def plot_sample(sample: CellSample, figsize: tuple[int, int] = (12, 6)) -> None:
    """Display a sample's image and mask side by side.

    Args:
        sample: The cell sample to display.
        figsize: Figure size in inches.
    """
    _ensure_matplotlib()
    from matplotlib import pyplot as plt

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    ax1.imshow(sample.image)
    ax1.set_title(f"Image ({sample.cell_class})")
    ax1.axis("off")
    ax2.imshow(sample.mask)
    ax2.set_title("Mask")
    ax2.axis("off")
    plt.tight_layout()
    plt.show()


def plot_augmentation_grid(
    sample: CellSample,
    transform: Transform,
    n: int = 5,
    seed: int = 42,
    figsize: tuple[int, int] | None = None,
) -> None:
    """Show the original sample plus *n* augmented versions in a grid.

    Args:
        sample: The original cell sample.
        transform: The transform (or ``Compose``) to apply.
        n: Number of augmented versions to show.
        seed: Random seed for reproducibility.
        figsize: Figure size; auto-calculated if ``None``.
    """
    _ensure_matplotlib()
    from matplotlib import pyplot as plt

    cols = n + 1
    if figsize is None:
        figsize = (4 * cols, 4)

    rng = np.random.default_rng(seed)
    fig, axes = plt.subplots(1, cols, figsize=figsize)

    axes[0].imshow(sample.image)
    axes[0].set_title("Original")
    axes[0].axis("off")

    for i in range(n):
        aug = transform(sample, rng)
        axes[i + 1].imshow(aug.image)
        axes[i + 1].set_title(f"Aug {i + 1}")
        axes[i + 1].axis("off")

    plt.tight_layout()
    plt.show()


def plot_dataset_summary(
    dataset: CellDataset,
    samples_per_class: int = 3,
    seed: int = 42,
    figsize: tuple[int, int] | None = None,
) -> None:
    """Display class distribution and sample images from a dataset.

    Args:
        dataset: The dataset to summarize.
        samples_per_class: Number of example images per class.
        seed: Random seed for sample selection.
        figsize: Figure size; auto-calculated if ``None``.
    """
    _ensure_matplotlib()
    from matplotlib import pyplot as plt

    classes = dataset.classes
    n_classes = len(classes)
    rng = np.random.default_rng(seed)

    cols = samples_per_class + 1  # +1 for the bar
    if figsize is None:
        figsize = (4 * cols, 3 * n_classes)

    fig, axes = plt.subplots(n_classes, cols, figsize=figsize, squeeze=False)

    for row, cls in enumerate(classes):
        # Class count in first column
        samples = dataset[cls]
        axes[row][0].barh([0], [len(samples)], color="steelblue")
        axes[row][0].set_title(cls)
        axes[row][0].set_xlim(0, dataset.size)
        axes[row][0].set_yticks([])

        # Sample images
        indices = rng.choice(len(samples), size=min(samples_per_class, len(samples)), replace=False)
        for col, idx in enumerate(indices):
            axes[row][col + 1].imshow(samples[idx].image)
            axes[row][col + 1].axis("off")

        # Clear unused axes
        for col in range(len(indices) + 1, cols):
            axes[row][col].axis("off")

    plt.tight_layout()
    plt.show()
