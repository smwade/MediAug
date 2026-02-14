"""Tests for I/O modules."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from mediaug.io.masks import generate_cell_mask, generate_cell_mask_list
from mediaug.io.readers import read_dat, read_image
from mediaug.io.writers import save_image

FIXTURES_DIR = Path(__file__).parent / "fixtures"


class TestReadImage:
    def test_read_existing_image(self) -> None:
        img = read_image(FIXTURES_DIR / "cell_img.png")
        assert img.ndim == 3
        assert img.shape[2] == 3
        assert img.dtype == np.uint8

    def test_read_rgb_default(self) -> None:
        img_rgb = read_image(FIXTURES_DIR / "cell_img.png", color_mode="rgb")
        img_bgr = read_image(FIXTURES_DIR / "cell_img.png", color_mode="bgr")
        # R and B channels should be swapped
        np.testing.assert_array_equal(img_rgb[:, :, 0], img_bgr[:, :, 2])
        np.testing.assert_array_equal(img_rgb[:, :, 2], img_bgr[:, :, 0])

    def test_read_missing_file(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_image("/nonexistent/path.png")


class TestReadDat:
    def test_read_dat_file(self) -> None:
        dat = read_dat(FIXTURES_DIR / "dat" / "007_nuc01.dat")
        assert dat.ndim == 2
        assert dat.shape[1] == 2

    def test_read_missing_dat(self) -> None:
        with pytest.raises(FileNotFoundError):
            read_dat("/nonexistent/file.dat")


class TestSaveImage:
    def test_roundtrip(self, tmp_path: Path) -> None:
        img = np.random.default_rng(0).integers(0, 255, (64, 64, 3), dtype=np.uint8)
        out_path = tmp_path / "test.png"
        save_image(img, out_path)
        loaded = read_image(out_path)
        np.testing.assert_array_equal(img, loaded)

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        out_path = tmp_path / "a" / "b" / "c" / "test.png"
        img = np.zeros((32, 32, 3), dtype=np.uint8)
        save_image(img, out_path)
        assert out_path.exists()


class TestMaskGeneration:
    def test_generate_cell_mask(self) -> None:
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cyto = np.array([[20, 20], [80, 20], [80, 80], [20, 80]], dtype=np.float64)
        nuc = np.array([[40, 40], [60, 40], [60, 60], [40, 60]], dtype=np.float64)
        mask = generate_cell_mask(img, cyto, nuc)
        assert mask.shape == (100, 100, 3)
        assert mask.dtype == np.uint8
        # Should have non-zero pixels where polygons were drawn
        assert mask.sum() > 0

    def test_generate_cell_mask_list(self) -> None:
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cytos = [np.array([[10, 10], [40, 10], [40, 40], [10, 40]], dtype=np.float64)]
        nucs = [np.array([[20, 20], [30, 20], [30, 30], [20, 30]], dtype=np.float64)]
        mask = generate_cell_mask_list(img, cytos, nucs)
        assert mask.shape == (100, 100, 3)
        assert mask.sum() > 0
