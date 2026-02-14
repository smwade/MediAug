"""MediAug CLI — command-line tools for dataset augmentation.

Replaces the original ``command_line.py`` with:
- Fixed ``Image.ANTIALIAS`` → ``Image.Resampling.LANCZOS``
- ``pathlib.Path`` throughout
- ``--seed`` for reproducibility
- Removed ``prepare-pix2pix-images`` (model-specific)
- Added ``download`` and ``info`` commands
"""

from __future__ import annotations

import logging
from itertools import cycle
from pathlib import Path

import click
import numpy as np

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
def cli(verbose: bool) -> None:
    """MediAug — medical image augmentation tools."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")


@cli.command()
@click.argument("input_dir", type=click.Path(exists=True, path_type=Path))
@click.argument("out_dir", type=click.Path(path_type=Path))
@click.argument("width", type=int)
@click.argument("height", type=int)
def resize(input_dir: Path, out_dir: Path, width: int, height: int) -> None:
    """Resize all images in INPUT_DIR to WIDTH x HEIGHT, saving to OUT_DIR."""
    from PIL import Image

    out_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for img_path in sorted(input_dir.rglob("*")):
        if img_path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".bmp", ".tiff"):
            continue
        relative = img_path.relative_to(input_dir)
        dest = out_dir / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        im = Image.open(img_path)
        im_resized = im.resize((width, height), Image.Resampling.LANCZOS)
        im_resized.save(dest)
        count += 1
    click.echo(f"Resized {count} images to {width}x{height} in {out_dir}")


@cli.command()
@click.option("--slide-dir", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--cell-dir", type=click.Path(exists=True, path_type=Path), required=True)
@click.option("--out-dir", type=click.Path(path_type=Path), required=True)
@click.option("--num", type=int, required=True, help="Number of augmented slides to generate.")
@click.option("--max-cells", type=int, default=7, help="Max cells to insert per slide.")
@click.option("--seed", type=int, default=None, help="Random seed for reproducibility.")
def augment(
    slide_dir: Path,
    cell_dir: Path,
    out_dir: Path,
    num: int,
    max_cells: int,
    seed: int | None,
) -> None:
    """Generate an augmented dataset by inserting cells into slide backgrounds."""
    from mediaug.datasets.base import CellDataset
    from mediaug.transforms.cell import InsertCell

    rng = np.random.default_rng(seed)

    slides = CellDataset(slide_dir)
    cells = CellDataset(cell_dir)
    out_ds = CellDataset(out_dir, classes=["all"])

    # Use normal slides as backgrounds
    good_classes = [c for c in ["superficial-intermediate", "parabasal"] if c in slides.classes]
    good_slides = []
    for cls in good_classes:
        good_slides.extend(slides[cls])
    rng.shuffle(good_slides)  # type: ignore[arg-type]
    slide_iter = cycle(good_slides)

    bad_classes = [c for c in slides.classes if c not in good_classes]

    inserter = InsertCell(
        cell_source=cells,
        cell_classes=bad_classes,
        num_cells=(0, max_cells),
    )

    for i in range(num):
        slide = next(slide_iter)
        augmented = inserter.apply(slide, rng)
        out_ds.add_data(augmented.image, augmented.mask, "all", str(i))
        if (i + 1) % 10 == 0:
            click.echo(f"Generated {i + 1}/{num} augmented slides")

    click.echo(f"Done. {num} augmented slides saved to {out_dir}")


@cli.command()
@click.option(
    "--dest",
    type=click.Path(path_type=Path),
    default=None,
    help="Download destination (default: ~/.mediaug/sipakmed_raw).",
)
def download(dest: Path | None) -> None:
    """Download the SIPaKMeD dataset."""
    from mediaug.datasets.sipakmed import download_sipakmed

    path = download_sipakmed(data_dest=dest)
    click.echo(f"Downloaded to: {path}")


@cli.command()
@click.argument("data_dir", type=click.Path(exists=True, path_type=Path))
def info(data_dir: Path) -> None:
    """Show dataset statistics."""
    from mediaug.datasets.base import CellDataset

    ds = CellDataset(data_dir)
    click.echo(f"Dataset: {data_dir}")
    click.echo(f"Total samples: {ds.size}")
    click.echo(f"Classes ({len(ds.classes)}):")
    for cls in ds.classes:
        click.echo(f"  {cls}: {len(ds[cls])} samples")
