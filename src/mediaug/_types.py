"""Core data types for MediAug."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np
from numpy.typing import NDArray


@dataclass
class CellSample:
    """A single cell image with its corresponding mask.

    Attributes:
        image: H x W x 3 RGB uint8 image array.
        mask: H x W x 3 RGB uint8 mask array. Cytoplasm and nucleus regions
            are encoded with distinct grayscale values.
        cell_class: The cell type classification label.
        id: Optional identifier for this sample.
        metadata: Arbitrary key-value metadata.
    """

    image: NDArray[np.uint8]
    mask: NDArray[np.uint8]
    cell_class: str
    id: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def height(self) -> int:
        return int(self.image.shape[0])

    @property
    def width(self) -> int:
        return int(self.image.shape[1])
