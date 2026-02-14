"""Image writing utilities."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from numpy.typing import NDArray


def save_image(img: NDArray[np.uint8], path: str | Path, color_mode: str = "rgb") -> Path:
    """Save an image array to disk.

    Args:
        img: Image array (H, W, 3) in RGB order by default.
        path: Destination file path.
        color_mode: ``"rgb"`` (default) means the input is RGB and will be
            converted to BGR for OpenCV's ``imwrite``.  Pass ``"bgr"`` if the
            array is already in BGR order.

    Returns:
        The resolved ``Path`` where the image was written.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    if img.ndim == 3 and img.shape[2] == 3 and color_mode == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    cv2.imwrite(str(p), img)
    return p
