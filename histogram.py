import cv2
import matplotlib.pyplot as plt

from matplotlib import use

use('TkAgg')


def plot_histogram(img, name="image"):
    # Calculate histogram
    bit_depth = img.dtype.itemsize * 8
    img_gray_level_res = 2**bit_depth
    hist = cv2.calcHist([img], [0], None, [img_gray_level_res], [0, img_gray_level_res])

    # Plot histogram
    plt.plot(hist)
    plt.title(f"Histogram of {name}")
    plt.xlabel('Intensity')
    plt.ylabel('Frequency')
    plt.show()


if __name__ == '__main__':
    image_path = './data/input/lena.png'
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    plot_histogram(image)
