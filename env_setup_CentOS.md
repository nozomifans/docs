# Guide to setup a GPU environment

## 0. Hardware and OS
* Graphic Card: RTX 2080
* OS: CentOS Linux release 7.6.1810 (Core)

## 1. Install Graphic Card Driver
Ref: https://www.cyberciti.biz/faq/how-to-install-nvidia-driver-on-centos-7-linux/

* Not tested

## 2. Install CUDA

Ref: https://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html

* Not tested

Verify installation with samples: https://github.com/NVIDIA/cuda-samples

## 3. Install Cudnn

This step might be unnecessary because install tensorflow and pytorch via conda might setup cudnn as well.

Ref: https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html

### 3.1 Get CUDNN

https://developer.nvidia.com/rdp/cudnn-download

### 3.2 Install from a Tar File

* Navigate to your path directory containing the cuDNN Tar file

* Unzip the package: $ tar -xzvf cudnn-9.0-linux-x64-v7.tgz

* Copy files to the CUDA Toolkit directory and change the file permissions: 
  $ sudo cp cuda/include/cudnn.h /usr/local/cuda/include
  $ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
  $ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
  (In the cases of /usr/local/cuda/ is not the default cuda directory, copy also to the corresponding directories in the directory with the version number specified: /usr/local/cuda-10.0/ for example)

* Add paths to the default bash profile:
  vim ~/.bash_profile 
  and insert
  PATH=$PATH:/usr/local/cuda/bin/
  export $PATH
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64/
  export $LD_LIBRARY_PATH

### 3.3 Verify your installation with samples

https://github.com/Hardware-Alchemy/cuDNN-sample

## 4. Install Anaconda

### 4.1 Get Anaconda

Select Linux from https://www.anaconda.com/distribution/

### 4.2 Run Installer

$ bash <AnacondaInstaller>.sh

### 4.3 Follow the command line prompts

### 4.4 run conda init

conda init bash

### 4.5 Create your own conda virtual environment
conda create -n <env name> python=<python version>

## 5. Install Opencv-4.1.0

https://linuxize.com/post/how-to-install-opencv-on-centos-7/

### 5.1 Install with yum (version 2.4.5, not recommended see below): 

sudo yum install opencv opencv-devel opencv-python 

* YOLOv3 (darknet: https://github.com/pjreddie/darknet) cannot be successfully compiled with Opencv-2.4.5 installed with yum. If you already have opencv-2.4.5 installed in /usr/lib64/, you could remove with 
sudo yum erase opencv opencv-devel opencv-python
or change the priority of library to have /usr/local/lib64/ over /usr/lib64/ (check the order by  
gcc -m64 -Xlinker --verbose  2>/dev/null | grep SEARCH | sed 's/SEARCH_DIR("=\?\([^"]\+\)"); */\1\n/g'  | grep -vE '^$'
) to avoid conflicts. 

### 5.2 Compile from the source

* Install dependencies

$ sudo yum install epel-release git gcc gcc-c++ cmake3 qt5-qtbase-devel python python-devel python-pip cmake
$ sudo yum install python-devel numpy python34-numpy gtk2-devel libpng-devel jasper-devel openexr-devel libwebp-devel
$ sudo yum install libjpeg-turbo-devel libtiff-devel  libdc1394-devel tbb-devel eigen3-devel gstreamer-plugins-base-devel
$ sudo yum install freeglut-devel mesa-libGL mesa-libGL-devel  boost boost-thread boost-devel libv4l-devel

* create a directory and clone OpenCV and OpenCV contrib repo

$ mkdir ~/opencv_build && cd ~/opencv_build
$ git clone https://github.com/opencv/opencv.git
$ git clone https://github.com/opencv/opencv_contrib.git

* cd to the directory

$ cd ~/opencv_build/opencv && mkdir build && cd build

* Configure the OpenCV build

$ cmake3 -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_C_EXAMPLES=ON \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_build/opencv_contrib/modules \
    -D BUILD_EXAMPLES=ON ..

* Compile for 8 processors

$ make -j8

* Install 

$ sudo make install

* Create symlink

$ sudo ln -s /usr/local/lib64/pkgconfig/opencv4.pc /usr/share/pkgconfig/
$ sudo ldconfig

* Enable Python cv2

$ sudo ln -s ~/anaconda3/lib/python3.7/site-packages/cv2  ~/anaconda3/lib/python3.7/site-packages/

### 5.3 Verification

pkg-config --modversion opencv4

python -c "\
import cv2
print(cv2.__version__)" 

## 6. Install Tensorflow GPU and PyTorch

### 6.1 Install Tensorflow

$ conda install tensorflow-gpu

### 6.2 Install Pytorch

Visit https://pytorch.org/

Get your install string

or 

$ conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

## 7. Backup environment or import environment

There is a backup script in scripts/. If you want to import the environment, find the exported environment in env_yaml/ and run

conda env create -f <environment.yml>
