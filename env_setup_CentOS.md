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

* Unzip the package: 

  ```bash
  $ tar -xzvf cudnn-9.0-linux-x64-v7.tgz
  ```

* Copy files to the CUDA Toolkit directory and change the file permissions: 
  
  ```bash
  $ sudo cp cuda/include/cudnn.h /usr/local/cuda/include
  $ sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
$ sudo chmod a+r /usr/local/cuda/include/cudnn.h /usr/local/cuda/lib64/libcudnn*
  ```
  
  (In the cases of /usr/local/cuda/ is not the default cuda directory, copy also to the corresponding directories in the directory with the version number specified: /usr/local/cuda-10.0/ for example)
  
* Add paths to the default bash profile:
  
  ```bash
  vim ~/.bash_profile 
  ```
  
  and insert
  
  ```bash
  PATH=$PATH:/usr/local/cuda/bin/
  export $PATH
  LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64/
  export $LD_LIBRARY_PATH
  ```

### 3.3 Verify your installation with samples

https://github.com/Hardware-Alchemy/cuDNN-sample

## 4. Install Anaconda

### 4.1 Get Anaconda

Select Linux from https://www.anaconda.com/distribution/

### 4.2 Run Installer

```bash
$ bash <AnacondaInstaller>.sh
```

### 4.3 Follow the command line prompts

### 4.4 run conda init

```bash
$ conda init bash
```

### 4.5 Create your own conda virtual environment
```bash
$ conda create -n <env name> python=<python version>
```

## 5. Install Tensorflow GPU and PyTorch

### 5.1 Install Tensorflow

```bash
$ conda install tensorflow-gpu
```

### 5.2 Install Pytorch

Visit https://pytorch.org/

Get your install string

or 

```bash
$ conda install pytorch torchvision cudatoolkit=10.0 -c pytorch
```

## 6. Backup environment or import environment

There is a backup script in scripts/. If you want to import the environment, find the exported environment in env_yaml/ and run

```bash
$ conda env create -f <environment.yml>
```