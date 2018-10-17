This repository contains python programs developed during iNTUition 5.0, a one-day hackathon held by NTU Open Source Society and iEEE Student Organization in Nanyang Technological University, Singapore.

# Base website:
## https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/

# More information on this project on DevPost
https://devpost.com/software/blinkception
# Installation instructions on Windows

1) Download the latest version of Anaconda from https://www.anaconda.com/download/

2) While installing, add Anaconda to PATH environment AND register Anaconda as default Python.

3) Open command prompt and execute the following instruction:

```conda create --name opencv-env python=3.7 ```

4) After installing whatever it prompts you to install, activate the environment you just created with:

``` activate opencv-env ```

5) Execute the following commands:

``` pip install numpy scipy matplotlib scikit-learn jupyter ```

``` pip install opencv-contrib-python ```

``` pip install cmake setuptools dlib ```

7) Now add the .dat file into the same directory as your project from https://github.com/AKSHAYUBHAT/TensorFace/blob/master/openface/models/dlib/shape_predictor_68_face_landmarks.dat

8) You are finally set! Run the program by executing the following command from your open cv environment:

``` python eyeControl.py --shape-predictor shape_predictor_68_face_landmarks.dat ```

Libraries for speech-to-text conversion and face-recognition:

``` pip install pyaudio (for mac) ```

``` pip install SpeechRecognition ```

``` pip install face_recognition ```

## Configuring your website
To implement Blinkception, you need to modify the classes of all the web elements you want the user to interact with. The class name rules are as follows:
1. ```bc-first``` and ``bc-1`` for the first element of each page.

2. ```bc-last``` for the last element of each page.

3. ``bc-1``, ``bc-2``, `bc-3`... for each element till the latest.

How the Blinkception program interacts with each element also depends on the class of the element. The following classes are supported:

1. `bc-button` for any element that is meant to be clicked (button, link, etc.)

2. `bc-slide` for any sliders.

3. `bc-input` when the element takes a text input.
