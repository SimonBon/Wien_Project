import os
from skimage import io
from skimage.measure import shannon_entropy, find_contours, perimeter
import matplotlib.pyplot as plt
from os.path import join
import pandas as pd
import numpy as np
import math
import argparse
from natsort import natsorted
from tqdm import tqdm
from PIL import Image
import gc


def parse() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('-masks_dir', required=True, type=str)
    parser.add_argument('-image_path', required=True, type=str)
    parser.add_argument('-save_dir', required=True, type=str)

    return parser.parse_args()


def extract_boundaries(mask: np.ndarray) -> list:
    contour = np.array(find_contours(mask)[0]).squeeze()+1
    return np.array([contour[:, 0].min(), contour[:, 0].max(), contour[:, 1].min(), contour[:, 1].max()]).astype(int)


def calculate_roundness(mask: np.ndarray, area: int) -> float:
    perimeter_ = perimeter(mask)
    return (math.pi * 4 * area)/np.square(perimeter_)


def extract_features(image: np.ndarray, mask: np.ndarray, name: str) -> dict:

    masked_aipf = image.copy()
    masked_aipf[~mask] = 0

    cell_pixels = masked_aipf[masked_aipf != 0]
    area = len(cell_pixels)

    mean_pix = cell_pixels.mean()
    upper_20 = np.percentile(cell_pixels, 80)
    lower_20 = np.percentile(cell_pixels, 20)
    std_pix = cell_pixels.std()

    B = extract_boundaries(mask)
    entropy = shannon_entropy(masked_aipf[B[0]:B[1], B[2]:B[3]])
    roundness = calculate_roundness(mask, area)

    features = {
        "area": area,
        "mean": mean_pix,
        "upper_20": upper_20,
        "lower_20": lower_20,
        "std_pix": std_pix,
        "entropy": entropy,
        "roundness": roundness,
        "name": name,
    }

    del masked_aipf
    del cell_pixels
    gc.collect()

    return B, features


def plot_cells(mask: np.ndarray, image: np.ndarray, B: np.ndarray) -> None:

    _, ax = plt.subplots(1, 2)
    ax[0].imshow(mask[B[0]:B[1], B[2]:B[3]])
    ax[1].imshow(image[B[0]:B[1], B[2]:B[3]])
    plt.show()


def main():

    args = parse()

    save_dir = args.save_dir
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    segmentations_path = args.masks_dir
    image_path = args.image_path

    aipf_image = io.imread(image_path).astype(np.float64)

    segmentations = [x for x in os.listdir(segmentations_path) if not x.startswith(".")]
    segmentations = natsorted(segmentations)
    print("Number of cells segmented: ", len(segmentations))

    all_features = []
    for num, mask_name in enumerate(tqdm(segmentations)):
        mask_path = join(segmentations_path, mask_name)
        with Image.open(mask_path) as mask:
            # mask = io.imread(mask_path).astype(bool)
            mask = np.array(mask).astype(bool)
            if mask.any():

                B, features = extract_features(aipf_image, mask, mask_name)
                #plot_cells(mask, aipf_image, B)
                all_features.append(features)

                del mask
                del features
                gc.collect()

    df = pd.DataFrame(all_features)
    save_path = join(save_dir, "cells.pkl")
    df.iloc[:, :7].to_excel(join(save_dir, "cells.xlsx"))
    df.to_pickle(save_path)
    print(f"Feature extraction finished! Saved under: {save_path}")


if __name__ == "__main__":

    main()
