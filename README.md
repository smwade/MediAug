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