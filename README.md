# Yolo v3 Implementation on Kitti

## Step 1, Set up the darknet
```bash
git clone https://github.com/MuMuPatrick/kitti_yolo/ 
make 
```
## Step 2, Transfer the format of KITTI
Download the Kitti Dataset for Object Detection, the link for is http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=2d
Transfer the KITTI Dataset into VOC format, 
  Firstly, load the images into `.\kitti_dataset\JPEGImages` and labels to `.\kitti_dataset\Labels`
  If you want to combine the annotations, run `python modify_annotations_txt.py`
  Secondly, change the format from txt into xml, run `python kitti_txt_to_xml.py`
  Thirdly, change the xml format into the format that can be read by darknet `python xml_to_yolo_txt.py`

## Step 3, Load the KITTI Dataset to YOLO
Save the image into `.\kitti_data\train_images` and `.\kitti_data\val_images` and the labels into `.\kitti_data\train_labels` and `.\kitti_data\val_labels` respectively
At the main directory folder, run `python kitti_train_val.py` to generate train.txt and valid.txt
Ensure the kitti.names is in the right configuration. Please ensure the right .txt file is linked during training or validation

## Step 4, Train or Test the model
If you want to train the model with pre-trained darknet53, please download the `darknet53.conv.74` in https://pjreddie.com/media/files/darknet53.conv.74 and store the weight document under the main category, run
```bash
./darknet detector train kitti_data/kitti.data cfg/yolov3-kitti.cfg darknet53.conv.74 
```
If you want to download the best weight in 10000 iterations, please download at https://drive.google.com/file/d/1LSVrJOq_MboOLbwa8LFfo6-eMSe2cvQ0/view?usp=sharing, 
You can generate prediction by 
```bash
./darknet detector test kitti_data/kitti.data cfg/yolov3-kitti.cfg yolov3-kitti_best.weight
```
And provide path to the image to generate prediction
