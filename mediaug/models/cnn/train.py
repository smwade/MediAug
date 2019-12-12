import os
import numpy as np
import click
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from utils import get_callbacks
from model import get_model


@click.command()
@click.option('--input_dir', type=click.Path(exists=True), required=True)
@click.option('--log_dir', type=click.Path(), required=True)
@click.option('--batch_size', default=32)
@click.option('--epochs', default=200)
@click.option('--img_width', default=256)
@click.option('--img_height', default=256)
@click.option('--val_split', default=.2)
def train_cell_classifier(input_dir,log_dir, batch_size, epochs, img_height, img_width, val_split):
    # data generation
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=val_split
    )

    # create training/val sets
    train_generator = train_datagen.flow_from_directory(
        input_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='training')
    validation_generator = train_datagen.flow_from_directory(
        input_dir,
        target_size=(img_height, img_width),
        batch_size=batch_size,
        class_mode='categorical',
        subset='validation')

    # train model
    model = get_model(img_width, img_height)
    history = model.fit_generator(
        train_generator,
        steps_per_epoch = train_generator.samples // batch_size,
        validation_data = validation_generator, 
        validation_steps = validation_generator.samples // batch_size,
        epochs = epochs,
        callbacks=get_callbacks(log_dir)
    )


if __name__ == '__main__':
    train_cell_classifier()

