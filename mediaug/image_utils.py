import cv2
import numpy as np
from PIL import Image, ImageSequence, ImageDraw

from mediaug.utils import convert_array_to_poly
from mediaug.variables import COLOR_CYTO_MASK, COLOR_NUC_MASK


def read_tiff(path):
    """ Reads an image with a .tff extension, used in the Unet example
    Returns np.array
    """
    return np.array([np.array(p) for p in ImageSequence.Iterator(Image.open(path))])


def read_bmp(img_path):
    """ Reads an image with a .bmp extension Returns np.array """
    return cv2.imread(img_path)


def read_png(img_path):
    """ Reads an image with a .png extension. Returns np.array """
    return cv2.imread(img_path)


def read_img(img_path):
    """ Reads an image
    Args:
      img_path (str): The image path (png, jpg, or bmp)
    Returns:
      img (np.array): The image array
    """
    return cv2.imread(img_path)


def read_dat_file(path):
    """ Reads an .dat file with polygons, the data from SIPaKMeD
    Args:
      path (str): The path to polygon .dat file
    Returns:
      poly_array (np.array): Array of (x, y) points for the polygon
    """
    return np.loadtxt(path, delimiter=',')


def save_img(img, path):
    """ Save an img to path """
    cv2.imwrite(path, img)
    return path


def rotate(image, angle):
    """ Rotates an image by angle, increases the dimension as necessary """
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
 
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])
 
    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))
 
    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY
    return cv2.warpAffine(image, M, (nW, nH))


def soften_mask(mask, amount=5):
    """ Softens the edges of a mask by dialating it and then Gaussian blurring"""
    kernel = np.ones((5,5), np.uint8) 
    mask_dilation = cv2.dilate(mask, kernel, iterations=amount)
    blur = cv2.GaussianBlur(mask_dilation, (5,5), 0)
    return cv2.max(mask, blur)


def get_blank_mask(img, greyscale=False):
    if greyscale:
        return np.zeros(img.shape[:2], np.uint8)
    return np.zeros(img.shape,np.uint8)


def image_on_image_alpha(bg, fg, fg_mask, center):
    """ Place an image on an image with a backround mask
    Blends using the alpha
    """
    alpha = np.zeros(bg.shape[:2], dtype=np.uint8)
    alpha = place_img_on_img(alpha, fg_mask, center)
    cell_img = place_img_on_img(bg.copy(), fg, center)

    alpha = alpha.astype(float)/255
    alpha = np.repeat(alpha[:, :, np.newaxis], 3, axis=2)

    fg = cv2.multiply(alpha, cell_img.astype(float))
    bg = cv2.multiply(1.0 - alpha, bg.astype(float))

    return cv2.add(fg, bg).astype(np.uint8)


def place_img_on_img(bg, fg, center):
    """
    bg (np.array): backgourn image
    fg (np.array): foreground image
    center (x, y): where to put CENTER of fg image
    """
    ch, cw = center
    fg_h, fg_w = fg.shape[:2]
    bg_h, bg_w = bg.shape[:2]

    # check offset in bg
    if cw < 0 or cw > bg_w or ch < 0 or ch > bg_h:
        raise ValueError('Center not in backgound bounds')

    # find top left corner of fg in respect to bg
    left_w = cw - (fg_w // 2)
    left_h = ch - (fg_h // 2)
    end_w = left_w + fg_w
    end_h = left_h + fg_h

    # for if goes over bg boundries
    abs_left_w = max(left_w, 0)
    abs_left_h = max(left_h, 0)
    abs_end_w = min(end_w, bg_w)
    abs_end_h = min(end_h, bg_h)
    
    # for fg boundries
    fg_left_w = abs(min(left_w, 0))
    fg_left_h = abs(min(left_h, 0))
    diff_w = bg_w - end_w
    diff_h = bg_h - end_h
    if diff_w >= 0:
        fg_end_w = fg_w
    else:
        fg_end_w = diff_w
    if diff_h >= 0:
        fg_end_h = fg_h
    else:
        fg_end_h = diff_h

    ans = np.copy(bg)
    ans[abs_left_h:abs_end_h, abs_left_w:abs_end_w] = fg[fg_left_h:fg_end_h, fg_left_w:fg_end_w]
    return ans


def generate_cell_mask(img, cyto, nuc):
    """ Generate a mask for a labelled cell """
    w, h, _ = img.shape
    mask = Image.new(mode="RGB", size=(h, w))
    ImageDraw.Draw(mask).polygon(convert_array_to_poly(cyto), outline=None, fill=COLOR_CYTO_MASK)
    ImageDraw.Draw(mask).polygon(convert_array_to_poly(nuc), outline=None, fill=COLOR_NUC_MASK)
    return np.array(mask)


def generate_full_mask(img, cytos, nucs):
    """ Generates a mask for any number of cells on a slide """
    h, w, _ = img.shape
    mask = Image.new(mode="RGB", size=(w, h))
    for poly in cytos:
        ImageDraw.Draw(mask).polygon(convert_array_to_poly(poly), outline=None, fill=COLOR_CYTO_MASK)
    for poly in nucs:
        ImageDraw.Draw(mask).polygon(convert_array_to_poly(poly), outline=None, fill=COLOR_NUC_MASK)
    return np.array(mask)


def is_greyscale(img):
    """ Checks if an image array is greyscale. Returns bool. """
    if len(img.shape) < 3:
        return True
    return False
