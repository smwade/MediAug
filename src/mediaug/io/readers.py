"""Unified image and data file reading.

Replaces the three identical ``read_bmp``, ``read_png``, ``read_img`` functions
from ``image_utils.py`` with a single ``read_image`` that handles BGR→RGB
conversion and validates that the file exists.
"""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray


def read_image(path: str | Path, color_mode: str = "rgb") -> NDArray[np.uint8]:
    """Read an image file and return a numpy array.

    Args:
        path: Path to the image file.
        color_mode: ``"rgb"`` (default) or ``"bgr"``. OpenCV loads as BGR;
            this function converts to RGB by default for consistency with
            PIL, matplotlib, and the rest of MediAug.

    Returns:
        Image array with shape (H, W, 3) for color or (H, W) for grayscale.

    Raises:
        FileNotFoundError: If *path* does not exist.
        ValueError: If the file cannot be decoded as an image.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Image not found: {p}")

    img = cv2.imread(str(p), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"Could not decode image: {p}")

    # Convert BGR → RGB for 3-channel images
    if img.ndim == 3 and img.shape[2] == 3 and color_mode == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    elif img.ndim == 3 and img.shape[2] == 4 and color_mode == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

    return img


def read_dat(path: str | Path) -> NDArray[np.float64]:
    """Read a ``.dat`` polygon file (comma-separated x,y coordinates).

    Args:
        path: Path to the ``.dat`` file.

    Returns:
        An (N, 2) array of polygon vertices.

    Raises:
        FileNotFoundError: If *path* does not exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"DAT file not found: {p}")
    return np.loadtxt(str(p), delimiter=",")
