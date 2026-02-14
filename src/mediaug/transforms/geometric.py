"""Spatial / geometric transforms that modify both image and mask."""

from __future__ import annotations

import cv2
import numpy as np
from numpy.typing import NDArray

from mediaug._types import CellSample
from mediaug.transforms.base import Transform


def _rotate_array(image: NDArray[np.uint8], angle: float) -> NDArray[np.uint8]:
    """Rotate an image by *angle* degrees, expanding the canvas as needed."""
    h, w = image.shape[:2]
    cx, cy = w // 2, h // 2
    M = cv2.getRotationMatrix2D((cx, cy), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
    nw = int(h * sin + w * cos)
    nh = int(h * cos + w * sin)
    M[0, 2] += nw / 2 - cx
    M[1, 2] += nh / 2 - cy
    return cv2.warpAffine(image, M, (nw, nh))


class Rotate(Transform):
    """Rotate the image and mask by a random angle in [-max_angle, max_angle]."""

    def __init__(self, max_angle: float = 25.0, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.max_angle = max_angle

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        angle = rng.uniform(-self.max_angle, self.max_angle)
        return CellSample(
            image=_rotate_array(sample.image, angle),
            mask=_rotate_array(sample.mask, angle),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class FlipHorizontal(Transform):
    """Flip the image and mask left-right."""

    def __init__(self, p: float = 0.5) -> None:
        super().__init__(p=p)

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        return CellSample(
            image=np.fliplr(sample.image).copy(),
            mask=np.fliplr(sample.mask).copy(),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class FlipVertical(Transform):
    """Flip the image and mask top-bottom."""

    def __init__(self, p: float = 0.5) -> None:
        super().__init__(p=p)

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        return CellSample(
            image=np.flipud(sample.image).copy(),
            mask=np.flipud(sample.mask).copy(),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class RandomCrop(Transform):
    """Randomly crop a region with area between *min_area* and *max_area* of the original."""

    def __init__(self, min_area: float = 0.5, max_area: float = 0.85, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.min_area = min_area
        self.max_area = max_area

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        h, w = sample.image.shape[:2]
        area_frac = rng.uniform(self.min_area, self.max_area)
        scale = area_frac**0.5
        crop_h = max(1, int(h * scale))
        crop_w = max(1, int(w * scale))
        top = rng.integers(0, max(1, h - crop_h + 1))
        left = rng.integers(0, max(1, w - crop_w + 1))
        return CellSample(
            image=sample.image[top : top + crop_h, left : left + crop_w].copy(),
            mask=sample.mask[top : top + crop_h, left : left + crop_w].copy(),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class Resize(Transform):
    """Resize the image and mask to exact (height, width)."""

    def __init__(self, height: int, width: int, p: float = 1.0) -> None:
        super().__init__(p=p)
        self.height = height
        self.width = width

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        interp = cv2.INTER_AREA if self.height < sample.height else cv2.INTER_LINEAR
        return CellSample(
            image=cv2.resize(sample.image, (self.width, self.height), interpolation=interp),
            mask=cv2.resize(
                sample.mask, (self.width, self.height), interpolation=cv2.INTER_NEAREST
            ),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class RandomScale(Transform):
    """Randomly scale the image and mask by a factor in [min_scale, max_scale]."""

    def __init__(
        self, min_scale: float = 0.8, max_scale: float = 1.2, p: float = 0.5
    ) -> None:
        super().__init__(p=p)
        self.min_scale = min_scale
        self.max_scale = max_scale

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        scale = rng.uniform(self.min_scale, self.max_scale)
        new_h = max(1, int(sample.height * scale))
        new_w = max(1, int(sample.width * scale))
        interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        return CellSample(
            image=cv2.resize(sample.image, (new_w, new_h), interpolation=interp),
            mask=cv2.resize(sample.mask, (new_w, new_h), interpolation=cv2.INTER_NEAREST),
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class ElasticDistortion(Transform):
    """Apply elastic distortion to image and mask.

    Uses a grid of displacement vectors with random magnitudes, interpolated
    to produce smooth spatial deformations.
    """

    def __init__(
        self, grid_size: int = 8, magnitude: int = 5, p: float = 0.3
    ) -> None:
        super().__init__(p=p)
        self.grid_size = grid_size
        self.magnitude = magnitude

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        h, w = sample.image.shape[:2]
        # Generate random displacement fields on a coarse grid, then upscale
        dx = rng.uniform(-self.magnitude, self.magnitude, (self.grid_size, self.grid_size))
        dy = rng.uniform(-self.magnitude, self.magnitude, (self.grid_size, self.grid_size))
        dx = cv2.resize(dx.astype(np.float32), (w, h))
        dy = cv2.resize(dy.astype(np.float32), (w, h))

        x, y = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
        map_x = x + dx
        map_y = y + dy

        new_img = cv2.remap(sample.image, map_x, map_y, cv2.INTER_LINEAR)
        new_mask = cv2.remap(sample.mask, map_x, map_y, cv2.INTER_NEAREST)
        return CellSample(
            image=new_img,
            mask=new_mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )
