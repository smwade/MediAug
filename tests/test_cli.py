"""Smoke tests for the CLI."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
from click.testing import CliRunner

from mediaug.cli.main import cli


class TestCLI:
    def test_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "MediAug" in result.output

    def test_resize_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["resize", "--help"])
        assert result.exit_code == 0
        assert "WIDTH" in result.output

    def test_augment_help(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["augment", "--help"])
        assert result.exit_code == 0
        assert "--slide-dir" in result.output

    def test_info_command(self, tiny_dataset: Path) -> None:
        runner = CliRunner()
        result = runner.invoke(cli, ["info", str(tiny_dataset)])
        assert result.exit_code == 0
        assert "Total samples: 6" in result.output

    def test_resize_command(self, tmp_path: Path) -> None:
        # Create a small input directory with an image
        in_dir = tmp_path / "input"
        in_dir.mkdir()
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(str(in_dir / "test.png"), img)

        out_dir = tmp_path / "output"
        runner = CliRunner()
        result = runner.invoke(cli, ["resize", str(in_dir), str(out_dir), "32", "32"])
        assert result.exit_code == 0
        assert "Resized 1 images" in result.output
