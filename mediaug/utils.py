import os
import pathlib


def convert_array_to_poly(arr):
    return arr.flatten().tolist()


def create_dirs(base_path, dir_list=[]):
    """create dirs under the base path"""
    pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)
    for new_dir in dir_list:
        pathlib.Path(os.path.join(base_path, new_dir)).mkdir(parents=True)
