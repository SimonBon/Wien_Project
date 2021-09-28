'''
script to visualize the classification of single cells

Parameters:
pkl_file:  path to pkl file previously generated to assign classes to cells
image_file:  path to the original image file on which segmentation was performed
mask_dir: path to the directory where all mask images are saved
save_dir: path to the directory where the overlay image is saved
'''
import argparse
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
from tqdm import tqdm


def define_channel(data):

    channels = np.array([None for _ in data.iterrows()])

    channels[data["class"] == "tab:blue"] = 0
    channels[data["class"] == "tab:green"] = 1
    channels[data["class"] == "tab:orange"] = 2

    data["channel"] = channels


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-pkl_file', required=True)
    parser.add_argument('-image_file', required=True)
    parser.add_argument('-masks_dir', required=True)
    parser.add_argument('-save_dir', required=True)

    return parser.parse_args()


def main():
    args = parse()

    # read in clustered data and original image
    clustered_data = pd.read_pickle(args.pkl_file)
    image = io.imread(args.image_file)

    # predefine new image of size of original image
    overlay = np.zeros((*image.shape, 3))

    # define colors for overlay
    define_channel(clustered_data)

    # names of the mask files
    names = clustered_data["name"]

    # loop over files to assign color
    for name, channel in tqdm(zip(names, clustered_data["channel"])):
        with Image.open(os.path.join(args.masks_dir, name)) as mask:
            mask = np.array(mask).astype(bool)

        overlay[mask, channel] = 1

    # plot image and save in save_dir
    _, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image, cmap="gray")
    ax.imshow(overlay, alpha=0.2)
    ax.axis("off")
    save_path = os.path.join(args.save_dir, "overlay.png")
    plt.savefig(save_path)
    print(f"Visualization finished! Saved under: {save_path}")


if __name__ == "__main__":
    main()
