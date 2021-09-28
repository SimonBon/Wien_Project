'''
function to extract image data from a .czi file and save it as a tiff file foe easier use

Parameters:
image_path:  path to the .czi image
target_path:  desired path and name of the .tiff file
'''

from aicsimageio.writers import OmeTiffWriter
from napari_czifile2 import io

import argparse


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', required=True,)
    parser.add_argument('target_path', required=True,)
    return parser.parse_args()


def main():

    args = parse()

    img = io.CZISceneFile(args.image_path, 0)
    pixel_sz = [img.scale_x_um, img.scale_y_um]
    image = img.as_tzcyx0_array()
    image = image.squeeze()

    OmeTiffWriter.save(
        image,
        uri=args.target_path,
        pixels_physical_size=pixel_sz,
        dimension_order="XY",
    )

    print(f"Image Saved under: {args.target_path}")


if __name__ == "__main__":
    main()
