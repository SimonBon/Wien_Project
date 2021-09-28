# PhD - Challenge

## Module Description:

## [extract_image.py](https://github.com/SimonBon/Wien_Project/blob/master/extract_image.py)

This module extracts the image data from a .czi file.

#### Input: 
'image_path': Path to the .czi-file from which the image data needs to be extracted
'target_path': Path + Filename to which the data is going to be saved.

#### Output: 
File saved under 'target_path' with the image data in the .tiff format


## [create_masks.py](https://github.com/SimonBon/Wien_Project/blob/master/create_masks.py)

This module takes data from the output of CellPose and creates masks for each segmentation instance.

#### Input: 
    'mask_image': Path to the CellPose Output File
    'mask_dir': Path to the directory where the masks should be created

#### Output: 
    Directory with with a binary .png image for each segmentation instance


## [morph_features.py](https://github.com/SimonBon/Wien_Project/blob/master/morph_features.py)

This module extracts morphological features for each of the binary masks in the given input directory. Features are then save in a .xlsx and .pkl file format for later use.

#### Input: 
    '-masks_dir': Path to the directory where the single images for each segmentation instance are saved
    '-image_path': Path to the original image which was segmented by CellPose
    '-save_dir': Path to the directory in which the .xlsx and .pkl file are saved

#### Output: 
    .xlsx file and .pkl file for later use in the pipeline under the 'save_dir' directory

## [clustering.py](https://github.com/SimonBon/Wien_Project/blob/master/clustering.py)

This module uses the output from [morph_features.py](https://github.com/SimonBon/Wien_Project/blob/master/morph_features.py) to cluster the analysed cells into clusters using a PCA (Pricipal Component Analysis). The default number of clusters is 3, but can be changed with the "-clusters" flag. 


#### Input: 

    '-pkl_file': Path to the .pkl file which was previoulsy created by morph_features.py
    '-save_dir': Path to the directory where all files are going to be saved
    '-v': flag to determine if a .gif is going to be created showing the 3D-PCA plot
    '-clusters': define the number of clusters

#### Output: 
    A .pkl file with the information on the clustered cells aswell as information to which cluster each segmented cell belongs.
    .gif file and a hidden folder ".images" under "save_dir" containing the images for the gif from different angles


## [visualize.py](https://github.com/SimonBon/Wien_Project/blob/master/visualize.py)

This module uses the output from [clustering.py](https://github.com/SimonBon/Wien_Project/blob/master/clustering.py) to 

#### Input: 

    '-pkl_file': Path to the .pkl file which was previoulsy created by morph_features.py
    '-save_dir': Path to the directory where all files are going to be saved
    '-v': flag to determine if a .gif is going to be created showing the 3D-PCA plot
    '-clusters': define the number of clusters

#### Output: 

    




