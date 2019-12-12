from IPython.display import display
from PIL import Image
from matplotlib import pyplot as plt


def show_image(img):
    """ Display image in jupyter noteobok
    Args:
      img (np.array): The image
    """
    display(Image.fromarray(img))


def plot_datapoint(dp):
    """ plot a datapoint image and mask side by side
    Args:
      dp (Datapoint): datapoint
    """
    plt.figure(figsize=(15,15))
    plt.subplot(121)
    plt.imshow(dp.img)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(dp.mask)
    plt.axis('off')
    plt.show()

def plot_img_and_mask(img, mask):
    """ plot image next to mask
    Args:
      img (np.array): image
      mask (np.array): mask
    """
    plt.figure(figsize=(15,15))
    plt.subplot(121)
    plt.imshow(img)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(mask)
    plt.axis('off')
    plt.show()