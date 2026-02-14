"""Cell mask generation from polygon annotations."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray
from PIL import Image, ImageDraw

from mediaug._constants import COLOR_CYTO_MASK, COLOR_NUC_MASK


def _polygon_to_flat_list(arr: NDArray[np.float64]) -> list[float]:
    """Convert an (N, 2) coordinate array to a flat [x1,y1,x2,y2,...] list."""
    return arr.flatten().tolist()


def generate_cell_mask(
    img: NDArray[np.uint8],
    cytoplasm_polygon: NDArray[np.float64],
    nucleus_polygon: NDArray[np.float64],
) -> NDArray[np.uint8]:
    """Generate a cell mask from cytoplasm and nucleus polygon annotations.

    Args:
        img: The source image (used only for dimensions).
        cytoplasm_polygon: (N, 2) array of cytoplasm boundary vertices.
        nucleus_polygon: (N, 2) array of nucleus boundary vertices.

    Returns:
        An RGB mask array where cytoplasm and nucleus regions are filled
        with distinct colors defined in ``_constants.py``.
    """
    h, w = img.shape[:2]
    mask = Image.new(mode="RGB", size=(w, h))
    draw = ImageDraw.Draw(mask)
    draw.polygon(_polygon_to_flat_list(cytoplasm_polygon), fill=COLOR_CYTO_MASK)
    draw.polygon(_polygon_to_flat_list(nucleus_polygon), fill=COLOR_NUC_MASK)
    return np.array(mask)


def generate_cell_mask_list(
    img: NDArray[np.uint8],
    cytoplasm_polygons: list[NDArray[np.float64]],
    nucleus_polygons: list[NDArray[np.float64]],
) -> NDArray[np.uint8]:
    """Generate a mask for multiple cells on a slide.

    Args:
        img: The source image (used only for dimensions).
        cytoplasm_polygons: List of (N, 2) arrays for cytoplasm boundaries.
        nucleus_polygons: List of (N, 2) arrays for nucleus boundaries.

    Returns:
        An RGB mask array with all cells drawn.
    """
    h, w = img.shape[:2]
    mask = Image.new(mode="RGB", size=(w, h))
    draw = ImageDraw.Draw(mask)
    for poly in cytoplasm_polygons:
        draw.polygon(_polygon_to_flat_list(poly), fill=COLOR_CYTO_MASK)
    for poly in nucleus_polygons:
        draw.polygon(_polygon_to_flat_list(poly), fill=COLOR_NUC_MASK)
    return np.array(mask)
