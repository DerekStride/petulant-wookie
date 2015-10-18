# SYSC 1005 A Fall 2013 Lab 7
# Revised: October 22, 2013.

import sys  # get_image calls exit
import filters
import convolution_filter
from Cimpl import *

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


if __name__ == "__main__":

    background = load_image("photos/background.bmp")
    dark_background = load_image("photos/dark_background.bmp")

    command = ""
    image = ""
    dark_ratio = 0
    light_ratio = 0
    image = get_image()

    while command != "Q":

        while (dark_ratio != 1.0):
            while (light_ratio != 1.0):

                modified = filters.backgound_detect(image, dark_background, dark_ratio)
                img = filters.backgound_detect(modified, dark_background, light_ratio)
                dest = convolution_filter.convolution_filter(img, "blur")
                dest = convolution_filter.convolution_filter(dest, "blur")
                # show(dest)
                dest1 = filters.black_and_white(dest, 25)
                save_as(dest1, "photos/tmp1.bmp")
                dest2 = filters.detect_edges_better(dest1, 128)
                save_as(dest2, "photos/tmp2.bmp")
                show(dest2)

                command = raw_input("L)oad image \nE)dge detect\nC)onvolution\nB)lack n White\nQ)uit \n: ")
                cmd = command in ["L", "Q", "E", "C", "B", "Y"]

                if command == "Y":
                    print("Dark: " + dark_ratio + " Light: " + light_ratio)

                light_ratio += 0.5
            dark_ratio += 0.5


        #
        # if cmd == False:
        #     print("No such command")
        #     command = "Q"
        # elif image == "" and command != "Q":
        #     print("No Image Loaded")
        #     command = "Q"
        # elif command == "E":
        #     threshold = float(raw_input("Threshold?: "))
        #     filters.detect_edges_better(image, threshold)
        #     show(image)
        # elif command == "C":
        #     dest = convolution_filter.convolution_filter(image, "blur")
        #     show(dest)
        # elif command == "B":
        #     dest1 = filters.black_and_white(image, 60)
        #     dest2 = filters.remove_noise(dest1, 9)
        #     show(dest1)
        #     show(dest2)
