# Yolo v3 Implementation on Kitti

## Step 1, Set up the darknet
'''
git clone https://github.com/MuMuPatrick/kitti_yolo/ 
make 
'''
## Step 2, Transfer the format of KITTI
Download the Kitti Dataset for Object Detection, the link for is http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d
Transfer the KITTI Dataset into VOC format


## Step 3, Load the KITTI Dataset to YOLO
Save the image into '.\kitti_data\train_images' and '.\kitti_data\val_images' and the labels into '.\kitti_data\train_labels' and '.\kitti_data\val_labels' respectively
Set up 
