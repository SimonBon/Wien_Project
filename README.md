# PhD - Challenge

## Module Description:

### [extract_image.py](https://github.com/SimonBon/Wien_Project/blob/master/extract_image.py)

This module extracts the image data from a .czi file.

#### Input: 
    'image_path': Path to the .czi-file from which the image data needs to be extracted
    'target_path': Path + Filename to which the data is going to be saved.

#### Output: 
    File saved under 'target_path' with the image data in the .tiff format


### [create_masks.py](https://github.com/SimonBon/Wien_Project/blob/master/create_masks.py)

This module takes data from the output of CellPose and creates masks for each segmentation instance.

#### Input: 
    'mask_image': Path to the CellPose Output File
    'mask_dir': Path to the directory where the masks should be created

#### Output: 
    Directory with with a binary .png image for each segmentation instance


    

