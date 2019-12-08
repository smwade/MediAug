from IPython.display import display
from PIL import Image
from matplotlib import pyplot as plt

def show_image(img):
    display(Image.fromarray(img))

def plot_segment(img, segments):
    plt.figure(figsize=(15,15))
    plt.imshow(img)
    for poly in segments:
        plt.fill(poly[:, 0], poly[:, 1], alpha=.3, facecolor='g', edgecolor='black', linewidth=5)

    plt.axis('off')
    plt.show()

def plot_datapoint(dp):
    """ plot the datapoint image next to the mask """
    plt.figure(figsize=(15,15))
    plt.subplot(121)
    plt.imshow(dp.img)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(dp.mask)
    plt.axis('off')
    plt.show()

def plot_img_and_mask(img, mask):
    """ plot the datapoint image next to the mask """
    plt.figure(figsize=(15,15))
    plt.subplot(121)
    plt.imshow(img)
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(mask)
    plt.axis('off')
    plt.show()