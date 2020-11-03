# FaceDetect: Face detection & recognition
+ By: Dory Azar
+ Video Demo: 
+ Live Demo: 

![](https://github.com/DoryAzar/e28/blob/master/independent-study/resources/facedetect1.png)

<br />

## Content

+ [Project Status](https://github.com/DoryAzar/FaceDetectPython#project-status)
+ [Project Synopsis](https://github.com/DoryAzar/FaceDetectPython#project-synopsis)
+ [Resources](https://github.com/DoryAzar/FaceDetectPython#resources)
+ [Let's get started](https://github.com/DoryAzar/FaceDetectPython#lets-get-started)
+ [Let's get through the basics](https://github.com/DoryAzar/FaceDetectPython#lets-get-through-the-basics)
+ [Let's have some fun](https://github.com/DoryAzar/FaceDetectPython#lets-have-some-fun)
+ [Final Thoughts](https://github.com/DoryAzar/FaceDetectPython#final-thoughts)
+ [Known Issues](https://github.com/DoryAzar/FaceDetectPython#known-issues)

<br />

## Project Status

+ The foundation for the framework has been completed. FaceDetect has been implemented and packaged as a class that just needs to be imported for usage.
+ The framework allows reading images, videos and webcam streams
+ The framework allows for customization in 2 ways: 
    1. By providing a settings dictionary to the constructor to adjust the native features
    2. By extending the FaceDetect class to create more elaborate features
+ Face Detection has been implemented for all 3 media. The faces can now be detected in images, videos and live webcams
+ Detections are either drawn on the medium (default setting) or the face locations can be printed out in the console
+ All the features are documented in the README


<br />

## Project Synopsis

Detecting human faces and recognizing faces and facial expressions have always been an area of interest for different applications such as games, utilities and even security. With the advancement of machine learning, the techniques of detection and recognition have become more accurate and precise than ever before.

However, machine learning remains a relatively complex field that could feel intimidating or inaccessible to many of us. Luckily, in the last couple of years, several organizations and open source communities have been developing tools and libraries that help abstract the complex mathematical algorithms in order to encourage developers to easily create learning models and train them using any programming languages. 

As part of this project, we will create a Face Detection framework in Python built on top of the work of several open source projects and models with the hope to reduce the entry barrier for developers and to encourage them to focus more on developing innovative applications that make use of face detection and recognition.

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

## Resources

+ **Face Recognition by Adam Geitgey**

    The face-recognition python library was created by Adam Geitgey. It uses deep learning for face detection and recognition using the Python **dlib** library. 
    
    [Face Recognition Documentation](https://face-recognition.readthedocs.io/en/latest/index.html)

+ **Open CV**: 
    
    While Open CV is a great library to implement face detection and recognition, it will mainly be used in this project for capture a stream from the webcam.
    
    [Open CV Documentation](https://docs.opencv.org/master/) 

<br />

## Let's get started

### Requirements

There are several libraries and packages needed to run this program successfully.  We will provide the instructions on how to download on a Mac/Linux machines:

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

### Testing the installation

The `main.py` script provided with the distribution provides an initial boiler plate main to test out the installation.
It can be run either in the terminal or using Anaconda PyCharm

+ Using the terminal

    ```
       python main.py
    ```
+ Using Anaconda PyCharm

    - After installing the dependencies, set up a new Anaconda project with a Python 3.8 Virtual Environment. 
    - Make sure to create a fresh new virtual environment in the folder containing the FaceDetect distribution
    - Run `main.py`


<br />


## Let's get through the basics

### Understanding Face detection and recognition

Detection and Recognition are two different concepts. While both use machine learning and neural networks in particular, they achieve different things. Understanding the distinction is key to better understanding how the FaceDetect framework operates.

+ **Face detection**: Face detection is about identifying a human face among all other "things" perceived through either an image or a video. So for example, a picture or a video can have people, objects, scenery etc... Face detection is when the system is capable of pointing out the presence of a human face among all those other things.

+ **Face recognition**: Recognition is about identifying who the human face is among all other faces and things perceived. So for example, Face recognition is when the system is capable of pointing out "Flash" among all other superheroes in a picture or a video.

<br />

### Understanding the framework

FaceDetect relies on an important principle: "First you detect then you do something with the detections". 
What we do with the detections is really what this framework is all about.
On one hand, it provides cool native features such as drawing rectangles around them, labeling them, recognizing the faces etc.
On the other, it provides a way to extend its capabilities by writing custom features

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_detection_webcam_output.png)

#### Getting Started with FaceDetect

1. Start by creating a new python script file in the root of the distribution folder FaceDetectPython (similarly to main.py that is provided with the distribution)
2. The first thing that you need to do is to import the FaceDetect package:

    ```python
   
    from FaceDetect.facedetect import FaceDetect 
   
    ```
           
3. Instantiate a FaceDetect object. A `settings` string in a JSON format can be passed to the constructor to use different features of FaceDetect. Initially, we will not pass any to run FaceDetect in its default settings.
        
     ```python
   
     # Instantiate a FaceDetect with the default settings
     facedetector = FaceDetect()
   
4. Start the detections 

    ```python
    try:
        # When the start method is not given an image or video path, it starts the webcam
        # For Image file: facedetector.start('<path to image file>')
        # For Video: facedetector.start('<path to video file>')
        # Press 'q' to exit
        facedetector.start()
    
    
    # FaceDetect always generates TypeError exceptions
    except TypeError as error:
        print(error)
    
    ```
 5. This will start a live stream from a webcam and human faces will be highlighted in the live stream with a blue rectangle surrounding them.
 This code can be found in the `main.py` script that is in the distribution
 
    We will explore more capabilities in the `Let's have some fun` section
  

<br />

#### Extending the capabilities of FaceDetect

FaceDetect provides you with a way to extend its capabilities by implementing your own code on top of the package.
In order to do that you will need to extend the FaceDetect class.

1. Create a new script file in the FaceDetectPython root folder
2. Import the FaceDetect package:

    ```python
   
    from FaceDetect.facedetect import FaceDetect 
   
    ```
3. Create a class that extends FaceDetect. That class extends FaceDetect and inherits all of its properties and methods. You can add additional methods and properties.
    ```python
    class MyDetector(FaceDetect):
   
       # example of a method that print the detections property from FaceDetect
        def main(self):
            print(self.detections)
    
    ```
4. Instantiate an object of this created class
    ```python
    
    # Set custom to True and pass the name of the method to its constructor
    my_detector = MyDetector({'custom': True, 'method': 'main' })
    
    ```
 5. Start the detections 
     
    ```python
    try:
        facedetector.start()
    
    # FaceDetect always generates TypeError exceptions
    except TypeError as error:
        print(error)

    ```
 
 6. This will start a live stream from a webcam and human faces will be highlighted in the live stream with a blue rectangle surrounding them.
 On top of this, the code in the `main` function will be executed iteratively with every detection cycle.
 This code can be found in the `main_detect_webcam_extended.py` script that is in the distribution.

<br />

#### Personalized Settings

FaceDetect gives you the flexibility to control its features through the use of a `settings` dictionary that can be passed to the constructor.

```python

facedetector = FaceDetect({'setting1':'value1', 'settings2': 'value2' # etc...})

```
Here is a list of all the settings and their potential values:

```python
'mode': 'video'     # Specifies if the input for detections is video (default) or image. Webcam is mode video
'draw': True        # Specifies whether or not the face detections should be drawn on the image or video. If set to False, nothing is displayed but detections are printed out in the console
'custom': False     # If you wish to extend the FaceDetect class, set to True (check the next section for more information)
'method': 'detect'  # detect (default) to run detections. 'recognize' to run face recognition
                    # If custom is set to True, the method setting will specify the callback method that you define in the extended class

```


<br />


## Let's have some fun



<br />



## Final Thoughts



<br />

## Known Issues

+ OpenCV is generating a warning upon loading a video, webcam or an image indicating that some plugins are not compiled against the right Qt binaries. This is due to the GUI that needs to be compiled and that depends heavily on X11 libraries. This issue did not cause any issue for the needs of FaceDetect. It could be resolved by making sure all libraries are compatible with the latest MacOs.

+ OpenCV is not the best for drawing on top of rich media. It is however the most robust in terms of computer graphics and is a fast video and image processor. 
