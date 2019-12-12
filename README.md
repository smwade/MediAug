# MediAug

## Overview

MediAug is a set of tools for data augmentation of histology
slides. It is primaraly developed for cervical cancer by
augmenting Pap smear slides. However, it can be extended to
any cell data that has an image and mask of different types of
cells. Currently supports general image augmentation techniques
as well as specialized ones like cell insertion and blending.

## Installation

To install:

```bash
git clone https://github.com/smwade/MediAug
python setup.py install
```

## CLI

MediAug comes with a CLI with useful scripts. These include:

* generate-augment-dataset
* prepare-pix2pix-images
* resize-images

The list of all can be seen with the command

```bash
mediaug --help
```

### Generate cell augmented dataset

```bash
mediaug generate-augment-dataset --slide_dir <slide_dir> --cell_dir <cell_dir> --out_dir <out_dir> --num 1000 --max_cells <10>
```

### Prepare images for Pix2Pix

```bash
mediaug prepare-pix2pix-images --image_dir <image_dir> --mask_dir <mask_dir> --out_dir <out_dir> --split_ratio <split_ratio>
```

### Recursivly resize all images in directory

```bash
mediaug resize-images --input_dir <input_dir> --out_dir <out_dir> --w 256 --height 256
```
