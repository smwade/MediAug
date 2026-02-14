"""Tests for CellDataset."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mediaug._types import CellSample
from mediaug.datasets.base import CellDataset


class TestCellDataset:
    def test_load_from_dir(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        assert ds.size == 6  # 3 per class x 2 classes
        assert len(ds.classes) == 2

    def test_class_indexing(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        samples = ds["class_a"]
        assert len(samples) == 3
        assert all(isinstance(s, CellSample) for s in samples)

    def test_integer_indexing(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        sample = ds[0]
        assert isinstance(sample, CellSample)

    def test_negative_indexing(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        sample = ds[-1]
        assert isinstance(sample, CellSample)

    def test_index_out_of_range(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        with pytest.raises(IndexError):
            ds[100]

    def test_unknown_class(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        with pytest.raises(KeyError, match="Unknown class"):
            ds["nonexistent"]

    def test_len(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        assert len(ds) == 6

    def test_iter(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        all_samples = list(ds)
        assert len(all_samples) == 6

    def test_random_sample(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        rng = np.random.default_rng(42)
        s = ds.random_sample(rng=rng)
        assert isinstance(s, CellSample)

    def test_random_sample_deterministic(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        s1 = ds.random_sample(rng=np.random.default_rng(42))
        s2 = ds.random_sample(rng=np.random.default_rng(42))
        np.testing.assert_array_equal(s1.image, s2.image)

    def test_create_empty_dataset(self, tmp_path: Path) -> None:
        ds_path = tmp_path / "new_dataset"
        ds = CellDataset(ds_path, classes=["alpha", "beta"])
        assert ds.size == 0
        assert sorted(ds.classes) == ["alpha", "beta"]
        assert (ds_path / "alpha" / "image").is_dir()
        assert (ds_path / "alpha" / "mask").is_dir()

    def test_add_data(self, tmp_path: Path) -> None:
        ds_path = tmp_path / "add_test"
        ds = CellDataset(ds_path, classes=["cls"])
        img = np.zeros((32, 32, 3), dtype=np.uint8)
        mask = np.zeros((32, 32, 3), dtype=np.uint8)
        ds.add_data(img, mask, "cls", "sample_001")
        assert ds.size == 1
        loaded = ds["cls"][0]
        assert loaded.image.shape == (32, 32, 3)

    def test_nonexistent_path_no_classes(self, tmp_path: Path) -> None:
        with pytest.raises(ValueError, match="does not exist"):
            CellDataset(tmp_path / "does_not_exist")

    def test_repr(self, tiny_dataset: Path) -> None:
        ds = CellDataset(tiny_dataset)
        r = repr(ds)
        assert "CellDataset" in r
        assert "size=6" in r
