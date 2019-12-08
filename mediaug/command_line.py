import pathlib
from PIL import Image
import os
from os.path import join
import click


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mesage')
    args = parser.parse_args()


@click.command()
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
