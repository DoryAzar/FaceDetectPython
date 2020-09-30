# FaceDetect: Face detection & recognition
+ By: Dory Azar
+ Video Demo: 
+ Live Demo: 

![](https://github.com/DoryAzar/e28/blob/master/independent-study/resources/facedetect1.png)

<br />

## Content

+ [What is it?](https://github.com/DoryAzar/FaceDetectPython#what-is-it)
+ [Credits & Resources](https://github.com/DoryAzar/FaceDetectPython#credits--resources)
+ [Let's get started](https://github.com/DoryAzar/FaceDetectPython#lets-get-started)
+ [Let's get through the basics](https://github.com/DoryAzar/FaceDetectPython#lets-get-through-the-basics)
+ [Let's have some fun](https://github.com/DoryAzar/FaceDetectPython#lets-have-some-fun)
+ [Final Thoughts](https://github.com/DoryAzar/FaceDetectPython#final-thoughts)
+ [Known Issues](https://github.com/DoryAzar/FaceDetectPython#known-issues)

<br />

## What is it?

Detecting human faces and recognizing faces and facial expressions have always been an area of interest for different applications such as games, utilities and even security. With the advancement of machine learning, the techniques of detection and recognition have become more accurate and precise than ever before.

However, machine learning remains a relatively complex field that could feel intimidating or inaccessible to many of us. Luckily, in the last couple of years, several organizations and open source communities have been developing tools and libraries that help abstract the complex mathematical algorithms in order to encourage developers to easily create learning models and train them using any programming languages. 

As part of this project, we will create a Python framework built on top of the work of several open source projects and models with the hope to reduce the entry barrier for developers and to encourage them to focus more on developing innovative applications that make use of face detection and recognition.

Artificial Intelligence (AI) and Machine Learning in particular don't have to be difficult and we hope that the FaceDetect framework gives developers the means to include face detection and recognition in a seamless way in their applications.


The framework aims to provide an easy way for developers to  detect faces, facial features and recognize faces from an image, a video or a live cam stream. 

Here are some of the features that we are considering. We will try to do as many as time allows:
+ Detect faces in an image, video or live webcam
+ Detect facial features (eyes, noses, ears etc.) 
+ Line drawings of faces detected in images, videos or live webcams
+ Recognize previously saved faces in an image, video or live webcam 
+ Create a face signature from a live webcam and recognize that face in the live stream
+ Generate live detections in a JSON format for extensibility

<br />

## Credits & Resources

+ **Face Recognition by Adam Geitgey**

    The face-recognition python library was created by Adam Geitgey. It uses deep learning for face detection and recognition using the Python **dlib** library. 
    
    [Face Recognition Documentation](https://face-recognition.readthedocs.io/en/latest/index.html)

+ **Open CV**: 
    
    While Open CV is a great library to implement face detection and recognition, it will mainly be used in this project for capture a stream from the webcam.
    
    [Open CV Documentation](https://docs.opencv.org/master/) 

<br />

## Let's get started

### Requirements

There are several libraries and packages needed to run this program successfully.  We will provide the instructions for how to download on a Mac/Linux machines:

#### Python 3.8+
This program and its dependencies have only been tested with Python 3.8 

#### cmake

In order to successfully install and build all the dependencies locally, CMake needs to be installed for python
```bash
    // Use Homebrew to install Cmake
    brew install cmake
```
#### dlib 

C++ library that provides machine learning tools to be used in several other languages such as python.
```
    // use pip to install dlib
    python -m pip install dlib
``` 
#### face-recognition

library built on top of dlib that facilitates the usage of face detection and face recognition
```
    // use pip to install face-recognition
    pip install face-recognition
```
#### Open CV

Open source computer vision library that provides machine AI vision
```
    //use pip to install opencv
    pip install opencv-python
```
<br />

### Installation

You can install the FaceDetect application from github
```
git clone https://github.com/DoryAzar/FaceDetectPython
```

### Running the program

+ Using the terminal

    ```
       python facedetect.py
    ```
+ Using Anaconda

    - After installing the dependencies, set up a new Anaconda project with a Python 3.8 Virtual Environment. 
    
    - Run `facedetect.py`


<br />


## Let's get through the basics

### Understanding Face detection and recognition

Detection and Recognition are two different concepts. While both use machine learning and neural networks in particular, they achieve different things. Understanding the distinction is key to better understanding how the FaceDetect framework operates.

+ **Face detection**: Face detection is about identifying a human face among all other "things" perceived through either an image or a video. So for example, a picture or a video can have people, objects, scenery etc... Face detection is when the system is capable of pointing out the presence of a human face among all those other things.

+ **Face recognition**: Recognition is about identifying who the human face is among all other faces and things perceived. So for example, Face recognition is when the system is capable of pointing out "Flash" among all other superheroes in a picture or a video.


<br />

## Let's have some fun



<br />



## Final Thoughts



<br />

## Known Issues



