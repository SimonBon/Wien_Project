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

    clustered_data = pd.read_pickle(args.pkl_file)
    image = io.imread(args.image_file)
    overlay = np.zeros((*image.shape, 3))

    define_channel(clustered_data)

    names = clustered_data["name"]

    for name, channel in tqdm(zip(names, clustered_data["channel"])):
        with Image.open(os.path.join(args.masks_dir, name)) as mask:
            mask = np.array(mask).astype(bool)

        overlay[mask, channel] = 1

    _, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(image, cmap="gray")
    ax.imshow(overlay, alpha=0.2)
    ax.axis("off")
    save_path = os.path.join(args.save_dir, "overlay.png")
    plt.savefig(save_path)
    print(f"Visualization finished! Saved under: {save_path}")


if __name__ == "__main__":
    main()
