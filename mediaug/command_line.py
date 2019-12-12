import pathlib
from PIL import Image
import os
import random
from os.path import join
import click
from math import floor
from itertools import cycle

from mediaug.image_utils import read_png, save_img, get_blank_mask
from mediaug.utils import create_dirs
from mediaug.data_prep import make_pix2pix_format
from mediaug.dataset import Dataset
from mediaug.augment import randomly_insert_cells


@click.group()
def cli():
    pass


@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('out_dir', type=click.Path(exists=False))
@click.argument('w')
@click.argument('h')
@click.option('--out_type', default='png')
def resize_image(in_dir, out_dir, w, h):
    """resize all images in a dir"""
    print(in_dir, out_dir, h, w)
    pathlib.Path(out_dir).mkdir(parents=True)
    for subdir, dirs, files in os.walk(in_dir):
        for file in files:
            if file.endswith('png') or file.endswith('jpg'):
                im = Image.open(join(subdir, file))
                imResize = im.resize((h, w), Image.ANTIALIAS)
                cell_type = os.path.basename(subdir)
                pathlib.Path(join(out_dir, cell_type)).mkdir(parents=True, exist_ok=True)
                imResize.save(join(out_dir, cell_type, file), 'PNG')


@cli.command()
@click.option('--slide_dir', type=click.Path(exists=True), required=True)
@click.option('--cell_dir', type=click.Path(exists=True), required=True)
@click.option('--out_dir', type=click.Path(), required=True)
@click.option('--num', type=int, required=True)
@click.option('--max_cells', type=int, default=7)
def generate_augment_dataset(slide_dir, cell_dir, out_dir, num, max_cells):
    """ Adds cells to slides to produce a weekly supervised training
    dataset for SIPaKMeD dataset.
    """
    slides = Dataset(slide_dir)
    cells = Dataset(cell_dir)
    out_ds = Dataset(out_dir, ['all'])

    good_slides = slides['superficial-intermediate'] + slides['parabasal']
    random.shuffle(good_slides)
    slide_generator = cycle(good_slides)

    bad_cells = list(set(slides.classes) - set(['superficial-intermediate', 'parabasal']))

    for i in range(num):
        slide = next(slide_generator)
        new_img, new_mask = randomly_insert_cells(slide.img, get_blank_mask(slide.img), cells, bad_cells, (0,max_cells))
        out_ds.add_data(new_img, new_mask, 'all', i)


@cli.command()
@click.option('-i', '--image_dir', type=click.Path(exists=True), required=True)
@click.option('-m', '--mask_dir', type=click.Path(exists=True), required=True)
@click.option('-o', '--out_dir', type=click.Path(), required=True)
@click.option('-r', '--split_ratio', type=float, required=True)
def prepare_pix2pix_images(image_dir, mask_dir, out_dir, split_ratio):
    """ Prepares images to be in correct format for Pix2Pix algorithm."""
    images_list = os.listdir(image_dir)
    create_dirs(out_dir, ['train', 'val', 'test', 'all'])
    
    # calc split cutoffs
    train_cutoff = floor(split_ratio * len(images_list))
    val_cutoff = train_cutoff + floor((len(images_list)-train_cutoff) // 2)

    for i, image_path in enumerate(images_list):
        mask_path = join(mask_dir, os.path.basename(image_path))
        img = read_png(join(image_dir, image_path))
        mask = read_png(join(mask_dir, mask_path))
        new_img = make_pix2pix_format(img, mask)

        # split the data
        if i < train_cutoff:
            save_img(new_img, join(out_dir, 'train', f'{i}.jpg'))
        elif i < val_cutoff:
            save_img(new_img, join(out_dir, 'val', f'{i}.jpg'))
        else:
            save_img(new_img, join(out_dir, 'test', f'{i}.jpg'))
        save_img(new_img, join(out_dir, 'all', f'{i}.jpg'))
