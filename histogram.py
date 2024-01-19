import cv2
import numpy as np
import matplotlib.pyplot as plt

from matplotlib import use

use('TkAgg')


def plot_histogram(img, name="image"):
    # Calculate histogram
    bit_depth = img.dtype.itemsize * 8
    img_gray_level_res = 2 ** bit_depth
    hist = cv2.calcHist([img], [0], None, [img_gray_level_res], [0, img_gray_level_res])

    # Plot histogram
    plt.plot(hist)
    plt.title(f"Histogram of {name}")
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.show()


def modify_bits(img, bit_changes):
    """
    The image bits will be changed based on the pattern in bit_changes.
    For each bit of all pixels in the image, if the corresponding value
    in the bit_changes list is -1, the bit will be left unchanged, if
    it is 0, the bit will be set to 0 and if it is 1, the bit will be
    set to 1.
    """
    bit_depth = len(bit_changes)

    modified_img = np.copy(img)
    for i, change in enumerate(bit_changes):
        if change == 0:
            modified_img = modified_img & ~(1 << (bit_depth - i - 1))
        elif change == 1:
            modified_img = modified_img | (1 << (bit_depth - i - 1))

    modified_img = modified_img.astype(np.uint8)

    return modified_img


if __name__ == '__main__':
    image_path = './data/input/lena.png'

    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    plot_histogram(image, "original Lena")

    modified_image = modify_bits(image, [-1, -1, -1, -1, 0, 0, 0, 0])
    plot_histogram(modified_image, "modified Lena")
