from typing import Callable, Tuple
from math import log

from PIL import Image


def normalize(pixel: int):
    """ Maps the range of 0-255 into 0-1. """
    return pixel / 255


def negative(pixel: int):
    return 255 - pixel


def pixel_log(pixel: int, s: float = (256 / 8), base: int = 10):
    return int(s * log(pixel + 1, base))


def pixel_power(pixel: int, c: int = 1, y: float = 3.0, e: float = 0):
    normalized_pixel = normalize(pixel)
    output_pixel = c * (normalized_pixel + e) ** y
    return int(output_pixel * 255)


def apply(gray_image: Image, f: Callable, params: Tuple = None) -> Image:
    output_image = Image.new('L', gray_image.size)
    width, height = gray_image.size
    for y in range(height):
        for x in range(width):
            pixel_value = gray_image.getpixel((x, y))

            # TODO adding params
            new_pixel_value = f(pixel_value)
            output_image.putpixel((x, y), new_pixel_value)

    return output_image


functions = {
    'negation': negative,
    'log': pixel_log,
    'power': pixel_power,
}

if __name__ == '__main__':
    input_image = Image.open('./data/input/lena.png')
    gray_image = input_image.convert('L')

    for func_name, func in functions.items():
        output_image = apply(gray_image, func)

        output_image.show()
        output_image.save(f'./data/output/{func_name}.png')
