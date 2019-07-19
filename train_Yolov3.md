# Train YOLOv3 for Kaggle imagenet object localization

Project: [https://www.kaggle.com/c/imagenet-object-localization-challenge](https://www.kaggle.com/c/imagenet-object-localization-challenge)

YOLOv3: https://pjreddie.com/darknet/yolo/

YOLO source code: https://github.com/pjreddie/darknet

Steps following: https://github.com/mingweihe/ImageNet

## 0. Set up environment

Follow env_setup.md for Ubuntu or env_setup_CentOS.md for CentOS 7 machines.

## 1. Download Dataset

Download competition dataset using kaggle api: https://github.com/Kaggle/kaggle-api

```bash
$ pip install kaggle --upgrade
```

To obtain APT credentials, please follow the instruction on https://github.com/Kaggle/kaggle-api. Once done, you will have a `kaggle.json` downloaded. 

Create a directory in your home

```bash
$ mkdir ~/.kaggle
```

and move the credentials into the directory,

```bash
$ mv kaggle.json ~/.kaggle/
```

For security, you can block the read access of other users by

```bash
$ chmod 600 ~/.kaggle/kaggle.json
```

You can also choose to export your Kaggle username and token to the environment:

```bash
$ export KAGGLE_USERNAME=datadinosaur
$ export KAGGLE_KEY=xxxxxxxxxxxxxx
```

Download the dataset with command lines:

```bash
$ kaggle competitions {list, files, download, submit, submissions, leaderboard}
$ kaggle datasets {list, files, download, create, version, init}
$ kaggle kernels {list, init, push, pull, output, status}
$ kaggle config {view, set, unset}
```

For the ImageNet Object Localization competition

```bash
$ kaggle competitions download imagenet-object-localization-challenge
```

* Dataset is about 155G and unzip is necessary later, please select the directory with enough storage.

## 2. Install Opencv-4.1.0 for CentOS

Origin: https://linuxize.com/post/how-to-install-opencv-on-centos-7/

### 2.1 Install with yum (version 2.4.5, not recommended see below): 

```bash
$ sudo yum install opencv opencv-devel opencv-python
```

- YOLOv3 cannot be successfully compiled with Opencv-2.4 installed with yum. If you already have opencv-2.4 installed in /usr/lib64/, you could remove with 

  ```bash
  $ sudo yum erase opencv opencv-devel opencv-python
  ```

  or change the priority of library to have /usr/local/lib64/ over /usr/lib64/ to avoid conflicts. 

  Check the order by 

  ```bash
  $ gcc -m64 -Xlinker --verbose  2>/dev/null | grep SEARCH | sed 's/SEARCH_DIR("=\?\([^"]\+\)"); */\1\n/g'  | grep -vE '^$'
  ```

### 2.2 Compile from the source

- Install dependencies

```bash
$ sudo yum install epel-release git gcc gcc-c++ cmake3 qt5-qtbase-devel python python-devel python-pip cmake
$ sudo yum install python-devel numpy python34-numpy gtk2-devel libpng-devel jasper-devel openexr-devel libwebp-devel
$ sudo yum install libjpeg-turbo-devel libtiff-devel  libdc1394-devel tbb-devel eigen3-devel gstreamer-plugins-base-devel
$ sudo yum install freeglut-devel mesa-libGL mesa-libGL-devel  boost boost-thread boost-devel libv4l-devel
```

- Create a directory and clone OpenCV and OpenCV contrib repo

```bash
$ mkdir ~/opencv_build && cd ~/opencv_build
$ git clone https://github.com/opencv/opencv.git
$ git clone https://github.com/opencv/opencv_contrib.git
```

- cd to the directory

```bash
$ cd ~/opencv_build/opencv && mkdir build && cd build
```

- Configure the OpenCV build

```bash
$ cmake3 -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..
```

- Compile for 8 processors

```bash
$ make -j8
```

- Install 

```bash
$ sudo make install
```

- Create symlink

```bash
$ sudo ln -s /usr/local/lib64/pkgconfig/opencv4.pc /usr/share/pkgconfig/
$ sudo ldconfig
```

- Enable Python cv2

```bash
$ sudo ln -s ~/anaconda3/lib/python3.7/site-packages/cv2  ~/anaconda3/lib/python3.7/site-packages/
```

link to the directory the python library is called, the example here calls the python library managed in anaconda3.

### 2.3 Verify installation

```bash
$ pkg-config --modversion opencv4
```

```bash
$ python -c "\
  import cv2
  print(cv2.__version__)" 
```

## 3. Install YOLO 

### 3.1 Download YOLOv3

```bash
$ git clone https://github.com/pjreddie/darknet
```

If you are using OpenCV4, download:

```bash
$ git clone https://github.com/tiagoshibata/darknet/
```

### 3.2 Compile

```bash
$ cd darknet
$ make
```

Modify Makefile and compile with OpenCV:

```bash
$ cd darknet
$ sed -i 's/GPU=./GPU=1/' Makefile
$ sed -i 's/CUDNN=./CUDNN=0/' Makefile
$ sed -i 's/OPENCV=./OPENCV=1/' Makefile
$ sed -i 's/OPENMP=./OPENMP=1/' Makefile
$ sed -i 's/DEBUG=./DEBUG=0/' Makefile
$ make
```

* If you fail to compile with error like 

```cpp
IplImage *image_to_ipl(image+im)
  ^~~~~~~~ undefined IplImage
```

Very likely you're having conflicts between different OpenCV versions. Please refer to Section 2 to choose the version works for you. OpenCV4 compiled from the source code is recommended for CentOS. You then need to download the right version of darknet, see above.

### 3.3 Test run

```bash
$ wget https://pjreddie.com/media/files/yolov3.weights
$ ./darknet detector test cfg/coco.data cfg/yolov3.cfg yolov3.weights data/dog.jpg
```

## 4 Train your darknet for the object detection

### 4.1 Preprocess training data

```bash
$ cd <directory/to/downloaded/data>
$ tar -zxvf imagenet_object_localization.tar.gz
```

Delete package to save disk space

```bash
$ rm imagenet_object_localization.tar.gz
```

Prepare data
```bash
$ unzip LOC_synset_mapping.txt.zip
$ mkdir ILSVRC/Data/CLS-LOC/train/images
$ mv ILSVRC/Data/CLS-LOC/train/n* ILSVRC/Data/CLS-LOC/train/images/
$ mv ILSVRC/Data/CLS-LOC/val/ ILSVRC/Data/CLS-LOC/images
$ mkdir ILSVRC/Data/CLS-LOC/val/
$ mv ILSVRC/Data/CLS-LOC/images ILSVRC/Data/CLS-LOC/val/images
```

Run script by mingweihe@github to set data

```bash
$ git clone https://github.com/mingweihe/ImageNet
$ pip3 install pandas
$ pip3 install pathlib
$ cd ImageNet
```

Generate formatted label files for training data
```bash
$ python3 generate_labels.py ../LOC_synset_mapping.txt ../ILSVRC/Annotations/CLS-LOC/train ../ILSVRC/Data/CLS-LOC/train/labels 1
```

Generate formatted label files for validation data
```bash
$ python3 generate_labels.py ../LOC_synset_mapping.txt ../ILSVRC/Annotations/CLS-LOC/val ../ILSVRC/Data/CLS-LOC/val/labels 0
```

Change the generated ILSVRC.data with proper directories to darknet and dataset, 

```
classes= 1000
train = <directory/to/darknet>/darknet/data/inet.train.list
valid = <directory/to/darknet>/darknet/data/inet.val.list
names = <directory/to/downloaded/data>/LOC_synset_mapping.txt
backup = <directory/to/darknet>/darknet/backup/
```

List the data with corrected file type in the darknet data index

```bash
$ cd <directory/to/downloaded/data>
$ find `pwd`/ILSVRC/Data/CLS-LOC/train/labels/ -name \*.txt > ~/darknet/data/inet.train.list
$ sed -i 's/\.txt/\.JPEG/g' ~/darknet/data/inet.train.list
$ sed -i 's/labels/images/g' ~/darknet/data/inet.train.list
$ find `pwd`/ILSVRC/Data/CLS-LOC/val/labels/ -name \*.txt > ~/darknet/data/inet.val.list
$ sed -i 's/\.txt/\.JPEG/g' ~/darknet/data/inet.val.list
$ sed -i 's/labels/images/g' ~/darknet/data/inet.val.list
```

if /darknet/ is in home directory ~.

### 4.2 Obtain pretrained weights for darknet

```bash
$ cd ~/darknet
$ wget https://pjreddie.com/media/files/darknet53.conv.74
```

### 4.3 Train YOLOv3 darknet

```bash
$ ./darknet detector train <directory/to/downloaded/data>/ImageNet/ILSVRC.data <directory/to/downloaded/data>/ImageNet/yolov3-ILSVRC.cfg darknet53.conv.74
```

Or restart training from a checkpoint:

```bash
$ ./darknet detector train <directory/to/downloaded/data>/ImageNet/ILSVRC.data <directory/to/downloaded/data>/ImageNet/yolov3-ILSVRC.cfg backup/yolov3-ILSVRC.backup
```

Train with multiple GPUs (for four GPUs)

```bash
$ ./darknet detector train <directory/to/downloaded/data>/ImageNet/ILSVRC.data <directory/to/downloaded/data>/ImageNet/yolov3-ILSVRC.cfg backup/yolov3-ILSVRC.backup -gpus 0,1,2,3
```

* Note: If you get error messages like

* ```
  CUDA Error: out of memory
  ```

  please choose smaller batch value or larger subdivisions in yolov3-ILSVRC.cfg

  ```
  batch=32
  subdivisions=8
  ```

  works on GeForce RTX 2080.

Train without connection using nohup

```bash
$ nohup ./darknet detector train <directory/to/downloaded/data>/ImageNet/ILSVRC.data <directory/to/downloaded/data>/ImageNet/yolov3-ILSVRC.cfg backup/yolov3-ILSVRC.backup -gpus 0,1,2,3 &
```

All output including the training process will be print in the file **nohup.out**. 

## 5 Predict and submit results

### 5.1 Predict object detection to a csv file

cd to the directory of downloaded data

```bash
$ unzip LOC_sample_submission.csv.zip
$ mkdir submissions
$ python3 ImageNet/predict.py
```

* Before running the script, please change the paths of the darknet and image data to the proper directories in the `predict.py`. 

### 5.2 Submit prediction using Kaggle-Api

If you have downloaded Kaggle-API properly as explained in Section 1, you can use the same API to submit the prediction.

```bash
$ kaggle competitions submit imagenet-object-localization-challenge -f <your csv file to submit> -m "Your comment of the submission"
```

## 6. Improve accuracy

Augmentation

Ensembling