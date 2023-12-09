from typing import Callable, Tuple
from math import log

from PIL import Image


def normalize(pixel: int):
    """ Maps the range of 0-255 into 0-1 """
    return pixel / 255


def negative(pixel: int):
    return 255 - pixel


def pixel_log(pixel: int, s: float = (256 / 8), base: int = 10):
    return int(s * log(pixel + 1, base))


def pixel_power(pixel: int, c: int = 1, y: float = 3.0, e: float = 0):
    normalized_pixel = normalize(pixel)
    output_pixel = c * (normalized_pixel + e) ** y
    return int(output_pixel * 255)


def linear_function(
        x1: float,
        y1: float,
        x2: float,
        y2: float,
):
    """ Returns the formula of the line passing (x1, y1) and (x2, y2) """

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - slope * x1

    def linear_func(value: float):
        return slope + value + intercept

    return linear_func


def piecewise_linear_transformation(
        pixel: int,
        r1: float,
        s1: float,
        r2: float,
        s2: float,
        max_range: float = 255.0
):
    result = 0

    if pixel < r1:
        result = linear_function(0, 0, r1, s1)(pixel)
    elif r1 <= pixel <= r2:
        result = linear_function(r1, s1, r2, s2)(pixel)
    elif pixel > r2:
        result = linear_function(r2, s2, max_range, max_range)(pixel)

    return int(result)


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


def apply_with_params(
        gray_image: Image,
        f: Callable,
        params: Tuple = None
) -> Image:
    output_image = Image.new('L', gray_image.size)
    width, height = gray_image.size
    for y in range(height):
        for x in range(width):
            pixel_value = gray_image.getpixel((x, y))

            new_pixel_value = f(pixel_value, *params)
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

    # for func_name, func in functions.items():
    #     output_image = apply(gray_image, func)
    #
    #     output_image.show()
    #     output_image.save(f'./data/output/{func_name}.png')

    pixels = list(gray_image.getdata())

    # Find min and max pixel values
    r_min = min(pixels)
    r_max = max(pixels)

    output_image = apply_with_params(
        gray_image,
        piecewise_linear_transformation,
        (r_min, 0, r_max, 255)
    )

    output_image.show()
    output_image.save('./data/output/PLT-rmin-0-rmax-255.png')
