""" SYSC 1005 Fall 2013 - Matrix convolution and image processing.

A convolution kernel is a square matrix; for example:

    |c00  c01  c02|
C = |c10  c11  c12|
    |c20  c21  c22|

In the example, the kernel is a 3-by-3 matrix, but be larger (e.g., 5-by-5,
7-by-7, etc.)

The element at the center of the matrix is known as the anchor point.

The convolution kernel is placed over a square region in an image; for example:

  (r1, g1, b1)  (r2, g2, b2)  (r3, g3, b3)
  (r4, g4, b4)  (r5, g5, b5)  (r6, g6, b6)
  (r7, g7, b7)  (r8, g8, b8)  (r9, g9, b9)

(r1, b1, g1) represent the red, green and blue components of the pixel in
the upper-left corner; (r2, g2, b2) represent the red, green and blue
components of the pixel to the right of it, etc.

Note that the kernel's anchor point will be above the pixel in the center of
the region; i.e., (r5, g5, b5).

Each element in the convolution kernel is multiplied by the red component of
the pixel beneath it, and these products are added together. This sum is
typically divided by the number of elements in the kernel. This value will be
used as the red component for the new colour for the pixel under the anchor
point.

To summarize:

new_red = (c00 * r1 + c01 * r2 + c02 * r3 +
           c10 * r4 + c11 * r5 + c12 * r6 +
           c20 * r7 + c21 * r8 + c22 * r9) / 9

The convolution is repeated for the blue and green components in the region.

After the new red, green and blue components have been calculated, the
pixel's colour is set to the new colour.

We then shift the convolution kernel one pixel to the right, and repeat the
convolution. After processing one row, we shift the kernel down to the next row.
"""

from Cimpl import *

def convolution_filter(img, manipulation):
    """ Return a new image created from the picture bound to img,
    using the specified 3-by-3 convolution kernel.
    """

    table = build_kernel_table()

    # takes the kernel that was passed in to the function from the dictionary
    # of kernels
    kernel = table[manipulation]


    # Create a blank image that's the same size as the original image.
    # The filter modifies this image, so that the convolution always uses
    # pixels from the original image, instead of pixels that have been
    # been modified.

    dest = create_image(get_width(img), get_height(img))

    # To keep things simple, don't do the convolution on the pixels along
    # the images edges.

    for y in range(1, get_height(img)-1):
        for x in range(1, get_width(img)-1):

            # We could use a nested for loop to traverse the convolution
            # kernel, but instead, we use a technique known as "unrolling the
            # loops".

            # The kernel's anchor point is situated over the pixel @ (x, y).
            # Note: kernel elements are indexed by kernel[row][col]

            sum_red = 0
            sum_green = 0
            sum_blue = 0
            divisor = 0

            # NW (north west corner)
            r, g, b = get_color(img, x-1, y-1)
            sum_red = sum_red + r * kernel[0][0]
            sum_green = sum_green + g * kernel[0][0]
            sum_blue = sum_blue + b * kernel[0][0]
            divisor = divisor + kernel[0][0]

            # N
            r, g, b = get_color(img, x, y-1)
            sum_red = sum_red + r * kernel[0][1]
            sum_green = sum_green + g * kernel[0][1]
            sum_blue = sum_blue + b * kernel[0][1]
            divisor = divisor + kernel[0][1]

            # NE
            r, g, b = get_color(img, x+1, y-1)
            sum_red = sum_red + r * kernel[0][2]
            sum_green = sum_green + g * kernel[0][2]
            sum_blue = sum_blue + b * kernel[0][2]
            divisor = divisor + kernel[0][2]

            # W
            r, g, b = get_color(img, x-1, y)
            sum_red = sum_red + r * kernel[1][0]
            sum_green = sum_green + g * kernel[1][0]
            sum_blue = sum_blue + b * kernel[1][0]
            divisor = divisor + kernel[1][0]

            # center
            r, g, b = get_color(img, x, y)
            sum_red = sum_red + r * kernel[1][1]
            sum_green = sum_green + g * kernel[1][1]
            sum_blue = sum_blue + b * kernel[1][1]
            divisor = divisor + kernel[1][1]

            # E
            r, g, b = get_color(img, x+1, y)
            sum_red = sum_red + r * kernel[1][2]
            sum_green = sum_green + g * kernel[1][2]
            sum_blue = sum_blue + b * kernel[1][2]
            divisor = divisor + kernel[1][2]

            # SW
            r, g, b = get_color(img, x-1, y+1)
            sum_red = sum_red + r * kernel[2][0]
            sum_green = sum_green + g * kernel[2][0]
            sum_blue = sum_blue + b * kernel[2][0]
            divisor = divisor + kernel[2][0]

            # S
            r, g, b = get_color(img, x, y+1)
            sum_red = sum_red + r * kernel[2][1]
            sum_green = sum_green + g * kernel[2][1]
            sum_blue = sum_blue + b * kernel[2][1]
            divisor = divisor + kernel[2][1]

            # SE
            r, g, b = get_color(img, x+1, y+1)
            sum_red = sum_red + r * kernel[2][2]
            sum_green = sum_green + g * kernel[2][2]
            sum_blue = sum_blue + b * kernel[2][2]
            divisor = divisor + kernel[2][2]

            # To normalize the new component values, divide them by the sum
            # of the values in the kernel. If the divisor is 0, divide by 1.
            if divisor == 0:
                divisor = 1

            new_red = sum_red / divisor

            # Cimpl modifies components so that they lie between 0 and 255,
            # so we don't really need the next statement.
            new_red = min(max(new_red, 0), 255)

            new_green = sum_green / divisor
            new_green = min(max(new_green, 0), 255)

            new_blue = sum_blue / divisor
            new_blue = min(max(new_blue, 0), 255)

            col = create_color(new_red, new_green, new_blue)
            set_color(dest, x, y, col)

    # We've processed all the pixels except those on the edges.
    # Make those pixels black.

    black = create_color(0, 0, 0)

    bottom_row = get_height(img) - 1
    for x in range(get_width(img)):
        set_color(dest, x, 0, black)
        set_color(dest, x, bottom_row, black)

    right_column = get_width(img) - 1
    for y in range(get_height(img)):
        set_color(dest, 0, y, black)
        set_color(dest, right_column, y, black)

    return dest

blur_kernel = (
    (1, 1, 1),
    (1, 1, 1),
    (1, 1, 1)
)

sharpen_kernel = (
    (0,  -3,  0),
    (-3, 21, -3),
    (0,  -3,  0)
)

emboss_kernel = (
    (-18, -9, 0),
    ( -9, 9,  9),
    (  0, 9, 18)
)

edge_detect_1_kernel = (
    (0,  9,  0),
    (9, -36, 9),
    (0,  9,  0)
)

edge_detect_2_kernel = (
    (-9,  -9, -9),
    (-9, -36, -9),
    (-9,  -9, -9)
)

def test_convolution_filter():
    img = load_image("great_big_c.jpg")
    show(img)
    new_image = convolution_filter(img, raw_input("Enter a kernel \n:"))
    show(new_image)
    # save_as(new_image, "great_big_c_convolution_blur.jpg")

def build_kernel_table():
    """
    Builds a dictionary containing all the convolution kernels
    """
    kernel_table = {}

    kernel_table["blur"] = blur_kernel
    kernel_table["sharpen"] = sharpen_kernel
    kernel_table["emboss"] = emboss_kernel
    kernel_table["edge detect 1"] = edge_detect_1_kernel
    kernel_table["edge detect 2"] = edge_detect_2_kernel

    return kernel_table




def build_concordance(filename):
    """
    Prints a table of the unique words a what lines they occur on at least once
    """

    # defines the dictionary line number and opens the text file for reading
    concordance = {}
    line_number = 1
    textfile = open(filename, "r")

    # get each line in the file
    for line in textfile:
        # turns the line into a list of all the words
        words = line.split()

        # get each word in the list
        for word in words:
            # remove any punctuation
            w = word.strip(".!?,;:()\"'-").lower()

            # make sure the word isn't blank
            if w != "":
                # Make sure the key exsists or creates it
                if w not in concordance:
                    concordance[w] = set()

                # adds the line number to the dictionary
                concordance.get(w).add(line_number)

        line_number += 1

    # create and sort a list of the keys
    word_list = concordance.keys()
    word_list.sort()

    # output the results
    for item in word_list:
        print item + " : " + str(list(concordance[item]))



if __name__ == "__main__":
    # Automatically binds kernels to the dictionary created in the function
    # When the program is run

    table = build_kernel_table()
