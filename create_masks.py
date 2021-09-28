'''
Function to create individual binary images for each segmented instance from CellPose output

Parameters:
mask_image:  path to output image from CellPose
mask_dir:  path to directory where images will be saved
'''
import numpy as np
from skimage import io
from PIL import Image
import os
import argparse


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument('mask_image', required=True,)
    parser.add_argument('mask_dir', required=True,)
    return parser.parse_args()


def main():

    args = parse()

    if not os.path.isdir(args.mask_dir):
        os.mkdir(args.mask_dir)

    mask = np.array(io.imread(args.mask_image)).astype(np.uint16)

    # iterate over all values in mask image (each color identifies a single cell)
    for i in range(mask.min()+1, mask.max()):
        patch = mask.copy()
        patch[patch != i] = 0
        patch[patch == i] = 255
        im = Image.fromarray(np.uint8(patch))
        im.save(f"{args.mask_dir}/mask_{i}.png")


if __name__ == "__main__":
    main()
