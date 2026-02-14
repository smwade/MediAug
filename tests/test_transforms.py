"""Tests for the transform system."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mediaug._types import CellSample
from mediaug.datasets.base import CellDataset
from mediaug.transforms.base import Compose, OneOf
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


class TestTransformBase:
    def test_p_zero_skips(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = FlipHorizontal(p=0.0)
        result = t(sample_cell, rng)
        assert result is sample_cell

    def test_p_one_applies(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = FlipHorizontal(p=1.0)
        result = t(sample_cell, rng)
        assert result is not sample_cell

    def test_invalid_p(self) -> None:
        with pytest.raises(ValueError, match="p must be"):
            FlipHorizontal(p=1.5)


class TestCompose:
    def test_sequential_application(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        pipeline = Compose([FlipHorizontal(p=1.0), FlipVertical(p=1.0)])
        result = pipeline(sample_cell, rng)
        # Double flip should change the image
        assert result.image.shape == sample_cell.image.shape
        assert result.cell_class == sample_cell.cell_class

    def test_empty_compose(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        pipeline = Compose([])
        result = pipeline(sample_cell, rng)
        np.testing.assert_array_equal(result.image, sample_cell.image)


class TestOneOf:
    def test_applies_one(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = OneOf([FlipHorizontal(p=1.0), FlipVertical(p=1.0)], p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape

    def test_p_zero_skips(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = OneOf([FlipHorizontal(p=1.0)], p=0.0)
        result = t(sample_cell, rng)
        assert result is sample_cell


class TestGeometricTransforms:
    def test_rotate_shape(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = Rotate(max_angle=45, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.ndim == 3
        assert result.mask.ndim == 3
        assert result.image.shape == result.mask.shape

    def test_flip_horizontal(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = FlipHorizontal(p=1.0)
        result = t(sample_cell, rng)
        np.testing.assert_array_equal(result.image, np.fliplr(sample_cell.image))
        np.testing.assert_array_equal(result.mask, np.fliplr(sample_cell.mask))

    def test_flip_vertical(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = FlipVertical(p=1.0)
        result = t(sample_cell, rng)
        np.testing.assert_array_equal(result.image, np.flipud(sample_cell.image))

    def test_random_crop_smaller(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        t = RandomCrop(min_area=0.3, max_area=0.5, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape[0] <= sample_cell.image.shape[0]
        assert result.image.shape[1] <= sample_cell.image.shape[1]
        assert result.image.shape == result.mask.shape

    def test_resize_exact(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = Resize(height=64, width=64, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == (64, 64, 3)
        assert result.mask.shape == (64, 64, 3)

    def test_random_scale(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = RandomScale(min_scale=0.5, max_scale=1.5, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.ndim == 3
        assert result.image.shape == result.mask.shape

    def test_elastic_distortion_shape(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        t = ElasticDistortion(grid_size=4, magnitude=3, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.mask.shape == sample_cell.mask.shape


class TestIntensityTransforms:
    def test_brightness_shape(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = RandomBrightness(limit=0.3, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.image.dtype == np.uint8
        # Mask should be unchanged
        np.testing.assert_array_equal(result.mask, sample_cell.mask)

    def test_contrast_shape(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = RandomContrast(limit=0.3, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        np.testing.assert_array_equal(result.mask, sample_cell.mask)

    def test_gaussian_noise(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        t = GaussianNoise(std=15.0, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.image.dtype == np.uint8
        np.testing.assert_array_equal(result.mask, sample_cell.mask)

    def test_histogram_matching_no_ref(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        t = HistogramMatching(reference=None, p=1.0)
        result = t(sample_cell, rng)
        np.testing.assert_array_equal(result.image, sample_cell.image)

    def test_histogram_matching_with_ref(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        ref = (sample_cell.image * 0.8).astype(np.uint8)
        t = HistogramMatching(reference=ref, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape


class TestStainNormalization:
    def test_no_reference_passthrough(
        self, sample_cell: CellSample, rng: np.random.Generator
    ) -> None:
        t = StainNormalization(reference=None, p=1.0)
        result = t(sample_cell, rng)
        np.testing.assert_array_equal(result.image, sample_cell.image)

    def test_with_reference(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        ref = (sample_cell.image * 0.9).astype(np.uint8)
        t = StainNormalization(reference=ref, p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.image.dtype == np.uint8
        # Mask should be unchanged
        np.testing.assert_array_equal(result.mask, sample_cell.mask)

    def test_preserves_metadata(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        ref = sample_cell.image.copy()
        t = StainNormalization(reference=ref, p=1.0)
        result = t(sample_cell, rng)
        assert result.cell_class == sample_cell.cell_class
        assert result.id == sample_cell.id


class TestInsertCell:
    def test_insert_cell_basic(
        self, sample_cell: CellSample, tiny_dataset: Path, rng: np.random.Generator
    ) -> None:
        ds = CellDataset(tiny_dataset)
        t = InsertCell(cell_source=ds, num_cells=(1, 3), p=1.0)
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.mask.shape == sample_cell.mask.shape
        assert result.cell_class == sample_cell.cell_class

    def test_insert_cell_with_hist_matching(
        self, sample_cell: CellSample, tiny_dataset: Path, rng: np.random.Generator
    ) -> None:
        ds = CellDataset(tiny_dataset)
        t = InsertCell(
            cell_source=ds,
            num_cells=(1, 2),
            blend_method="hist",
            p=1.0,
        )
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape

    def test_insert_cell_specific_classes(
        self, sample_cell: CellSample, tiny_dataset: Path, rng: np.random.Generator
    ) -> None:
        ds = CellDataset(tiny_dataset)
        t = InsertCell(
            cell_source=ds,
            cell_classes=["class_a"],
            num_cells=(1, 2),
            p=1.0,
        )
        result = t(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape

    def test_insert_cell_deterministic(
        self, sample_cell: CellSample, tiny_dataset: Path
    ) -> None:
        ds = CellDataset(tiny_dataset)
        t = InsertCell(cell_source=ds, num_cells=(2, 4), p=1.0)
        rng1 = np.random.default_rng(99)
        rng2 = np.random.default_rng(99)
        result1 = t(sample_cell, rng1)
        result2 = t(sample_cell, rng2)
        np.testing.assert_array_equal(result1.image, result2.image)
        np.testing.assert_array_equal(result1.mask, result2.mask)

    def test_insert_cell_p_zero(
        self, sample_cell: CellSample, tiny_dataset: Path, rng: np.random.Generator
    ) -> None:
        ds = CellDataset(tiny_dataset)
        t = InsertCell(cell_source=ds, num_cells=(1, 3), p=0.0)
        result = t(sample_cell, rng)
        assert result is sample_cell


class TestRepr:
    def test_transform_repr(self) -> None:
        t = FlipHorizontal(p=0.5)
        assert "FlipHorizontal" in repr(t)
        assert "0.5" in repr(t)

    def test_compose_repr(self) -> None:
        c = Compose([FlipHorizontal(p=0.5), Rotate(max_angle=30)])
        r = repr(c)
        assert "Compose" in r
        assert "FlipHorizontal" in r
        assert "Rotate" in r

    def test_oneof_repr(self) -> None:
        o = OneOf([FlipHorizontal(), FlipVertical()], p=0.7)
        r = repr(o)
        assert "OneOf" in r
        assert "0.7" in r


class TestDeterminism:
    def test_same_rng_same_result(self, sample_cell: CellSample) -> None:
        t = Compose([
            Rotate(max_angle=30, p=1.0),
            RandomBrightness(limit=0.2, p=1.0),
        ])
        rng1 = np.random.default_rng(123)
        rng2 = np.random.default_rng(123)
        result1 = t(sample_cell, rng1)
        result2 = t(sample_cell, rng2)
        np.testing.assert_array_equal(result1.image, result2.image)
        np.testing.assert_array_equal(result1.mask, result2.mask)


class TestIntegration:
    def test_full_pipeline(
        self, sample_cell: CellSample, tiny_dataset: Path
    ) -> None:
        """End-to-end: load dataset, build pipeline, apply, verify determinism."""
        ds = CellDataset(tiny_dataset)

        pipeline = Compose([
            Rotate(max_angle=15, p=0.5),
            FlipHorizontal(p=0.5),
            RandomBrightness(limit=0.1, p=0.3),
            GaussianNoise(std=5.0, p=0.3),
            InsertCell(cell_source=ds, num_cells=(1, 3), p=1.0),
        ])

        # Two runs with the same seed should produce identical output
        rng1 = np.random.default_rng(42)
        rng2 = np.random.default_rng(42)

        result1 = pipeline(sample_cell, rng1)
        result2 = pipeline(sample_cell, rng2)

        np.testing.assert_array_equal(result1.image, result2.image)
        np.testing.assert_array_equal(result1.mask, result2.mask)
        assert result1.image.dtype == np.uint8
        assert result1.cell_class == sample_cell.cell_class

    def test_pipeline_with_oneof(self, sample_cell: CellSample, rng: np.random.Generator) -> None:
        pipeline = Compose([
            OneOf([
                RandomBrightness(limit=0.2, p=1.0),
                RandomContrast(limit=0.2, p=1.0),
                GaussianNoise(std=10.0, p=1.0),
            ], p=1.0),
            FlipHorizontal(p=0.5),
        ])
        result = pipeline(sample_cell, rng)
        assert result.image.shape == sample_cell.image.shape
        assert result.image.dtype == np.uint8
