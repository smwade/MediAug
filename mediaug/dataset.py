import os
from os.path import join
import numpy as np
from PIL import Image
import cv2
from tqdm import tqdm
from random import choice
from mediaug.image_utils import read_png, save_img
from mediaug.download import get_data_cache
from random import randint
# TODO: Documentation

class DataPoint:

    def __init__(self, img_path, mask_path, _class, _id=None):
        self.img_path = img_path
        self.mask_path = mask_path
        self._class = _class
        if _id is None:
            self.id = img_path.split('.')[0]

    @property
    def img(self):
        return read_png(self.img_path)

    @property
    def pil_img(self):
        return Image.fromarray(read_png(self.img_path))

    @property
    def mask(self):
        return read_png(self.mask_path)

    @property
    def pil_mask(self):
        return Image.fromarray(read_png(self.mask_path))

    def __repr__(self):
        return f'<img_path: {self.img_path}>\n<mask_path: {self.mask_path}>'


class Dataset:
    """Dataset object for managing image augmentation

    Attributes:
        data_path (str): Path to the data directory root
    """

    def __init__(self, data_path=None, classes=None):
        self.data_path = data_path
        if not os.path.exists(data_path) and classes is not None:
            self._create_empty_dataset(classes)
        if not os.path.exists(data_path) and classes is None:
            raise ValueError('No data in path or classes.')
        self._parse(data_path)
    
    def _parse(self, data_path):
        self.data = {}
        categories =  [x for x in os.listdir(data_path) if not x.startswith('.')]
        self.data = {key:[] for key in categories}
        for c in categories:
            cur_dir = join(data_path, c)
            for base_name in os.listdir(join(cur_dir, 'image')):
                name = base_name.split('.')[0]
                dp = DataPoint(join(cur_dir, 'image', base_name),
                                join(cur_dir, 'mask', base_name), c, name)
                self.data[c].append(dp)

    def _create_empty_dataset(self, classes):
        os.mkdir(self.data_path)
        self.data = {key:[] for key in classes}
        for _class in classes:
            os.mkdir(join(self.data_path, _class))
            os.mkdir(join(self.data_path, _class, 'image'))
            os.mkdir(join(self.data_path, _class, 'mask'))


    def add_datapoint(self, dp):
        self.data[dp._class].append(dp)

    
    def random_sample(self):
        _class = choice(self.classes)
        return choice(self.data[_class])


    def add_data(self, img, mask, _class, name):
        img_path = save_img(img, join(self.data_path, _class, 'image', f'{name}.png'))
        mask_path = save_img(mask, join(self.data_path, _class, 'mask', f'{name}.png'))
        self.data[_class].append(DataPoint(img_path, mask_path, _class))


    def get_data(self, _id):
        """ Gets a datapoint by id """
        raise NotImplementedError 


    def get_array(self, num_samples=-1, n_last=False, greyscale=False):
        """ This is of the form:
        (x_train, y_train), (x_test, y_test)
        ex: (num_samples, 32, 32, 3)
        (num_samples, 1)
        """
        images = []
        masks = []
        for c in tqdm(self.classes):
            for dp in tqdm(self.data[c][:num_samples]):
                if greyscale == True:
                    images.append(cv2.cvtColor(dp.img, cv2.COLOR_BGR2GRAY))
                    masks.append(cv2.cvtColor(dp.mask, cv2.COLOR_BGR2GRAY))
                else:
                    images.append(dp.img)
                    masks.append(dp.mask)
        images = np.array(images)
        masks = np.array(masks)
        if n_last:
            images = np.moveaxis(images, 0, -1)
            masks = np.moveaxis(masks, 0, -1)
        return images, masks
    

    @property
    def classes(self):
        return list(self.data.keys())

    @property
    def size(self):
        size = 0
        for c in self.classes:
            size += len(self.data[c])
        return size

    def __getitem__(self, arg):
        return self.data[arg]
