# MediAug

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

Medical image augmentation for histology and cytology slides.

MediAug provides **cell-level augmentation** — inserting cells with realistic blending, histogram matching, and mask propagation into slide images. This capability is not available in general-purpose augmentation libraries. It is primarily developed for cervical cancer screening (Pap smear slides) but works with any cell image data that has image/mask pairs.

## Results

MediAug supports several augmentation techniques. Here are examples of each:

| Technique | Output |
|-----------|--------|
| Rotation | ![rotate](docs/project_writeup/images/augmentation_examples/rotate_aug1.png) |
| Elastic Deformation | ![elastic](docs/project_writeup/images/augmentation_examples/elastic_deformation_aug1.png) |
| Random Crop | ![crop](docs/project_writeup/images/augmentation_examples/random_crop_aug1.png) |
| Zoom | ![zoom](docs/project_writeup/images/augmentation_examples/zoom_aug1.png) |
| Flip | ![flip](docs/project_writeup/images/augmentation_examples/flip_aug1.png) |

## Installation

```bash
pip install mediaug
```

For development:

```bash
git clone https://github.com/smwade/MediAug
cd MediAug
pip install -e ".[dev,viz]"
```

## Quick Start

```python
import mediaug
import numpy as np

# Load a dataset of cell images
ds = mediaug.CellDataset("path/to/cells")

# Build an augmentation pipeline
pipeline = mediaug.Compose([
    mediaug.Rotate(max_angle=30, p=0.5),
    mediaug.FlipHorizontal(p=0.5),
    mediaug.RandomBrightness(limit=0.2, p=0.3),
    mediaug.InsertCell(cell_source=ds, num_cells=(1, 5), p=0.8),
])

# Apply with full reproducibility
rng = np.random.default_rng(42)
sample = ds.random_sample(rng=rng)
augmented = pipeline(sample, rng=rng)
```

## Available Transforms

### Geometric (applied to both image and mask)

| Transform | Parameters |
|-----------|-----------|
| `Rotate` | `max_angle`, `p` |
| `FlipHorizontal` | `p` |
| `FlipVertical` | `p` |
| `RandomCrop` | `min_area`, `max_area`, `p` |
| `Resize` | `height`, `width`, `p` |
| `RandomScale` | `min_scale`, `max_scale`, `p` |
| `ElasticDistortion` | `grid_size`, `magnitude`, `p` |

### Intensity (applied to image only)

| Transform | Parameters |
|-----------|-----------|
| `RandomBrightness` | `limit`, `p` |
| `RandomContrast` | `limit`, `p` |
| `GaussianNoise` | `std`, `p` |
| `HistogramMatching` | `reference`, `p` |
| `StainNormalization` | `reference`, `luminosity_threshold`, `p` |

### Cell-level (unique to MediAug)

| Transform | Parameters |
|-----------|-----------|
| `InsertCell` | `cell_source`, `cell_classes`, `num_cells`, `scale_mean`, `scale_std`, `blend_method`, `edge_softening`, `p` |

### Composition

| Class | Description |
|-------|-------------|
| `Compose` | Apply transforms sequentially |
| `OneOf` | Randomly pick and apply one transform |

## Dataset Format

MediAug expects image/mask pairs organized by cell class:

```
dataset/
  class_name/
    image/
      001.png
      002.png
    mask/
      001.png
      002.png
```

### Supported Datasets

- **SIPaKMeD**: 4,049 cells across 5 categories ([link](http://cs.uoi.gr/~marina/sipakmed.html))
- **SMEAR**: 917 cells segmented by nucleus/cytoplasm ([link](https://mde-lab.aegean.gr/downloads))

Download SIPaKMeD:

```bash
mediaug download
```

## CLI

```bash
mediaug --help          # Show all commands
mediaug info <dir>      # Show dataset statistics
mediaug resize ...      # Resize images in a directory
mediaug augment ...     # Generate augmented dataset
mediaug download        # Download SIPaKMeD dataset
```

## Notebooks

Example notebooks are available in `notebooks/` demonstrating dataset loading, augmentation pipelines, and cell insertion.

## License

MIT
