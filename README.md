
### How to compile on Linux (using `make`)

Just do `make` in the darknet directory. (You can try to compile and run it on Google Colab in cloud [link](https://colab.research.google.com/drive/12QusaaRj_lUwCGDvQNfICpa7kA7_a2dE) (press «Open in Playground» button at the top-left corner) and watch the video [link](https://www.youtube.com/watch?v=mKAEGSxwOAY) )
Before make, you can set such options in the `Makefile`: [link](https://github.com/AlexeyAB/darknet/blob/9c1b9a2cf6363546c152251be578a21f3c3caec6/Makefile#L1)

- `GPU=1` to build with CUDA to accelerate by using GPU (CUDA should be in `/usr/local/cuda`)
- `CUDNN=1` to build with cuDNN v5-v7 to accelerate training by using GPU (cuDNN should be in `/usr/local/cudnn`)
- `CUDNN_HALF=1` to build for Tensor Cores (on Titan V / Tesla V100 / DGX-2 and later) speedup Detection 3x, Training 2x
- `OPENCV=1` to build with OpenCV 4.x/3.x/2.4.x - allows to detect on video files and video streams from network cameras or web-cams
- `DEBUG=1` to build debug version of Yolo
- `OPENMP=1` to build with OpenMP support to accelerate Yolo by using multi-core CPU
- `LIBSO=1` to build a library `darknet.so` and binary runnable file `uselib` that uses this library. Or you can try to run so `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib test.mp4` How to use this SO-library from your own code - you can look at C++ example: https://github.com/AlexeyAB/darknet/blob/master/src/yolo_console_dll.cpp
    or use in such a way: `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib data/coco.names cfg/yolov4.cfg yolov4.weights test.mp4`
- `ZED_CAMERA=1` to build a library with ZED-3D-camera support (should be ZED SDK installed), then run
    `LD_LIBRARY_PATH=./:$LD_LIBRARY_PATH ./uselib data/coco.names cfg/yolov4.cfg yolov4.weights zed_camera`
- You also need to specify for which graphics card the code is generated. This is done by setting `ARCH=`. If you use a never version than CUDA 11 you further need to edit line 20 from Makefile and remove `-gencode arch=compute_30,code=sm_30 \` as Kepler GPU support was dropped in CUDA 11. You can also drop the general `ARCH=` and just uncomment `ARCH=` for your graphics card.

### How to compile on Windows (using `CMake`)

Requires:

- MSVC: https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=Community
- CMake GUI: `Windows win64-x64 Installer`https://cmake.org/download/
- Download Darknet zip-archive with the latest commit and uncompress it: [master.zip](https://github.com/AlexeyAB/darknet/archive/master.zip)

In Windows:

- Start (button) -> All programs -> CMake -> CMake (gui) ->

- [look at image](https://habrastorage.org/webt/pz/s1/uu/pzs1uu4heb7vflfcjqn-lxy-aqu.jpeg) In CMake: Enter input path to the darknet Source, and output path to the Binaries -> Configure (button) -> Optional platform for generator: `x64`  -> Finish -> Generate -> Open Project ->

- in MS Visual Studio: Select: x64 and Release -> Build -> Build solution

- find the executable file `darknet.exe` in the output path to the binaries you specified

![x64 and Release](https://habrastorage.org/webt/ay/ty/f-/aytyf-8bufe7q-16yoecommlwys.jpeg)

### How to compile on Windows (using `vcpkg`)

This is the recommended approach to build Darknet on Windows.

1. Install Visual Studio 2017 or 2019. In case you need to download it, please go here: [Visual Studio Community](http://visualstudio.com). Remember to install English language pack, this is mandatory for vcpkg!

2. Install CUDA enabling VS Integration during installation.

3. Open Powershell (Start -> All programs -> Windows Powershell) and type these commands:

```PowerShell
Set-ExecutionPolicy unrestricted -Scope CurrentUser -Force
git clone https://github.com/AlexeyAB/darknet
cd darknet
.\build.ps1 -UseVCPKG -EnableOPENCV -EnableCUDA -EnableCUDNN
```

(add option `-EnableOPENCV_CUDA` if you want to build OpenCV with CUDA support - very slow to build! - or remove options like `-EnableCUDA` or `-EnableCUDNN` if you are not interested in them). If you open the `build.ps1` script at the beginning you will find all available switches.

## How to train with multi-GPU

1. Train it first on 1 GPU for like 1000 iterations: `darknet.exe detector train cfg/coco.data cfg/yolov4.cfg yolov4.conv.137`

2. Then stop and by using partially-trained model `/backup/yolov4_1000.weights` run training with multigpu (up to 4 GPUs): `darknet.exe detector train cfg/coco.data cfg/yolov4.cfg /backup/yolov4_1000.weights -gpus 0,1,2,3`

If you get a Nan, then for some datasets better to decrease learning rate, for 4 GPUs set `learning_rate = 0,00065` (i.e. learning_rate = 0.00261 / GPUs). In this case also increase 4x times `burn_in =` in your cfg-file. I.e. use `burn_in = 4000` instead of `1000`.

https://groups.google.com/d/msg/darknet/NbJqonJBTSY/Te5PfIpuCAAJ

## How to train (to detect your custom objects)

(to train old Yolo v2 `yolov2-voc.cfg`, `yolov2-tiny-voc.cfg`, `yolo-voc.cfg`, `yolo-voc.2.0.cfg`, ... [click by the link](https://github.com/AlexeyAB/darknet/tree/47c7af1cea5bbdedf1184963355e6418cb8b1b4f#how-to-train-pascal-voc-data))

Training Yolo v4 (and v3):

0. For training `cfg/yolov4-custom.cfg` download the pre-trained weights-file (162 MB): [yolov4.conv.137](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137) (Google drive mirror [yolov4.conv.137](https://drive.google.com/open?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp) )
1. Create file `yolo-obj.cfg` with the same content as in `yolov4-custom.cfg` (or copy `yolov4-custom.cfg` to `yolo-obj.cfg)` and:

- change line batch to [`batch=64`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L3)
- change line subdivisions to [`subdivisions=16`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)
- change line max_batches to (`classes*2000`, but not less than number of training images and not less than `6000`), f.e. [`max_batches=6000`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) if you train for 3 classes
- change line steps to 80% and 90% of max_batches, f.e. [`steps=4800,5400`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L22)
- set network size `width=416 height=416` or any value multiple of 32: https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L8-L9
- change line `classes=80` to your number of objects in each of 3 `[yolo]`-layers:
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L610
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L696
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L783
- change [`filters=255`] to filters=(classes + 5)x3 in the 3 `[convolutional]` before each `[yolo]` layer, keep in mind that it only has to be the last `[convolutional]` before each of the `[yolo]` layers.
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L603
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L689
  - https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L776
- when using [`[Gaussian_yolo]`](https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L608)  layers, change [`filters=57`] filters=(classes + 9)x3 in the 3 `[convolutional]` before each `[Gaussian_yolo]` layer
  - https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L604
  - https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L696
  - https://github.com/AlexeyAB/darknet/blob/6e5bdf1282ad6b06ed0e962c3f5be67cf63d96dc/cfg/Gaussian_yolov3_BDD.cfg#L789

So if `classes=1` then should be `filters=18`. If `classes=2` then write `filters=21`.
**(Do not write in the cfg-file: filters=(classes + 5)x3)**

(Generally `filters` depends on the `classes`, `coords` and number of `mask`s, i.e. filters=`(classes + coords + 1)*<number of mask>`, where `mask` is indices of anchors. If `mask` is absence, then filters=`(classes + coords + 1)*num`)

So for example, for 2 objects, your file `yolo-obj.cfg` should differ from `yolov4-custom.cfg` in such lines in each of **3** [yolo]-layers:

```ini
[convolutional]
filters=21

[region]
classes=2
```

2. Create file `obj.names` in the directory `build\darknet\x64\data\`, with objects names - each in new line
3. Create file `obj.data` in the directory `build\darknet\x64\data\`, containing (where **classes = number of objects**):

  ```ini
  classes = 2
  train  = data/train.txt
  valid  = data/test.txt
  names = data/obj.names
  backup = backup/
  ```

4. Put image-files (.jpg) of your objects in the directory `build\darknet\x64\data\obj\`
5. You should label each object on images from your dataset. Use this visual GUI-software for marking bounded boxes of objects and generating annotation files for Yolo v2 & v3: https://github.com/AlexeyAB/Yolo_mark

It will create `.txt`-file for each `.jpg`-image-file - in the same directory and with the same name, but with `.txt`-extension, and put to file: object number and object coordinates on this image, for each object in new line:

`<object-class> <x_center> <y_center> <width> <height>`

  Where:

- `<object-class>` - integer object number from `0` to `(classes-1)`
- `<x_center> <y_center> <width> <height>` - float values **relative** to width and height of image, it can be equal from `(0.0 to 1.0]`
- for example: `<x> = <absolute_x> / <image_width>` or `<height> = <absolute_height> / <image_height>`
- attention: `<x_center> <y_center>` - are center of rectangle (are not top-left corner)

  For example for `img1.jpg` you will be created `img1.txt` containing:

  ```csv
  1 0.716797 0.395833 0.216406 0.147222
  0 0.687109 0.379167 0.255469 0.158333
  1 0.420312 0.395833 0.140625 0.166667
  ```

6. Create file `train.txt` in directory `build\darknet\x64\data\`, with filenames of your images, each filename in new line, with path relative to `darknet.exe`, for example containing:

  ```csv
  data/obj/img1.jpg
  data/obj/img2.jpg
  data/obj/img3.jpg
  ```

7. Download pre-trained weights for the convolutional layers and put to the directory `build\darknet\x64`
    - for `yolov4.cfg`, `yolov4-custom.cfg` (162 MB): [yolov4.conv.137](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.conv.137) (Google drive mirror [yolov4.conv.137](https://drive.google.com/open?id=1JKF-bdIklxOOVy-2Cr5qdvjgGpmGfcbp) )
    - for `yolov4-tiny.cfg`, `yolov4-tiny-3l.cfg`, `yolov4-tiny-custom.cfg` (19 MB): [yolov4-tiny.conv.29](https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29)  
    - for `csresnext50-panet-spp.cfg` (133 MB): [csresnext50-panet-spp.conv.112](https://drive.google.com/file/d/16yMYCLQTY_oDlCIZPfn_sab6KD3zgzGq/view?usp=sharing)
    - for `yolov3.cfg, yolov3-spp.cfg` (154 MB): [darknet53.conv.74](https://pjreddie.com/media/files/darknet53.conv.74)
    - for `yolov3-tiny-prn.cfg , yolov3-tiny.cfg` (6 MB): [yolov3-tiny.conv.11](https://drive.google.com/file/d/18v36esoXCh-PsOKwyP2GWrpYDptDY8Zf/view?usp=sharing)
    - for `enet-coco.cfg (EfficientNetB0-Yolov3)` (14 MB): [enetb0-coco.conv.132](https://drive.google.com/file/d/1uhh3D6RSn0ekgmsaTcl-ZW53WBaUDo6j/view?usp=sharing)

8. Start training by using the command line: `darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137`

   To train on Linux use command: `./darknet detector train data/obj.data yolo-obj.cfg yolov4.conv.137` (just use `./darknet` instead of `darknet.exe`)

   - (file `yolo-obj_last.weights` will be saved to the `build\darknet\x64\backup\` for each 100 iterations)
   - (file `yolo-obj_xxxx.weights` will be saved to the `build\darknet\x64\backup\` for each 1000 iterations)
   - (to disable Loss-Window use `darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137 -dont_show`, if you train on computer without monitor like a cloud Amazon EC2)
   - (to see the mAP & Loss-chart during training on remote server without GUI, use command `darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137 -dont_show -mjpeg_port 8090 -map` then open URL `http://ip-address:8090` in Chrome/Firefox browser)

8.1. For training with mAP (mean average precisions) calculation for each 4 Epochs (set `valid=valid.txt` or `train.txt` in `obj.data` file) and run: `darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137 -map`

9. After training is complete - get result `yolo-obj_final.weights` from path `build\darknet\x64\backup\`

   - After each 100 iterations you can stop and later start training from this point. For example, after 2000 iterations you can stop training, and later just start training using: `darknet.exe detector train data/obj.data yolo-obj.cfg backup\yolo-obj_2000.weights`

    (in the original repository https://github.com/pjreddie/darknet the weights-file is saved only once every 10 000 iterations `if(iterations > 1000)`)

   - Also you can get result earlier than all 45000 iterations.

 **Note:** If during training you see `nan` values for `avg` (loss) field - then training goes wrong, but if `nan` is in some other lines - then training goes well.

 **Note:** If you changed width= or height= in your cfg-file, then new width and height must be divisible by 32.

 **Note:** After training use such command for detection: `darknet.exe detector test data/obj.data yolo-obj.cfg yolo-obj_8000.weights`

  **Note:** if error `Out of memory` occurs then in `.cfg`-file you should increase `subdivisions=16`, 32 or 64: [link](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)

### How to train tiny-yolo (to detect your custom objects)

Do all the same steps as for the full yolo model as described above. With the exception of:

- Download file with the first 29-convolutional layers of yolov4-tiny: https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v4_pre/yolov4-tiny.conv.29
 (Or get this file from yolov4-tiny.weights file by using command: `darknet.exe partial cfg/yolov4-tiny-custom.cfg yolov4-tiny.weights yolov4-tiny.conv.29 29`
- Make your custom model `yolov4-tiny-obj.cfg` based on `cfg/yolov4-tiny-custom.cfg` instead of `yolov4.cfg`
- Start training: `darknet.exe detector train data/obj.data yolov4-tiny-obj.cfg yolov4-tiny.conv.29`

For training Yolo based on other models ([DenseNet201-Yolo](https://github.com/AlexeyAB/darknet/blob/master/build/darknet/x64/densenet201_yolo.cfg) or [ResNet50-Yolo](https://github.com/AlexeyAB/darknet/blob/master/build/darknet/x64/resnet50_yolo.cfg)), you can download and get pre-trained weights as showed in this file: https://github.com/AlexeyAB/darknet/blob/master/build/darknet/x64/partial.cmd
If you made you custom model that isn't based on other models, then you can train it without pre-trained weights, then will be used random initial weights.

## When should I stop training

Usually sufficient 2000 iterations for each class(object), but not less than number of training images and not less than 6000 iterations in total. But for a more precise definition when you should stop training, use the following manual:

1. During training, you will see varying indicators of error, and you should stop when no longer decreases **0.XXXXXXX avg**:

  > Region Avg IOU: 0.798363, Class: 0.893232, Obj: 0.700808, No Obj: 0.004567, Avg Recall: 1.000000,  count: 8
  > Region Avg IOU: 0.800677, Class: 0.892181, Obj: 0.701590, No Obj: 0.004574, Avg Recall: 1.000000,  count: 8
  >
  > **9002**: 0.211667, **0.60730 avg**, 0.001000 rate, 3.868000 seconds, 576128 images
  > Loaded: 0.000000 seconds

- **9002** - iteration number (number of batch)
- **0.60730 avg** - average loss (error) - **the lower, the better**

  When you see that average loss **0.xxxxxx avg** no longer decreases at many iterations then you should stop training. The final average loss can be from `0.05` (for a small model and easy dataset) to `3.0` (for a big model and a difficult dataset).
  
  Or if you train with flag `-map` then you will see mAP indicator `Last accuracy mAP@0.5 = 18.50%` in the console - this indicator is better than Loss, so train while mAP increases.

2. Once training is stopped, you should take some of last `.weights`-files from `darknet\build\darknet\x64\backup` and choose the best of them:

For example, you stopped training after 9000 iterations, but the best result can give one of previous weights (7000, 8000, 9000). It can happen due to over-fitting. **Over-fitting** - is case when you can detect objects on images from training-dataset, but can't detect objects on any others images. You should get weights from **Early Stopping Point**:

![Over-fitting](https://hsto.org/files/5dc/7ae/7fa/5dc7ae7fad9d4e3eb3a484c58bfc1ff5.png)

To get weights from Early Stopping Point:

  2.1. At first, in your file `obj.data` you must specify the path to the validation dataset `valid = valid.txt` (format of `valid.txt` as in `train.txt`), and if you haven't validation images, just copy `data\train.txt` to `data\valid.txt`.

  2.2 If training is stopped after 9000 iterations, to validate some of previous weights use this commands:

(If you use another GitHub repository, then use `darknet.exe detector recall`... instead of `darknet.exe detector map`...)

- `darknet.exe detector map data/obj.data yolo-obj.cfg backup\yolo-obj_7000.weights`
- `darknet.exe detector map data/obj.data yolo-obj.cfg backup\yolo-obj_8000.weights`
- `darknet.exe detector map data/obj.data yolo-obj.cfg backup\yolo-obj_9000.weights`

And compare last output lines for each weights (7000, 8000, 9000):

Choose weights-file **with the highest mAP (mean average precision)** or IoU (intersect over union)

For example, **bigger mAP** gives weights `yolo-obj_8000.weights` - then **use this weights for detection**.

Or just train with `-map` flag:

`darknet.exe detector train data/obj.data yolo-obj.cfg yolov4.conv.137 -map`

So you will see mAP-chart (red-line) in the Loss-chart Window. mAP will be calculated for each 4 Epochs using `valid=valid.txt` file that is specified in `obj.data` file (`1 Epoch = images_in_train_txt / batch` iterations)

(to change the max x-axis value - change [`max_batches=`](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L20) parameter to `2000*classes`, f.e. `max_batches=6000` for 3 classes)

![loss_chart_map_chart](https://hsto.org/webt/yd/vl/ag/ydvlagutof2zcnjodstgroen8ac.jpeg)

Example of custom object detection: `darknet.exe detector test data/obj.data yolo-obj.cfg yolo-obj_8000.weights`

- **IoU** (intersect over union) - average intersect over union of objects and detections for a certain threshold = 0.24

- **mAP** (mean average precision) - mean value of `average precisions` for each class, where `average precision` is average value of 11 points on PR-curve for each possible threshold (each probability of detection) for the same class (Precision-Recall in terms of PascalVOC, where Precision=TP/(TP+FP) and Recall=TP/(TP+FN) ), page-11: http://homepages.inf.ed.ac.uk/ckiw/postscript/ijcv_voc09.pdf

**mAP** is default metric of precision in the PascalVOC competition, **this is the same as AP50** metric in the MS COCO competition.
In terms of Wiki, indicators Precision and Recall have a slightly different meaning than in the PascalVOC competition, but **IoU always has the same meaning**.

![precision_recall_iou](https://hsto.org/files/ca8/866/d76/ca8866d76fb840228940dbf442a7f06a.jpg)

### Custom object detection

Example of custom object detection: `darknet.exe detector test data/obj.data yolo-obj.cfg yolo-obj_8000.weights`

| ![Yolo_v2_training](https://hsto.org/files/d12/1e7/515/d121e7515f6a4eb694913f10de5f2b61.jpg) | ![Yolo_v2_training](https://hsto.org/files/727/c7e/5e9/727c7e5e99bf4d4aa34027bb6a5e4bab.jpg) |
|---|---|

## How to improve object detection

1. Before training:

- set flag `random=1` in your `.cfg`-file - it will increase precision by training Yolo for different resolutions: [link](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L788)

- increase network resolution in your `.cfg`-file (`height=608`, `width=608` or any value multiple of 32) - it will increase precision

- check that each object that you want to detect is mandatory labeled in your dataset - no one object in your data set should not be without label. In the most training issues - there are wrong labels in your dataset (got labels by using some conversion script, marked with a third-party tool, ...). Always check your dataset by using: https://github.com/AlexeyAB/Yolo_mark

- my Loss is very high and mAP is very low, is training wrong? Run training with `-show_imgs` flag at the end of training command, do you see correct bounded boxes of objects (in windows or in files `aug_...jpg`)? If no - your training dataset is wrong.

- for each object which you want to detect - there must be at least 1 similar object in the Training dataset with about the same: shape, side of object, relative size, angle of rotation, tilt, illumination. So desirable that your training dataset include images with objects at different: scales, rotations, lightings, from different sides, on different backgrounds - you should preferably have 2000 different images for each class or more, and you should train `2000*classes` iterations or more

- desirable that your training dataset include images with non-labeled objects that you do not want to detect - negative samples without bounded box (empty `.txt` files) - use as many images of negative samples as there are images with objects

- What is the best way to mark objects: label only the visible part of the object, or label the visible and overlapped part of the object, or label a little more than the entire object (with a little gap)? Mark as you like - how would you like it to be detected.

- for training with a large number of objects in each image, add the parameter `max=200` or higher value in the last `[yolo]`-layer or `[region]`-layer in your cfg-file (the global maximum number of objects that can be detected by YoloV3 is `0,0615234375*(width*height)` where are width and height are parameters from `[net]` section in cfg-file)
  
- for training for small objects (smaller than 16x16 after the image is resized to 416x416) - set `layers = 23` instead of https://github.com/AlexeyAB/darknet/blob/6f718c257815a984253346bba8fb7aa756c55090/cfg/yolov4.cfg#L895
  - set `stride=4` instead of https://github.com/AlexeyAB/darknet/blob/6f718c257815a984253346bba8fb7aa756c55090/cfg/yolov4.cfg#L892
  - set `stride=4` instead of https://github.com/AlexeyAB/darknet/blob/6f718c257815a984253346bba8fb7aa756c55090/cfg/yolov4.cfg#L989
  
- for training for both small and large objects use modified models:
  - Full-model: 5 yolo layers: https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov3_5l.cfg
  - Tiny-model: 3 yolo layers: https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-tiny-3l.cfg
  - YOLOv4: 3 yolo layers: https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4-custom.cfg
  
- If you train the model to distinguish Left and Right objects as separate classes (left/right hand, left/right-turn on road signs, ...) then for disabling flip data augmentation - add `flip=0` here: https://github.com/AlexeyAB/darknet/blob/3d2d0a7c98dbc8923d9ff705b81ff4f7940ea6ff/cfg/yolov3.cfg#L17
  
- General rule - your training dataset should include such a set of relative sizes of objects that you want to detect:
  - `train_network_width * train_obj_width / train_image_width ~= detection_network_width * detection_obj_width / detection_image_width`
  - `train_network_height * train_obj_height / train_image_height ~= detection_network_height * detection_obj_height / detection_image_height`

  I.e. for each object from Test dataset there must be at least 1 object in the Training dataset with the same class_id and about the same relative size:

  `object width in percent from Training dataset` ~= `object width in percent from Test dataset`

  That is, if only objects that occupied 80-90% of the image were present in the training set, then the trained network will not be able to detect objects that occupy 1-10% of the image.

- to speedup training (with decreasing detection accuracy) set param `stopbackward=1` for layer-136 in cfg-file

- each: `model of object, side, illumination, scale, each 30 grad` of the turn and inclination angles - these are *different objects* from an internal perspective of the neural network. So the more *different objects* you want to detect, the more complex network model should be used.

- to make the detected bounded boxes more accurate, you can add 3 parameters `ignore_thresh = .9 iou_normalizer=0.5 iou_loss=giou` to each `[yolo]` layer and train, it will increase mAP@0.9, but decrease mAP@0.5.

- Only if you are an **expert** in neural detection networks - recalculate anchors for your dataset for `width` and `height` from cfg-file:
`darknet.exe detector calc_anchors data/obj.data -num_of_clusters 9 -width 416 -height 416`
then set the same 9 `anchors` in each of 3 `[yolo]`-layers in your cfg-file. But you should change indexes of anchors `masks=` for each [yolo]-layer, so for YOLOv4 the 1st-[yolo]-layer has anchors smaller than 30x30, 2nd smaller than 60x60, 3rd remaining, and vice versa for YOLOv3. Also you should change the `filters=(classes + 5)*<number of mask>` before each [yolo]-layer. If many of the calculated anchors do not fit under the appropriate layers - then just try using all the default anchors.

2. After training - for detection:

- Increase network-resolution by set in your `.cfg`-file (`height=608` and `width=608`) or (`height=832` and `width=832`) or (any value multiple of 32) - this increases the precision and makes it possible to detect small objects: [link](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L8-L9)

- it is not necessary to train the network again, just use `.weights`-file already trained for 416x416 resolution

- to get even greater accuracy you should train with higher resolution 608x608 or 832x832, note: if error `Out of memory` occurs then in `.cfg`-file you should increase `subdivisions=16`, 32 or 64: [link](https://github.com/AlexeyAB/darknet/blob/0039fd26786ab5f71d5af725fc18b3f521e7acfd/cfg/yolov3.cfg#L4)

## How to mark bounded boxes of objects and create annotation files

Here you can find repository with GUI-software for marking bounded boxes of objects and generating annotation files for Yolo v2 - v4: https://github.com/AlexeyAB/Yolo_mark

With example of: `train.txt`, `obj.names`, `obj.data`, `yolo-obj.cfg`, `air`1-6`.txt`, `bird`1-4`.txt` for 2 classes of objects (air, bird) and `train_obj.cmd` with example how to train this image-set with Yolo v2 - v4

Different tools for marking objects in images:

1. in C++: https://github.com/AlexeyAB/Yolo_mark
2. in Python: https://github.com/tzutalin/labelImg
3. in Python: https://github.com/Cartucho/OpenLabeling
4. in C++: https://www.ccoderun.ca/darkmark/
5. in JavaScript: https://github.com/opencv/cvat
6. in C++: https://github.com/jveitchmichaelis/deeplabel
7. in C#: https://github.com/BMW-InnovationLab/BMW-Labeltool-Lite
8. DL-Annotator for Windows ($30): [url](https://www.microsoft.com/en-us/p/dlannotator/9nsx79m7t8fn?activetab=pivot:overviewtab)
9. v7labs - the greatest cloud labeling tool ($1.5 per hour): https://www.v7labs.com/

## How to use Yolo as DLL and SO libraries

- on Linux
  - using `build.sh` or
  - build `darknet` using `cmake` or
  - set `LIBSO=1` in the `Makefile` and do `make`
- on Windows
  - using `build.ps1` or
  - build `darknet` using `cmake` or
  - compile `build\darknet\yolo_cpp_dll.sln` solution or `build\darknet\yolo_cpp_dll_no_gpu.sln` solution

There are 2 APIs:

- C API: https://github.com/AlexeyAB/darknet/blob/master/include/darknet.h
  - Python examples using the C API:
    - https://github.com/AlexeyAB/darknet/blob/master/darknet.py
    - https://github.com/AlexeyAB/darknet/blob/master/darknet_video.py

- C++ API: https://github.com/AlexeyAB/darknet/blob/master/include/yolo_v2_class.hpp
  - C++ example that uses C++ API: https://github.com/AlexeyAB/darknet/blob/master/src/yolo_console_dll.cpp

----

1. To compile Yolo as C++ DLL-file `yolo_cpp_dll.dll` - open the solution `build\darknet\yolo_cpp_dll.sln`, set **x64** and **Release**, and do the: Build -> Build yolo_cpp_dll
    - You should have installed **CUDA 10.2**
    - To use cuDNN do: (right click on project) -> properties -> C/C++ -> Preprocessor -> Preprocessor Definitions, and add at the beginning of line: `CUDNN;`

2. To use Yolo as DLL-file in your C++ console application - open the solution `build\darknet\yolo_console_dll.sln`, set **x64** and **Release**, and do the: Build -> Build yolo_console_dll

    - you can run your console application from Windows Explorer `build\darknet\x64\yolo_console_dll.exe`
    **use this command**: `yolo_console_dll.exe data/coco.names yolov4.cfg yolov4.weights test.mp4`

    - after launching your console application and entering the image file name - you will see info for each object:
    `<obj_id> <left_x> <top_y> <width> <height> <probability>`
    - to use simple OpenCV-GUI you should uncomment line `//#define OPENCV` in `yolo_console_dll.cpp`-file: [link](https://github.com/AlexeyAB/darknet/blob/a6cbaeecde40f91ddc3ea09aa26a03ab5bbf8ba8/src/yolo_console_dll.cpp#L5)
    - you can see source code of simple example for detection on the video file: [link](https://github.com/AlexeyAB/darknet/blob/ab1c5f9e57b4175f29a6ef39e7e68987d3e98704/src/yolo_console_dll.cpp#L75)

`yolo_cpp_dll.dll`-API: [link](https://github.com/AlexeyAB/darknet/blob/master/src/yolo_v2_class.hpp#L42)

```cpp
struct bbox_t {
    unsigned int x, y, w, h;    // (x,y) - top-left corner, (w, h) - width & height of bounded box
    float prob;                    // confidence - probability that the object was found correctly
    unsigned int obj_id;        // class of object - from range [0, classes-1]
    unsigned int track_id;        // tracking id for video (0 - untracked, 1 - inf - tracked object)
    unsigned int frames_counter;// counter of frames on which the object was detected
};

class Detector {
public:
        Detector(std::string cfg_filename, std::string weight_filename, int gpu_id = 0);
        ~Detector();

        std::vector<bbox_t> detect(std::string image_filename, float thresh = 0.2, bool use_mean = false);
        std::vector<bbox_t> detect(image_t img, float thresh = 0.2, bool use_mean = false);
        static image_t load_image(std::string image_filename);
        static void free_image(image_t m);

#ifdef OPENCV
        std::vector<bbox_t> detect(cv::Mat mat, float thresh = 0.2, bool use_mean = false);
        std::shared_ptr<image_t> mat_to_image_resize(cv::Mat mat) const;
#endif
};
```

## Citation

```
@misc{bochkovskiy2020yolov4,
      title={YOLOv4: Optimal Speed and Accuracy of Object Detection}, 
      author={Alexey Bochkovskiy and Chien-Yao Wang and Hong-Yuan Mark Liao},
      year={2020},
      eprint={2004.10934},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```

```
@InProceedings{Wang_2021_CVPR,
    author    = {Wang, Chien-Yao and Bochkovskiy, Alexey and Liao, Hong-Yuan Mark},
    title     = {{Scaled-YOLOv4}: Scaling Cross Stage Partial Network},
    booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
    month     = {June},
    year      = {2021},
    pages     = {13029-13038}
}
```
