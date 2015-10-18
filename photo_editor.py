# SYSC 1005 A Fall 2013 Lab 7
# Revised: October 22, 2013.

import sys  # get_image calls exit
import filters
import convolution_filter
import gui
import thread
import datetime
from Cimpl import *

start_time = datetime.datetime.now().time()
# filename = os.path.splitext(f)[0]

def get_image():
    """
    Interactively select an image file and return a Cimpl Image object
    containing the image loaded from the file.
    """

    # Pop up a dialogue box to select a file
    file = choose_file()

    # Exit the program if the Cancel button is clicked.
    if file == "":
        sys.exit("File Open cancelled, exiting program")

    # Open the file containing the image and load it
    img = load_image(file)

    return img

def apply_filters(img):
    dark_ratio = 0.4
    light_ratio = 0.55
    # background = load_image(gui.pathGUIBackground1)
    # dark_background = load_image(gui.pathGUIBackground2)
    background = load_image("background.bmp")
    dark_background = load_image("dark_background.bmp")
    modified = filters.backgound_detect(img, dark_background, dark_ratio)
    image = filters.backgound_detect(modified, dark_background, light_ratio)
    dest = convolution_filter.convolution_filter(image, "blur")
    dest = convolution_filter.convolution_filter(dest, "blur")
    dest1 = filters.black_and_white(dest, 25)
    # save_as(dest1, "photos/tmp1.bmp")
    return dest1

def check_holes(img):
    sequence = (0, 2, 4, 2, 0)
    index = 0
    for y in range(get_height(img)):
        color_change = 0
        for x in range(get_width(img) - 1):
            color = get_color(img, x, y)
            color_right = get_color(img, x+1, y)
            if color != color_right:
                color_change += 1
        # If the color_change is as expected continue
        if color_change == sequence[index]:
            continue
        # If you're at the end of the sequence, and there's another color
        # change then quit
        elif index + 1 == len(sequence):
            if color_change > 0:
                return False
        # If there's a differece that matches the next part in the sequence
        # move the index along
        elif color_change == sequence[index+1]:
            index += 1
            continue
        else:
            return False
    # You made it! The sequence is complete!
    return True

def _find_edge(img, direction):
    if direction < 0:
        start = get_width(img) - 1
        end = 0
        step = -1
    else:
        start = 0
        end = get_width(img) - 1
        step = 1

    for x in range(start, end, step):
        for y in range(get_height(img)):
            color = get_color(img, x, y)
            color_side = get_color(img, x+step, y)
            if color != color_side:
                return x
    return -1

def _count_col(img, x):
    count = 0
    switch = False
    white = create_color(255, 255, 255)
    for y in range(get_height(img)):
        if get_color(img, x, y) == white:
            count += 1
    return count


def size_irregularity(img, threshold):
    left = _find_edge(img, 1)
    right = _find_edge(img, -1)
    while(right - left > 0):
        left_count = _count_col(img, left)
        right_count = _count_col(img, right)
        if abs(left_count - right_count) > threshold:
            return False
        left += 1
        right -= 1
    return True


def process_image(img):
    modified = apply_filters(img)
    hole_check = check_holes(modified)
    size_check = size_irregularity(modified, 7)
    print("Hole: " + str(hole_check) + "\nSize: " + str(size_check) + "\nFinal: " + str(size_check and hole_check) + "\n")
    return size_check and hole_check

def execute(fileQueue, path):
    print("Hello")
    print(fileQueue)
    for img in fileQueue:
        valid_img = process_image(load_image(path + "/" + img))
        print("Image: " + img + " is " + str(valid_img))




if __name__ == "__main__":

    background = load_image("background.bmp")
    dark_background = load_image("dark_background.bmp")

    command = ""
    image = ""
    combos = [
        (0.15, 0.7),
        (0.15, 0.7),
        (0.2, 0.7),
        (0.25, 0.65),
        (0.3, 0.6),
        (0.35, 0.55),
        (0.4, 0.5),
        (0.4, 0.55),
        (0.45, 0.45),
        (0.45, 0.5),
        (0.5, 0.45),
        (0.55, 0.35),
        (0.55, 0.4)
    ]

    good_combos = [
        (0.4, 0.5),
        (0.4, 0.55)
    ]

    images = ["photos/th_DSC_0200.bmp", "photos/th_DSC_0384.bmp", "photos/th_DSC_0391.bmp", "photos/edgehole.bmp"]

    # img = load_image(images[1])
    # image = apply_filters(img)
    #
    # left = _find_edge(image, 1)
    # right = _find_edge(image, -1)
    #
    # for y in range(get_height(img)):
    #     set_color(image, left, y, create_color(255, 0, 0))
    #     set_color(image, right, y, create_color(255, 0, 0))

    # print left, right

    # show(image)



    for img in images:
        process_image(load_image(img))
