""" 
Last updated: 2/14/16 14:00

This code file analyzes a DNA sequence and outputs snippets of DNA that are likely to be protein-coding genes

@author: Emma Price
"""

import random
import math
from PIL import Image

"""prod(a,b) = a*b
avg(a,b) = .5(a+b)
cos_pi(a) = cos(pi*a)
sin_pi = sin(pi*a)
x(a,b) = a
y(a,b) = b
square(a) = a^2
square_root_abs_val(a) = math.sqrt(abs(a))"""

functions = ['sin_pi', 'cos_pi', 'square', 'square_root_abs_val', 'prod', 'avg', 'x', 'y']


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    random_function = random.randint(0,7)
    if max_depth == 0:
        f = random.randint(0,2)
        if f == 0:
            return ['x']
        elif f == 1:
            return ['y']
        elif f == 2:
            return ['t']
    if min_depth <= 0:
        f = random.randint(0,2)
        if f == 0:
            return ['x']
        elif f == 1:
            return ['y']
        elif f == 2:
            return ['t']
    if random_function <= 3:
        return [functions[random_function], build_random_function(min_depth - 1, max_depth - 1)]
    else:
        return [functions[random_function], build_random_function(min_depth - 1, max_depth - 1), build_random_function(min_depth - 1, max_depth - 1)]

def evaluate_random_function(f, x, y, t):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
    """
    if len(f) == 1:
        if f == ['x']:
            return float(x)
        elif f == ['y']:
            return float(y)
        elif f == ['t']:
            return float(t)
    elif f[0] == functions[0]:
        return math.sin(math.pi*evaluate_random_function(f[1], x, y, t))
    elif f[0] == functions[1]:
        return math.cos(math.pi*evaluate_random_function(f[1], x, y, t))
    elif f[0] == functions[2]:
        return (evaluate_random_function(f[1], x, y, t))**2
    elif f[0] == functions[3]:
        return math.sqrt(abs(evaluate_random_function(f[1], x, y, t)))
    elif f[0] == functions[4]:
        return evaluate_random_function(f[1], x, y, t)*evaluate_random_function(f[2], x, y, t)
    elif f[0] == functions[5]:
        return .5*(evaluate_random_function(f[1], x, y, t)+evaluate_random_function(f[2], x, y, t))
    elif f[0] == functions[6]:
        return evaluate_random_function(f[1], x, y, t)
    elif f[0] == functions[7]:
        return evaluate_random_function(f[2], x, y, t)

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_interval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    in_range = input_interval_end - input_interval_start
    out_range = output_interval_end - output_interval_start
    scaled_value = ((float(val - input_interval_start)/in_range)*out_range) + output_interval_start
    return scaled_value


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)
"""

def generate_art(filename, frames = 50, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    for frame in range(frames):
        t = remap_interval(frame, 0, frames, -1, 1)
        # Create image and loop over all pixels
        im = Image.new("RGB", (x_size, y_size))
        pixels = im.load()
        for i in range(x_size):
            for j in range(y_size):
                x = remap_interval(i, 0, x_size, -1, 1)
                y = remap_interval(j, 0, y_size, -1, 1)
                pixels[i, j] = (
                        color_map(evaluate_random_function(red_function, x, y, t)),
                        color_map(evaluate_random_function(green_function, x, y, t)),
                        color_map(evaluate_random_function(blue_function, x, y, t))
                        )
        im.save(filename + str(frame).zfill(3) + '.png')


if __name__ == '__main__':
    #import doctest
    #doctest.testmod()

    generate_art("frame")