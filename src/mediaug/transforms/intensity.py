"""Intensity transforms that modify only the image, leaving the mask unchanged."""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from skimage.exposure import match_histograms

from mediaug._types import CellSample
from mediaug.transforms.base import Transform

if TYPE_CHECKING:
    from numpy.typing import NDArray


class RandomBrightness(Transform):
    """Randomly adjust brightness by adding a uniform random value."""

    def __init__(self, limit: float = 0.2, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.limit = limit

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        factor = 1.0 + rng.uniform(-self.limit, self.limit)
        img = np.clip(sample.image.astype(np.float32) * factor, 0, 255).astype(np.uint8)
        return CellSample(
            image=img,
            mask=sample.mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class RandomContrast(Transform):
    """Randomly adjust contrast by interpolating toward the mean intensity."""

    def __init__(self, limit: float = 0.2, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.limit = limit

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        factor = 1.0 + rng.uniform(-self.limit, self.limit)
        mean = sample.image.mean()
        img = np.clip(mean + (sample.image.astype(np.float32) - mean) * factor, 0, 255).astype(
            np.uint8
        )
        return CellSample(
            image=img,
            mask=sample.mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class GaussianNoise(Transform):
    """Add Gaussian noise with a given standard deviation."""

    def __init__(self, std: float = 10.0, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.std = std

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        noise = rng.normal(0, self.std, sample.image.shape)
        img = np.clip(sample.image.astype(np.float32) + noise, 0, 255).astype(np.uint8)
        return CellSample(
            image=img,
            mask=sample.mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class HistogramMatching(Transform):
    """Match the histogram of the image to a reference image.

    Uses ``skimage.exposure.match_histograms`` with ``channel_axis=-1``
    (the ``multichannel`` parameter was removed in scikit-image 0.19).
    """

    def __init__(self, reference: NDArray[np.uint8] | None = None, p: float = 0.5) -> None:
        super().__init__(p=p)
        self.reference = reference

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        if self.reference is None:
            return sample
        matched = match_histograms(sample.image, self.reference, channel_axis=-1)
        return CellSample(
            image=matched.astype(np.uint8),
            mask=sample.mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )


class StainNormalization(Transform):
    """Macenko stain normalization for H&E histology images.

    Deconvolves the image into stain optical-density space, normalizes the
    stain concentrations, then reconvolves.  This makes slides stained by
    different labs look visually consistent.

    Reference:
        Macenko et al., "A method for normalizing histology slides for
        quantitative analysis", ISBI 2009.
    """

    def __init__(
        self,
        reference: NDArray[np.uint8] | None = None,
        luminosity_threshold: float = 0.8,
        p: float = 0.5,
    ) -> None:
        super().__init__(p=p)
        self.luminosity_threshold = luminosity_threshold
        self._ref_stain_matrix: NDArray[np.float64] | None = None
        self._ref_concentrations: tuple[float, float] | None = None
        if reference is not None:
            self._fit_reference(reference)

    def _fit_reference(self, reference: NDArray[np.uint8]) -> None:
        stain_matrix = self._get_stain_matrix(reference)
        concentrations = self._get_concentrations(reference, stain_matrix)
        self._ref_stain_matrix = stain_matrix
        max_c = np.percentile(concentrations, 99, axis=0)
        self._ref_concentrations = (float(max_c[0]), float(max_c[1]))

    def _od_from_rgb(self, img: NDArray[np.uint8]) -> NDArray[np.float64]:
        img = img.astype(np.float64) + 1.0  # avoid log(0)
        return -np.log(img / 256.0)

    def _rgb_from_od(self, od: NDArray[np.float64]) -> NDArray[np.uint8]:
        rgb = 256.0 * np.exp(-od) - 1.0
        return np.clip(rgb, 0, 255).astype(np.uint8)

    def _get_stain_matrix(self, img: NDArray[np.uint8]) -> NDArray[np.float64]:
        od = self._od_from_rgb(img).reshape(-1, 3)
        # Keep only pixels above luminosity threshold (tissue, not background)
        od_thresh = od[np.all(od > self.luminosity_threshold * 0.1, axis=1)]
        if od_thresh.shape[0] < 10:
            return np.eye(3)[:2]
        # SVD to find the plane of the two principal stains
        _, _, Vt = np.linalg.svd(od_thresh, full_matrices=False)
        plane = Vt[:2, :]
        # Project OD values onto the plane
        proj = od_thresh @ plane.T
        # Find the angle of each projected point
        angles = np.arctan2(proj[:, 1], proj[:, 0])
        min_angle = np.percentile(angles, 1)
        max_angle = np.percentile(angles, 99)
        v1 = np.array([np.cos(min_angle), np.sin(min_angle)]) @ plane
        v2 = np.array([np.cos(max_angle), np.sin(max_angle)]) @ plane
        # Ensure hematoxylin is first (it has a larger component in the blue channel)
        stain_matrix = np.array([v1, v2]) if v1[0] > v2[0] else np.array([v2, v1])
        # Normalize rows
        stain_matrix /= np.linalg.norm(stain_matrix, axis=1, keepdims=True)
        return stain_matrix

    def _get_concentrations(
        self, img: NDArray[np.uint8], stain_matrix: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        od = self._od_from_rgb(img).reshape(-1, 3)
        # Least-squares solve: od ≈ concentrations @ stain_matrix
        # stain_matrix is (2,3), pinv is (3,2), so od@pinv gives (N,2) concentrations
        return od @ np.linalg.pinv(stain_matrix)

    def apply(self, sample: CellSample, rng: np.random.Generator) -> CellSample:
        if self._ref_stain_matrix is None or self._ref_concentrations is None:
            return sample
        h, w = sample.image.shape[:2]
        src_stain = self._get_stain_matrix(sample.image)
        src_conc = self._get_concentrations(sample.image, src_stain)
        max_c = np.percentile(src_conc, 99, axis=0)
        max_c[max_c == 0] = 1.0  # avoid division by zero
        # Normalize source concentrations to reference range
        src_conc[:, 0] *= self._ref_concentrations[0] / max_c[0]
        src_conc[:, 1] *= self._ref_concentrations[1] / max_c[1]
        # Reconstruct with reference stain matrix
        od_result = src_conc @ self._ref_stain_matrix
        img = self._rgb_from_od(od_result.reshape(h, w, 3))
        return CellSample(
            image=img,
            mask=sample.mask,
            cell_class=sample.cell_class,
            id=sample.id,
            metadata=sample.metadata,
        )
