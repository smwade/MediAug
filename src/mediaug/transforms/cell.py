"""Cell insertion transform — MediAug's unique value proposition.

Inserts individual cell images into slide backgrounds with realistic blending,
mask propagation, and optional histogram matching. Refactored from the original
``augment.py:randomly_insert_cells()`` and ``add_cell()`` functions.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import cv2
import numpy as np
from skimage.exposure import match_histograms

from mediaug._constants import CYTO_BLEND_ALPHA, CYTO_GRAY, NUC_BLEND_ALPHA, NUC_GRAY
from mediaug._types import CellSample
from mediaug.transforms.base import Transform

if TYPE_CHECKING:
    from mediaug.datasets.base import CellDataset


# ---------------------------------------------------------------------------
# Internal compositing helpers (from image_utils.py)
# ---------------------------------------------------------------------------


def _soften_mask(mask: np.ndarray, amount: int = 5) -> np.ndarray:
    """Soften mask edges by dilation followed by Gaussian blur."""
    kernel = np.ones((5, 5), np.uint8)
    dilated = cv2.dilate(mask, kernel, iterations=amount)
    blurred = cv2.GaussianBlur(dilated, (5, 5), 0)
    return cv2.max(mask, blurred)


def _place_image_on_image(
    bg: np.ndarray, fg: np.ndarray, center: tuple[int, int]
) -> np.ndarray:
    """Place *fg* on *bg* centered at *center*, handling boundary clipping."""
    ch, cw = center
    fg_h, fg_w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    if cw < 0 or cw > bg_w or ch < 0 or ch > bg_h:
        return bg.copy()

    left_w = cw - fg_w // 2
    left_h = ch - fg_h // 2
    end_w = left_w + fg_w
    end_h = left_h + fg_h

    abs_left_w = max(left_w, 0)
    abs_left_h = max(left_h, 0)
    abs_end_w = min(end_w, bg_w)
    abs_end_h = min(end_h, bg_h)

    fg_left_w = abs(min(left_w, 0))
    fg_left_h = abs(min(left_h, 0))
    diff_w = bg_w - end_w
    diff_h = bg_h - end_h
    fg_end_w = fg_w if diff_w >= 0 else diff_w
    fg_end_h = fg_h if diff_h >= 0 else diff_h

    result = bg.copy()
    result[abs_left_h:abs_end_h, abs_left_w:abs_end_w] = fg[
        fg_left_h:fg_end_h, fg_left_w:fg_end_w
    ]
    return result


def _alpha_blend(
    bg: np.ndarray,
    fg: np.ndarray,
    fg_mask: np.ndarray,
    center: tuple[int, int],
) -> np.ndarray:
    """Blend *fg* into *bg* using *fg_mask* as an alpha channel."""
    alpha = np.zeros(bg.shape[:2], dtype=np.uint8)
    alpha = _place_image_on_image(alpha, fg_mask, center)
    cell_img = _place_image_on_image(bg.copy(), fg, center)

    alpha_f = alpha.astype(np.float32) / 255.0
    if bg.ndim == 3:
        alpha_f = np.repeat(alpha_f[:, :, np.newaxis], 3, axis=2)

    blended = cv2.multiply(alpha_f, cell_img.astype(np.float32))
    background = cv2.multiply(1.0 - alpha_f, bg.astype(np.float32))
    return cv2.add(blended, background).astype(np.uint8)


# ---------------------------------------------------------------------------
# Rotation helper (from image_utils.py)
# ---------------------------------------------------------------------------


def _rotate_array(image: np.ndarray, angle: float) -> np.ndarray:
    """Rotate with canvas expansion."""
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


# ---------------------------------------------------------------------------
# InsertCell transform
# ---------------------------------------------------------------------------


class InsertCell(Transform):
    """Insert random cells from a dataset into the sample image.

    This is MediAug's core differentiator: realistic cell-level augmentation
    with mask propagation, histogram matching, and edge softening.

    Args:
        cell_source: A ``CellDataset`` from which donor cells are drawn.
        cell_classes: Which cell classes to draw from. If ``None``, uses all
            classes in *cell_source*.
        num_cells: ``(min, max)`` range for the number of cells to insert per
            call.  Sampled uniformly.
        scale_mean: Mean of the normal distribution for cell scaling.
        scale_std: Standard deviation for the scale distribution.
        blend_method: ``None`` for direct compositing, ``"hist"`` to match
            the donor cell's histogram to the background before insertion.
        edge_softening: Dilation iterations for mask edge softening.
        p: Probability of applying this transform.
    """

    def __init__(
        self,
        cell_source: CellDataset,
        cell_classes: list[str] | None = None,
        num_cells: tuple[int, int] = (1, 5),
        scale_mean: float = 1.0,
        scale_std: float = 0.2,
        blend_method: str | None = None,
        edge_softening: int = 1,
        p: float = 0.8,
    ) -> None:
        super().__init__(p=p)
        self.cell_source = cell_source
        self.cell_classes = cell_classes
        self.num_cells = num_cells
        self.scale_mean = scale_mean
        self.scale_std = scale_std
        self.blend_method = blend_method
        self.edge_softening = edge_softening

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        img = sample.image.copy()
        mask = sample.mask.copy()

        n = int(rng.integers(self.num_cells[0], self.num_cells[1] + 1))

        classes = self.cell_classes or self.cell_source.classes
        # Collect candidate cells
        candidates: list[CellSample] = []
        for cls in classes:
            candidates.extend(self.cell_source[cls])

        if not candidates:
            return sample

        h, w = img.shape[:2]
        border = 5

        for _ in range(n):
            idx = rng.integers(len(candidates))
            cell = candidates[idx]
            pos = (int(rng.integers(border, max(border + 1, h - border))),
                   int(rng.integers(border, max(border + 1, w - border))))
            angle = float(rng.integers(0, 360))
            scale = max(0.1, rng.normal(self.scale_mean, self.scale_std))

            img, mask = self._add_cell(img, mask, cell, pos, angle, scale)

        return CellSample(
            image=img,
            mask=mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )

    def _add_cell(
        self,
        bg: np.ndarray,
        bg_mask: np.ndarray,
        cell: CellSample,
        pos: tuple[int, int],
        angle: float,
        scale: float,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Composite a single cell onto the background."""
        fg = cv2.resize(cell.image, (0, 0), fx=scale, fy=scale)
        orig_fg_mask = cv2.resize(cell.mask, (0, 0), fx=scale, fy=scale)

        fg_mask_gray = cv2.cvtColor(orig_fg_mask, cv2.COLOR_RGB2GRAY)

        # Optional histogram matching
        if self.blend_method == "hist":
            fg = match_histograms(fg, bg, channel_axis=-1).astype(np.uint8)

        # Map mask gray values to blend alpha values
        fg_mask_gray[fg_mask_gray == CYTO_GRAY] = CYTO_BLEND_ALPHA
        fg_mask_gray[fg_mask_gray == NUC_GRAY] = NUC_BLEND_ALPHA

        fg = _rotate_array(fg, angle)
        fg_mask_gray = _rotate_array(fg_mask_gray, angle)
        fg_mask_gray = _soften_mask(fg_mask_gray, amount=self.edge_softening)

        new_img = _alpha_blend(bg, fg, fg_mask_gray, pos)

        # For the mask overlay, make a binary alpha so the original mask colors
        # are preserved in the composited mask
        binary_alpha = fg_mask_gray.copy()
        binary_alpha[binary_alpha != 0] = 255
        new_mask = _alpha_blend(bg_mask, orig_fg_mask, binary_alpha, pos)

        return new_img, new_mask
