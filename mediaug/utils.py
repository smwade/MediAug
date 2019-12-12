import os
import pathlib


def convert_array_to_poly(arr):
    """ Convert array of (x,y) coordinates, nx2, to
    a Polygon object for Polygon package
    Args:
      arr (np.array): Array of the polygon
    Returns:
      asn (list): The polygon in a list
    """
    return arr.flatten().tolist()


def create_dirs(base_path, dir_list=[]):
    """create dirs under the base path
    Args:
      base_path (str): The base of the directory paths
      dir_list (list[str]): List of paths relative to the base dir
    """
    pathlib.Path(base_path).mkdir(parents=True, exist_ok=True)
    for new_dir in dir_list:
        pathlib.Path(os.path.join(base_path, new_dir)).mkdir(parents=True)
