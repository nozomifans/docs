# Guide to setup a GPU environment

## 0. Hardware and OS
* Graphic Card: RTX 2070
* OS: Ubuntu 18.04 x86_64

## 1. Install Graphic Card Driver
Ref: https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-18-04-bionic-beaver-linux

Step 1: Check available and recommand driver
$ ubuntu-drivers devices

Step 2: Install through sudo apt
$ sudo apt install nvidia-<version>

Step 3: Reboot system

## 2. Install CUDA

Ref: https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&target_distro=Ubuntu&target_version=1804&target_type=deblocal

## 3. Install Cudnn

This step might be unnecessary because install tensorflow and pytorch via conda might setup cudnn as well.

Ref: https://docs.nvidia.com/deeplearning/sdk/cudnn-install/index.html

Step 1: Get CUDNN

https://developer.nvidia.com/rdp/cudnn-download

Step 2: Run *.deb

sudo dpkg -i libcudnn7_7.0.3.11-1+cuda9.0_amd64.deb
sudo dpkg -i libcudnn7-devel_7.0.3.11-1+cuda9.0_amd64.deb
sudo dpkg -i libcudnn7-doc_7.0.3.11-1+cuda9.0_amd64.deb

## 4. Install Anaconda

Step 1. Get Anaconda

Select Linux from https://www.anaconda.com/distribution/

Step 2. Run Installer

$ sh <AnacondaInstaller>.sh

Step 3. Follow the command line prompts

Step 4. run conda init

conda init bash

Step 5. Create your own conda virtual environment
conda create -n <env name> python=<python version>

## 5. Install Tensorflow GPU and PyTorch

### 5.1 Install Tensorflow

$ conda install tensorflow-gpu

### 5.2 Install Pytorch

Visit https://pytorch.org/

Get your install string

or 

$ conda install pytorch torchvision cudatoolkit=10.0 -c pytorch

## 6. Backup environment or import environment

There is a backup script in scripts/. If you want to import the environment, find the exported environment in env_yaml/ and run

conda env create -f <environment.yml>
