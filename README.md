# Control relays by hand gestures using raspberry pi 3/4

This is a sample program that recognizes hand signs and finger count gestures with a simple MLP using the detected key points with mediapipe and python.(I used raspberry pi 4 model b)

This repository contains the following contents.
  * module.py (this contain the all the necessary functions) 
  * Project.py (main function)

To run this program
```
python Project.py
```
## What You Need
 *  Raspberry Pi 4 Model B
 *  Micro SD Card (That contain the OS)
 *  Power Supply
 *  pi camera

If you [set up](https://www.tomshardware.com/reviews/raspberry-pi-headless-setup-how-to,6028.html) a headless raspberry pi following things won't need,
 *  Monitor
 *  HDMI Cord
 *  Mouse and Keyboard

When setting up Raspberry Pi,
### 1. Install Raspberry Pi 'Buster' OS.
First you have to install Raspberry Pi 'Buster' OS by using raspberry pi imager.

<img src="https://github.com/Kawyanethma/control-relay-by-hand-gesture/assets/92635894/05cb4f34-ea1d-4d46-a6e3-9b079b65781f" width=400>

### 2. Setting up configuration for camera.
Open up the Raspberry Pi configuration menu and enable the camera found under the interfaces tab and restart.

<img src="https://github.com/Kawyanethma/control-relay-by-hand-gesture/assets/92635894/8fe832a1-ff9c-435f-82b6-856dd0ea6a2c " width=400>

### 3. Now expand the swapfile before next steps.
   
> To do this, type into terminal this line.
```
sudo nano /etc/dphys-swapfile
```
then change the number on **CONF_SWAPSIZE = 100 to CONF_SWAPSIZE=2048**.  
> Having done this press Ctrl-X, Y, and then Enter Key to save these changes.

### 4. Setting Up Open-CV on Raspberry Pi 'Buster' OS
Copy and paste each command into your Pi’s terminal, press Enter, and allow it to finish before moving onto the next command.

> If ever prompted, “Do you want to continue? (y/n)” press Y and then the Enter key to continue the process.

```
sudo apt-get update && sudo apt-get upgrade
```
```
sudo apt-get install build-essential cmake pkg-config
```
```
sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
```
```
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
```
```
sudo apt-get install libxvidcore-dev libx264-dev
```
```
sudo apt-get install libgtk2.0-dev libgtk-3-dev
```
```
sudo apt-get install libatlas-base-dev gfortran
```
```
sudo pip3 install numpy
```
```
wget -O opencv.zip https://github.com/opencv/opencv/archive/4.4.0.zip
```
```
wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.4.0.zip
```
```
unzip opencv.zip
```
```
unzip opencv_contrib.zip
```
```
cd ~/opencv-4.4.0/
```
```
mkdir build
```
```
cd build
```
```
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-4.4.0/modules \
-D BUILD_EXAMPLES=ON ..
```
```
make -j $(nproc)
```

**NOTE :**
This ` make ` Command will **take over an hour to install** .
> If it fails at any point and you receive a message like ` make: *** [Makefile:163: all] Error 2 ` <br>just re-type and enter the above line ` make -j $(nproc) `.

### 5. Final Steps (Setting Up mediapipe)

This package is able to identify, locate and provide a unique number for each joint on both your hands. 

> This has specific package that work with Raspberry Pi 3
```
sudo pip3 install mediapipe-rpi3
```
> This has specific package that work with Raspberry Pi 4
```
sudo pip3 install mediapipe-rpi4
```
> Following packages are common for both Raspberry Pi 3/4
```
sudo pip3 install gtts
```
```
sudo apt install mpg321
```

**Troubleshooting :**<br>
If you're running into following Compatability Issue.<br>
`RuntimeError: module compiled against API version 0xe but this version of numpy is 0xd `<br>
> Type and enter the following into your terminal to fix it

```
sudo pip install numpy --upgrade --ignore-installed
```
```
sudo pip3 install numpy --upgrade --ignore-installed
```
