import cv2
import numpy as np


def make_pix2pix_format(target_image, input_image, size=256):    
    """ place the 2 images together for the format for pix2pix. That is
    both images concatinated horizontally
    Args:
      target_image (np.array): The target image for Pix2Pix
      input_image (np.array): The given image for Pix2Pix input
      size (int): The dimension of both sides of the images
    Returns:
      new_img (np.array): An image of dimension [size, 2*size]
    """
    target_image = cv2.resize(target_image, (size, size))
    imput_image = cv2.resize(input_image, (size, size))
    h, w = size, size*2
    new_img = np.zeros((h, w, 3), np.uint8)
    new_img[:,0:w//2] = target_image
    new_img[:,w//2:] = imput_image
    return new_img
