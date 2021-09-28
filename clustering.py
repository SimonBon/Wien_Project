from locale import delocalize
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import pandas as pd
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
from tqdm import tqdm
import os
from natsort import natsorted
from PIL import Image
import argparse
import os


global COLOR_LIST
COLOR_LIST = ["tab:blue", "tab:green", "tab:orange", "c", "m", "y", "k"]


def create_gif(images_dir: str, save_dir: str) -> None:
    '''
    creates a gif from a folder with respective images in it

    Parameters:
    image_dir:  directory with the images for the gif in it
    save_dir:   directory where the created .gif is saved
    '''
    images = [os.path.join(images_dir, x) for x in os.listdir(images_dir) if not x.startswith(".")]
    images = natsorted(images)

    imgs = []
    for path in images:
        imgs.append(Image.open(path))

    imgs[0].save(
        os.path.join(save_dir, "pca.gif"),
        save_all=True,
        append_images=imgs[1:],
        optimize=False,
        duration=40,
        loop=0
    )


def vizualize(df: pd.DataFrame, save_dir: str,  per_var: list, centers=None) -> None:
    '''
    function creates 3D images from a dataframe and saves them in a hidden folder

    Parameters:
    df:         DataFrame for Cell Data
    save_dir:   directory where hidden folder is saved
    per_var:    contribution of the top 3 PCA variables
    centers:    centers of the KNN

    '''

    images_dir = os.path.join(save_dir, '.gif_images')
    if not os.path.isdir(images_dir):
        os.mkdir(images_dir)

    patches = []
    for num, col in enumerate(np.unique(df["class"])):
        if col == "k":
            patches.append(mpatches.Patch(color=col, label=f'Outlier'))
        else:
            patches.append(mpatches.Patch(color=col, label=f'Class {num}'))

    for i in tqdm(range(0, 360)):
        fig = pyplot.figure(figsize=(9, 7))
        ax = Axes3D(fig, auto_add_to_figure=False)
        fig.add_axes(ax)
        ax.scatter(df.PC1, df.PC2, df.PC3, c=df["class"], s=1, marker="x")

        if centers is not None:
            for ii in centers:
                ax.scatter(ii[0], ii[1], ii[2], s=50, marker="x", color="black")

        ax.view_init(elev=20., azim=i)
        ax.set_title('PCA Analysis Cell Segmentation')
        ax.set_xlabel(f'PC1 - {per_var[0]}')
        ax.set_ylabel(f'PC2 - {per_var[1]}')
        ax.set_zlabel(f'PC3 - {per_var[2]}')
        ax.legend(handles=patches)
        pyplot.savefig(os.path.join(images_dir, f"{i}.png"))
        plt.close()

    create_gif(images_dir, save_dir)


def perform_pca(df: pd.DataFrame):

    pca = PCA().fit(df)
    pca_data = pca.transform(df)
    per_var = np.round(pca.explained_variance_ratio_ * 100, decimals=1)
    labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]
    pca_df = pd.DataFrame(pca_data, columns=labels)

    return pca_df, per_var


def define_colors(labels: list) -> list:

    colors = np.array([None for _ in range(len(labels))])
    for i in range(-1, np.array(labels).max()+1):
        colors[labels == i] = COLOR_LIST[i]

    return colors


def parse():

    parser = argparse.ArgumentParser()
    parser.add_argument('-pkl_file', required=True)
    parser.add_argument('-save_dir', required=True)
    parser.add_argument('-v', type=str, default="True")
    parser.add_argument('-clusters', type=str, default=3, required=False)

    args = parser.parse_args()

    if "true" in args.v.lower() or "1" in args.v.lower():
        args.v = True
    elif "false" in args.v.lower() or "0" in args.v.lower():
        args.v = False
    else:
        raise ValueError("Please enter 'True/1' or 'False/0' for parameter -v")

    return args


def main():

    args = parse()

    # get input data
    raw_data = pd.read_pickle(args.pkl_file)

    # extract first 7 features
    feature_data = raw_data.iloc[:, :7]

    # sclare and perform pca
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(feature_data)
    pca_df, per_var = perform_pca(scaled_features)
    pca_df = pca_df.iloc[:, :3]

    # transform PCA results
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(pca_df)
    scaled_features = pd.DataFrame(scaled_features, columns=["PC1", "PC2", "PC3"])

    # cluster PCA scaled features
    kmeans = KMeans(
        init='random',
        n_clusters=args.clusters,
        max_iter=100,
        n_init=20
    )

    kmeans.fit(scaled_features)

    # assign class to each segmented cell
    colors = define_colors(kmeans.labels_)
    scaled_features["class"] = colors
    raw_data["class"] = colors

    #create .gif
    if args.v:
        vizualize(scaled_features, args.save_dir, per_var, centers=kmeans.cluster_centers_)

    # save data
    save_path = os.path.join(args.save_dir, "clustered_cells.pkl")
    raw_data.to_pickle(save_path)

    print(f"Clustering finished! Saved under: {save_path}")


if __name__ == "__main__":
    main()
