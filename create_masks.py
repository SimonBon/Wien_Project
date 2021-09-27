
import numpy as np
from skimage import io
from PIL import Image

import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('mask_image', required=True,)
    parser.add_argument('mask_dir', required=True,)
    return parser.parse_args()


def main():

    args = parse()

    mask = np.array(io.imread(args.mask_image)).astype(np.uint16)

    for i in range(mask.min()+1, mask.max()):
        patch = mask.copy()
        patch[patch != i] = 0
        patch[patch == i] = 255
        im = Image.fromarray(np.uint8(patch))
        im.save(f"{args.mask_dir}/mask_{i}.png")


if __name__ == "__main__":
    main()
