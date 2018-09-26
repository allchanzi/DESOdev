import skimage.io as io
import numpy as np
from math import floor
import unittest



def load_image(file_path):
    loaded_image = io.imread(file_path)[:, :, :3]
    return np.array(loaded_image)


def decrease_color_depth(input_image, output_depth):

    color_mapping = {
        9: 7,
        12: 15,
        15: 31,
        18: 63,
        21: 127,
        24: 255
    }

    if output_depth not in color_mapping:
        print("here")
        return None
    else:
        output_image = input_image.copy()
        # max = get_max(input_image) # mozno pouzit miesto 255
        height = len(input_image)
        width = len(input_image[0])

        for x in range(height):
            for y in range(width):
                R, G, B = input_image[x, y]

                newR = floor(color_mapping[output_depth] * R / 255) * floor(255/color_mapping[output_depth])
                newG = floor(color_mapping[output_depth] * G / 255) * floor(255/color_mapping[output_depth])
                newB = floor(color_mapping[output_depth] * B / 255) * floor(255/color_mapping[output_depth])

                output_image[x, y] = [newR, newG, newB]

        return np.array(output_image)


def get_color_channel(input_image, channel):
    output_image = input_image.copy()

    for row in output_image:
        for col in row:
            if channel.upper() in ("BLUE", "B"):
                col[1] = 0
                col[2] = 0
            if channel.upper() in ("GREEN", "G"):
                col[0] = 0
                col[2] = 0
            if channel.upper() in ("RED", "R"):
                col[0] = 0
                col[1] = 0

    return output_image


def flop_image(input_image): #vertically
    flopped_image = input_image.copy()
    rows = len(input_image)
    cols = len(input_image[0])
    for row in range(rows):
        flopped_image[row] = input_image[row][::-1]
        # cols = len(input_image[row])
        # for col in range(cols):
        #     flopped_image[row,col] = input_image[row, cols - col - 1]

    return flopped_image


def flip_image(input_image): #horizontally
    flipped_image = input_image[::-1]
    # flipped_image = input_image.copy()
    # rows = len(input_image)
    # for row in range(rows):
    #     flipped_image[row] = input_image[rows - row - 1]

    return np.array(flipped_image)


def get_max(input_array):
    max = 0
    for row in input_array:
        for col in row:
            for channel in col:
                if channel > max :
                    max = channel

                if (channel == 255):
                    break;

    return max

class ImageProcessor(object):

    def __init__(self):
        self.original_image = None
        self.output_image = None

    def load_image(self, path):
        self.original_image = load_image(path)
        return self.original_image

    def decrease_color_depth(self, output_depth, callback):
        self.output_image = decrease_color_depth(self.original_image, output_depth)
        callback(self.output_image)

    def flop_image(self):
        self.output_image = flop_image(self.original_image)
        return self.output_image

    def flip_image(self):
        self.output_image = flip_image(self.original_image)
        return self.output_image

    def get_color_channel(self, channel):
        self.output_image = get_color_channel(self.original_image, channel)
        return self.output_image

    def save(self, path):
        io.imsave(path, self.output_image)



class TestImageProcessor(unittest.TestCase):

    def test_load(self):
        jpgimage = load_image("inputs/jpgexample.jpg")
        _, _, channels = jpgimage.shape
        self.assertEqual(channels, 3)
        pngimage = load_image("inputs/pngexample.png")
        _, _, channels = pngimage.shape
        self.assertEqual(channels, 3)

    def test_flip(self):
        case = np.array([[ 1,  2,  3,  4],
                         [ 5,  6,  7,  8],
                         [ 9, 10, 11, 12],
                         [13, 14, 15, 16]])

        result = np.array([[13, 14, 15, 16],
                           [ 9, 10, 11, 12],
                           [ 5,  6,  7,  8],
                           [ 1,  2,  3,  4]])
        self.assertEqual(flip_image(case).tolist(), result.tolist())
        case = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]])

        result = np.array([[7, 8, 9],
                           [4, 5, 6],
                           [1, 2, 3]])
        self.assertEqual(flip_image(case).tolist(), result.tolist())

    def test_flop(self):
        case = np.array([[ 1,  2,  3,  4],
                         [ 5,  6,  7,  8],
                         [ 9, 10, 11, 12],
                         [13, 14, 15, 16]])

        result = np.array([[ 4,  3,  2,  1],
                           [ 8,  7,  6,  5],
                           [12, 11, 10,  9],
                           [16, 15, 14, 13]])
        self.assertEqual(flop_image(case).tolist(), result.tolist())
        case = np.array([[1, 2, 3],
                         [4, 5, 6],
                         [7, 8, 9]])
        result = np.array([[3, 2, 1],
                           [6, 5, 4],
                           [9, 8, 7]])
        self.assertEqual(flop_image(case).tolist(), result.tolist())

    def test_get_color_channel(self):
        input = np.array([[[1, 1, 1], [2, 2, 2], [3, 3, 3]],
                          [[4, 4, 4], [5, 5, 5], [6, 6, 6]],
                          [[7, 7, 7], [8, 8, 8], [9, 9, 9]]])

        case = "B"
        result = np.array([[[1, 0, 0], [2, 0, 0], [3, 0, 0]],
                           [[4, 0, 0], [5, 0, 0], [6, 0, 0]],
                           [[7, 0, 0], [8, 0, 0], [9, 0, 0]]])
        self.assertEqual(get_color_channel(input, case).tolist(), result.tolist())

        case = "g"
        result = np.array([[[0, 1, 0], [0, 2, 0], [0, 3, 0]],
                           [[0, 4, 0], [0, 5, 0], [0, 6, 0]],
                           [[0, 7, 0], [0, 8, 0], [0, 9, 0]]])
        self.assertEqual(get_color_channel(input, case).tolist(), result.tolist())

        case = "red"
        result = np.array([[[0, 0, 1], [0, 0, 2], [0, 0, 3]],
                           [[0, 0, 4], [0, 0, 5], [0, 0, 6]],
                           [[0, 0, 7], [0, 0, 8], [0, 0, 9]]])
        self.assertEqual(get_color_channel(input, case).tolist(), result.tolist())

# unittest.main()



