'''General Approaches:
    - Phase Cross Correlation (Mono Modal)
    - Mutual Information Registration (Multi Modal)
    - Machine Learning Approaches:
        - DRMIME: Differentiable Mutual Information and Matrix Exponential for Multi-Resolution Image Registration (https://github.com/abnan/DRMIME)
        - Multi-Modal Image Registration with Unsupervised Deep Learning (From Medical Imaging)
        - Wavelet Decomposition
        - CoMIR (https://github.com/MIDA-group/CoMIR)
    - Phase Correlation -> not applicable because multi modal
    - Mutal Inforamtion Registration <- !!!
    - Machine Learning Approaches: No training Data available for me'''

import argparse
from skimage import io, color
import matplotlib.pyplot as plt
from cv2 import resize
import cv2
import numpy as np
from tqdm import tqdm
from sklearn.metrics import mutual_info_score


def calc_MI(x, y, bins=100):
    c_xy, _, _ = np.histogram2d(x, y, bins)
    mi = mutual_info_score(None, None)
    return mi


def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', required=True,)

    return parser.parse_args()


def main():
    # args = parse()
    plot = False

    images = []
    # 20x : 0.3225 um/pixel or 3.10 pixels/um
    # IMC = 1 um/pixel

    images.append(io.imread("/Users/simongutwein/Documents/GitHub/Wien_Project/data/aipf.ome.tiff"))
    images.append(io.imread("/Users/simongutwein/Documents/GitHub/Wien_Project/data/20210430_BM_STA-NB-2_PFA.tiff"))

    target_size = (int(0.3225*1.4*images[0].shape[0]), int(0.3225*1.4*images[0].shape[1]))

    for i, image in enumerate(images):
        if len(image.shape) == 3:
            images[i] = color.rgb2gray(image)

        if i == 0:
            images[i] = resize(images[i], target_size, interpolation=cv2.INTER_AREA)

        image = images[i]
        image = image / np.percentile(image, 90)
        image[image > 1] = 1
        images[i] = image

    if plot:
        _, ax = plt.subplots(1, 2)
        ax[0].imshow(images[0][images[0].shape[0]//2:images[0].shape[0]//2+200, images[0].shape[1]//2:images[0].shape[1]//2+200])
        ax[1].imshow(images[1][images[1].shape[0]//2:images[1].shape[0]//2+200, images[1].shape[1]//2:images[1].shape[1]//2+200])
        plt.show()

    fix = images[0]
    moving = np.rot90(images[1], k=2)
    print(fix.max(), fix.min())
    print(moving.max(), moving.min())
    fix = (fix*65535).astype(np.uint16)
    moving = (moving*65535).astype(np.uint16)

    print(fix.max(), fix.min())
    print(moving.max(), moving.min())

    moving_space = (0, fix.shape[0]-moving.shape[0], 0, fix.shape[1]-moving.shape[1])
    print(moving_space)
    stride = 100

    mut = np.zeros((int(np.ceil((fix.shape[0]-moving.shape[0])/stride)), int(np.ceil((fix.shape[1]-moving.shape[1])/stride))))
    print(mut.shape)

    for j, i in enumerate(tqdm(range(moving_space[0], moving_space[1], stride))):
        for jj, ii in enumerate(range(moving_space[2], moving_space[3], stride)):
            fix_patch = fix[i:i+moving.shape[0], ii:ii+moving.shape[1]]
            mi = mutual_info_score(fix_patch[moving > 100].astype(np.uint16).ravel(), moving[moving > 100].astype(np.uint16).ravel())
            mut[j, jj] = mi

    top = 10

    plt.imshow(mut)
    plt.show()
    print(mut.max())
    ii = np.unravel_index(np.argsort(mut.ravel())[-top:], mut.shape)
    print(ii)

    for i in range(top):
        _, ax = plt.subplots(1, 2)
        ax[0].imshow(fix[ii[0][i]*stride:ii[0][i]*stride+moving.shape[0], ii[1][i]*stride:ii[1][i]*stride+moving.shape[1]])
        ax[1].imshow(moving)
        plt.show()
        print(np.sum(fix[ii[0][i]*stride:ii[0][i]*stride+moving.shape[0], ii[1][i]*stride:ii[1][i]*stride+moving.shape[1]]-moving))


if __name__ == "__main__":

    main()
