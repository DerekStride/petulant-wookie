from Cimpl import *

def black_and_white(img, threshold):
    """
    Convert the specified image to a black-and-white (two-tone) image.
    """

    # Brightness levels range from 0 to 255.
    # Change the colour of each pixel to black or white, depending on whether
    # its brightness is in the lower or upper half of this range.

    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)

    dest = create_image(get_width(img), get_height(img))

    for x, y, col in img:
        red, green, blue = col

        brightness = (red + green + blue) / 3
        if brightness < threshold:
            set_color(dest, x, y, black)
        else:     # brightness is between 128 and 255, inclusive
            set_color(dest, x, y, white)

    return dest

def backgound_detect(img, backgound, ratio):
    dest = create_image(get_width(img), get_height(img))
    for x, y, col in img:
        r, g, b = col
        br, bg, bb = get_color(backgound, x, y)
        set_color(dest, x, y, create_color(r - int((br*ratio)), g - int((bg*ratio)), b - int((bb*ratio))))
    return dest

def remove_noise(img, dimensions):
    """
    Convert the specified image to a black-and-white (two-tone) image.
    """

    if (dimensions % 2) == 0:
        dim = dimensions + 1
    else:
        dim = dimensions

    # Brightness levels range from 0 to 255.
    # Change the colour of each pixel to black or white, depending on whether
    # its brightness is in the lower or upper half of this range.

    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)

    dest = create_image(get_width(img), get_height(img))

    for y in range(dim / 2, get_height(img)-(dim / 2)):
        for x in range(dim / 2, get_width(img)-(dim / 2)):
            sum_brightness = 0
            for i in range(1-(dim / 2), dim / 2):
                for j in range(1-(dim / 2), dim / 2):
                    r, g, b = get_color(img, x+i, y+j)
                    if r < 20 and g < 20 and b < 20:
                        sum_brightness += 1
            if sum_brightness < dim / 3:
                set_color(dest, x, y, white)
            else:
                set_color(dest, x, y, black)

    return dest

def _adjust_component(amount):

    if amount >= 0 and amount <= 63:
        a = 31
    elif amount >= 64 and amount <= 127:
        a = 95
    elif amount >= 128 and amount <= 191:
        a = 159
    elif amount >= 192 and amount <= 255:
        a = 223

    return a


def swap_black_white(img):
    """
    Make all black pixels white and all white pixels black, leaving all
    other pixels unchanged.
    """

    black = create_color(0, 0, 0)
    white = create_color(255, 255, 255)

    for x, y, col in img:

        # Check if the pixel's colour is black; i.e., all three of its
        # components are 0.
        if col == black:

            # The pixel is black, make it white.
            set_color(img, x, y, white)

        # Check if the pixel's colour is white; i.e., all three of its
        # components are 255.
        elif col == white:

            # The pixel is white, make it black.
            set_color(img, x, y, black)


def detect_edges(img, threshold):

    for x in range(get_width(img)):
        for y in range(get_height(img) - 1):
            red, green, blue = get_color(img, x, y)
            red_bottom, green_bottom, blue_bottom = get_color(img, x, y+1)

            contrast = abs(((red + green + blue) / 3) -
                           ((red_bottom +  green_bottom + blue_bottom) / 3))

            if contrast > threshold:
                set_color(img, x, y, create_color(0, 0, 0))
            else:
                set_color(img, x, y, create_color(255, 255, 255))

def detect_edges_better(img, threshold):

    dest = create_image(get_width(img), get_height(img))

    for x in range(get_width(img) - 1):
        for y in range(get_height(img) - 1):
            red, green, blue = get_color(img, x, y)
            red_bottom, green_bottom, blue_bottom = get_color(img, x, y+1)
            red_right, green_right, blue_right = get_color(img, x+1, y)

            contrast_bottom = abs(((red + green + blue) / 3) -
                           ((red_bottom +  green_bottom + blue_bottom) / 3))

            contrast_right = abs(((red + green + blue) / 3) -
                                 ((red_right +  green_right + blue_right) / 3))

            if contrast_bottom > threshold or contrast_right > threshold:
                set_color(dest, x, y, create_color(0, 0, 0))
            else:
                set_color(dest, x, y, create_color(255, 255, 255))

    return dest
