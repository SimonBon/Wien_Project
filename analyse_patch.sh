#!/bin/bash

root_dir="/Users/simongutwein/Documents/GitHub/Wien_Project"

for ARGUMENT in "$@"
do
    KEY=$(echo $ARGUMENT | cut -f1 -d=)
    VALUE=$(echo $ARGUMENT | cut -f2 -d=)   
    case "$KEY" in
            MASKS_DIR)  MASKS_DIR=${VALUE} ;;
            IMAGE_PATH) IMAGE_PATH=${VALUE} ;;
            SAVE_DIR)   SAVE_DIR=${VALUE} ;;
            VISUALIZE)  VISUALIZE=${VALUE} ;;     
            *)   
    esac    
done

PKL_FILE="${SAVE_DIR}/cells.pkl"
PKL_CLUSTERED="${SAVE_DIR}/clustered_cells.pkl"

python3 ${root_dir}/morph_features.py -masks_dir ${MASKS_DIR} -image_path ${IMAGE_PATH} -save_dir ${SAVE_DIR}
python3 ${root_dir}/clustering.py -pkl_file ${PKL_FILE} -save_dir ${SAVE_DIR}
python3 ${root_dir}/visualization.py -pkl_file ${PKL_CLUSTERED} -image_file  ${IMAGE_PATH} -masks_dir ${MASKS_DIR} -save_dir ${SAVE_DIR}

echo "Done! Saved under: ${SAVE_DIR}"
