"""Shared test fixtures."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from mediaug._types import CellSample

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def rng() -> np.random.Generator:
    """Deterministic random generator for reproducible tests."""
    return np.random.default_rng(42)


@pytest.fixture()
def sample_cell() -> CellSample:
    """A CellSample loaded from the test fixture images."""
    img_path = FIXTURES_DIR / "cell_img.png"
    mask_path = FIXTURES_DIR / "cell_mask.png"
    img = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
    mask = cv2.cvtColor(cv2.imread(str(mask_path)), cv2.COLOR_BGR2RGB)
    # Ensure mask matches image dimensions (fixture files may differ)
    h, w = img.shape[:2]
    if mask.shape[:2] != (h, w):
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
    return CellSample(image=img, mask=mask, cell_class="test_class", id="test_001")


@pytest.fixture()
def sample_slide() -> CellSample:
    """A CellSample from the slide fixture images."""
    img_path = FIXTURES_DIR / "slide_img.png"
    mask_path = FIXTURES_DIR / "slide_mask.png"
    img = cv2.cvtColor(cv2.imread(str(img_path)), cv2.COLOR_BGR2RGB)
    mask = cv2.cvtColor(cv2.imread(str(mask_path)), cv2.COLOR_BGR2RGB)
    h, w = img.shape[:2]
    if mask.shape[:2] != (h, w):
        mask = cv2.resize(mask, (w, h), interpolation=cv2.INTER_NEAREST)
    return CellSample(image=img, mask=mask, cell_class="slide", id="slide_001")


@pytest.fixture()
def tiny_dataset(tmp_path: Path, sample_cell: CellSample) -> Path:
    """Create a minimal dataset directory structure with a few samples."""
    for cls in ("class_a", "class_b"):
        img_dir = tmp_path / cls / "image"
        mask_dir = tmp_path / cls / "mask"
        img_dir.mkdir(parents=True)
        mask_dir.mkdir(parents=True)
        for i in range(3):
            cv2.imwrite(
                str(img_dir / f"{i:03d}.png"),
                cv2.cvtColor(sample_cell.image, cv2.COLOR_RGB2BGR),
            )
            cv2.imwrite(
                str(mask_dir / f"{i:03d}.png"),
                cv2.cvtColor(sample_cell.mask, cv2.COLOR_RGB2BGR),
            )
    return tmp_path
