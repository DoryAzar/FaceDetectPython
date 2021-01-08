# FaceDetect: Face detection & recognition
+ By: Dory Azar

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/banner.png)

<br />


## Content

+ [Project Status](https://github.com/DoryAzar/FaceDetectPython#project-status)
+ [Project Synopsis](https://github.com/DoryAzar/FaceDetectPython#project-synopsis)
+ [Resources](https://github.com/DoryAzar/FaceDetectPython#resources)
+ [Let's get started](https://github.com/DoryAzar/FaceDetectPython#lets-get-started)
+ [Let's get through the basics](https://github.com/DoryAzar/FaceDetectPython#lets-get-through-the-basics)
+ [Let's have some fun](https://github.com/DoryAzar/FaceDetectPython#lets-have-some-fun)
+ [Known Issues](https://github.com/DoryAzar/FaceDetectPython#known-issues)

<br />

## Project Status

**All the features described below have been implemented for this project. 
The core logic that we created can be found in [FaceDetect > facedetect.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/FaceDetect/facedetect.py)**

+ The foundation for the framework has been completed. FaceDetect has been implemented and packaged as a class that just needs to be imported for usage.
+ The framework allows reading images, videos and webcam streams
+ The framework allows for customization in 2 ways: 
    1. By providing a settings dictionary to the constructor to adjust the native features
    2. By extending the FaceDetect class to create more elaborate features
+ Face Detection has been implemented for all 3 media. The faces can now be detected in images, videos and live webcams
+ Ability to either draw rectangles around the detections or print them to the console has been implemented
+ Ability to extract detected faces into separate individual images has been implemented
+ Ability to detect facial features and draw them on top of either medium has been implemented
+ Ability to recognize faces in a video, webcam or image based on known faces provided as image inputs
+ Ability to identify recognized faces visually in a video, webcam or image
+ Ability to access detection and recognition data through extensibility for use in other programs 
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
+ Extract detected faces in separate images from the main image
+ Detect and draw facial features (eyes, noses, ears etc.) 
+ Recognize previously saved faces in an image, video or live webcam 
+ Generate live data from detections that can be shared and used in other programs (extensibility)

<br />

## Resources

+ **Face Recognition by Adam Geitgey**

    The face-recognition python library was created by Adam Geitgey. It uses deep learning for face detection and recognition using the Python **dlib** library. 
    
    [Face Recognition Documentation](https://face-recognition.readthedocs.io/en/latest/index.html)

+ **Open CV**: 
    
    While Open CV is a great library to implement face detection and recognition, it will mainly be used in this project for capturing a stream from the webcam.
    
    [Open CV Documentation](https://docs.opencv.org/master/) 

<br />

## Let's get started

### Environment

#### Python 3.8+ - Anaconda installation

One of the easiest ways to install Python is to use packaged distributions. Anaconda is one such distribution. 
If you are new to Python, we recommend that you install the Anaconda distribution.

[Download Anaconda](https://www.anaconda.com/download/)

If you already have Anaconda installed, all you need to do is to update it and make sure that you are using the latest version
of Python. You can do this from the command line or the terminal:
```
conda update conda
conda update anaconda
conda update python
```

#### Recommended Editor (IDE)

You can use any development environment or editor that you are comfortable with. In this course, we will be using PyCharm.
You can download the free Community Edition version.

[Download PyCharm](https://www.jetbrains.com/pycharm/download/)

### Requirements

There are several libraries and packages needed to run this program successfully.  We will provide the instructions on how to download on Mac/Linux machines:

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

#### PIL: Python Imaging Library

PIL is a native Python library. It is used in this project for image manipulations.

<br />

#### Numpy

Numpy is a native Python library. It is used for multi-dimensional array manipulations. It is used in this project for image array manipulations and matrices conversions

<br />

### Installation

You can install the FaceDetect application from github
```
git clone https://github.com/DoryAzar/FaceDetectPython
```


### FaceDetect Structure

The distribution comes with several scripts that are explained herewith:

+ **FaceDetect > facedetect.py**: `facedetect.py` is the core logic that we created that makes all the magic happen. 
The FaceDetect class and all its features and functionalities are implemented in this script. The script is open source
and can be modified and adjusted as needed within the boundaries of an MIT license.

+ **main scripts**: In the root folder of the distribution, there are several scripts that start with `main...`.
This series of scripts are examples of how FaceDetect is used in different situations.

+ **resources**: The `resources` folder contains example images to test out face detection and recognition. 
They are used by the main scripts.

+ **outputs**: The `outputs` folder contains screenshots of the example programs in action used for documentation purposes

<br />


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


#### Getting Started with FaceDetect

1. Start by creating a new python script file in the root of the distribution folder FaceDetectPython (similarly to main.py that is provided with the distribution)
2. The first thing that you need to do is to import the FaceDetect package:

    ```python
   
    from FaceDetect.facedetect import FaceDetect 
   
    ```
           
3. Instantiate a FaceDetect object. A `settings` dictionary  can  be passed  to the constructor to use different features of FaceDetect. Initially, we will not pass any to run FaceDetect in its default settings.
        
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
    
    
    # FaceDetect always generates a FaceDetect Exception
    except Exception as error:
        print(error)
    
    ```
 5. This will start a live stream from a webcam and human faces will be highlighted in the live stream with a blue rectangle surrounding them.
 This code can be found in the `main.py` script that is in the distribution
 
    We will explore more capabilities in the `Let's have some fun` section
  

<br />

#### Personalized Settings

FaceDetect gives you the flexibility to control its features through the use of a `settings` dictionary that can be passed to the constructor.

```python

facedetector = FaceDetect({'setting1':'value1', 'settings2': 'value2' # etc...})

```
Here is a list of all the settings and their potential values:

```python
'mode': 'video'             # Specifies if the input for detections is video (default) or image. Webcam is mode video

'draw': True                # Specifies whether or not the face detections should be drawn on the image or video. If set to False, nothing is displayed but detections are printed out in the console

'custom': ''                # If you wish to extend the FaceDetect class, specify the method that it needs to execute

'method': 'detect'          # detect (default) to run detections. 'recognize' to run face recognition

'print': True               # Prints the face locations and labels on the console. Set to False to disable

'face-extraction': False    # Extracts captures of the faces into their own images. Applicable only to mode image

'face-features': []         # Default no face features will be drawn. Specify what face features to draw in a list/array
                            # Possible values: 'face' (for the whole face), 'chin', 'left_eye', 'right_eye', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'top_lip', 'bottom_lip'

'known-faces': {}          # Setting need for facial recognition when 'method' is set to 'recognize'
                            # It is a dictionary of face labels and image paths associated. 
                            # For example: {'John': 'person1.png', 'Jane': 'person2.png'}
```


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
    
    # Pass the name of the custom method to execute at every detection cycle
    my_detector = MyDetector({'custom': <name of custom method>, 'method': 'detect' })
    
    ```
 5. Start the detections 
     
    ```python
    try:
        facedetector.start()
    
    # FaceDetect always generates a FaceDetect Exception
    except Exception as error:
        print(error)

    ```
 
 6. This will start a live stream from a webcam and human faces will be highlighted in the live stream with a blue rectangle surrounding them.
 On top of this, the code in the `main` function will be executed iteratively with every detection cycle.
 This code can be found in the `main_detect_webcam_extended.py` script that is in the distribution.

<br />

#### FaceDetect Properties for extensibility

Extending FaceDetect gives access to the methods and properties of the FaceDetect object. 
The following properties give access to real-time computations generated by the detection and recognition algorithm that could be used by the extended program.

```python

canvas                  # Access to the canvas that can be drawn on
stream                  # If it is a video or a webcam, it provides access to the video stream. If it is an image it gives access to the image array
settings                # Access to the applied settings
frame                   # Access to the capture frame from the stream if it is a video or a webcam
known_faces_encodings   # Face Encodings of known faces
known_faces_labels      # Face Labels of known faces
face_locations          # Access to the locations of the faces detected
face_encodings          # Access to face encodings / face signature
face_labels             # Access to face labels
detections              # Access to zipped version of (face_locations, label)
face_landmarks          # Access to face feature landmarks
face_extracts           # Access to face extracted face image arrays

```

<br  />


## Let's have some fun

In this section, we will explore all the features that we developed as part of this project and illustrate them through examples. 
The complete codes for all the examples are provided as part of the distributions. They all start with `main...` 
and they are located in the root folder.

Let's remember that the goal of the FaceDetect framework is to make it easy for novice developers to detect and recognize faces.
You will notice that many of the features are executed in a few lines of code.

**When you run the examples, an image or video canva opens up. You need to press 'q' on your keyboard to quit or you could just interrupt the program.**

### 1. Detect faces in an image

In this first example, we will provide an image to FaceDetect and it will draw rectangles around the faces it finds in
the image. 

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_detection_image_output.png)

```python

# Tell FaceDetect to use mode image
facedetector  = FaceDetect({'mode': 'image'})

# Tell FaceDetect to start detections on a desired image
try:
    facedetector.start('resources/people.jpg')  
except Exception as error:
    print(error)

```

> The complete code can be found in [main_detect_image.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_detection_image.py)

<br  />

### 2. Detect faces in a video or a webcam

FaceDetect also allows you to detect faces in videos or live webcams. Both these modalities are video streams 
and are initialized in the same way. The only difference is that a video file needs to be provided if the desire is to detect faces
in a pre-recorded video.

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_detection_webcam_output.png)

```python

# FaceDetect can be initialized in its default settings. It will run in mode video by default
facedetector = FaceDetect() # {'mode': 'video'} is the default setting
try:
    facedetector.start()  # webcam 
    # facedetector.start('<path to video>') for video

except Exception as error:
    print(error)

```

> The complete code can be found in [main_detect_webcam.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_detection_webcam.py)


<br />

### 3. Detection settings

Upon detection, FaceDetect draws rectangles around the detected faces in the canvas and prints the faces locations in the console (terminal or IDE console).
You can turn these settings:

```python

# Set draw and print to False
facedetect = FaceDetect({'draw': False, 'print': False})

```

<br />

### 4. Draw facial features on top of detected faces

FaceDetect allows you to draw facial features on top of detected faces in an image, video or webcam in simple lines of code.

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_facefeatures_image_output.png)

```python

facedetector = FaceDetect({'mode': 'image', 'face-features': ['face']}) # switch image to video for video or webcam
# you can also choose to draw particular features such as:
# 'chin', 'left_eye', 'right_eye', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip', 'top_lip', 'bottom_lip'

try:
    facedetector.start('resources/people.jpg') # leave empty for webcam or provide a video file

except Exception as error:
    print(error)

```

> The complete code can be found in [main_facefeatures_image.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_facefeatures_image.py)

<br />

### 5. Extract faces into images (image mode only)

FaceDetect provides you with a way to extract the faces from an image and load them as individual images that can be saved locally.

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_faceextract_image_output.png)

```python

# Set face extraction to true
facedetector = FaceDetect({'mode': 'image', 'face-extraction': True})

try:
    facedetector.start('resources/people.jpg')

except Exception as error:
    print(error)

```

> The complete code can be found in [main_faceextract_image.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_faceextract_image.py)

<br />

### 6. Recognize faces in an image

FaceDetect allows you to recognize faces in an image based on a dictionary of known people faces. 
It compares the detected faces to the faces signatures that it computes from the images provided. If it finds matches, it
will identify them on the image with a green rectangle along with the respective names (provided). The unknown faces will be
identified with a red rectangle labelled 'Unknown'.

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_recognize_image_output.png)

```python

# Set the method to recognize and provide a dictionary of known faces names and image path
facedetector = FaceDetect({'mode': 'image', 'method': 'recognize', 'known-faces': {'John': 'resources/person1.png',
                                                                                   'Jane': 'resources/person2.png'}})

try:
    facedetector.start('resources/people.jpg')

except Exception as error:
    print(error)

```

> The complete code can be found in [main_recognize_image.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_recognize_image.py)

<br  />

### 7. Recognize faces in a video or a webcam

FaceDetect allows you to recognize faces in a video or a webcam based on a dictionary of known people faces. 
If it finds matches, it  will identify them on the video or webcam canvas with a green rectangle along with the respective names (provided). 
The unknown faces will be identified with a red rectangle labelled 'Unknown'.

![](https://github.com/DoryAzar/FaceDetectPython/blob/master/outputs/main_recognize_video_output.png)

```python

# Set the method to recognize and provide a dictionary of known faces names and image path
facedetector = FaceDetect({'method': 'recognize', 'known-faces': {'John': 'resources/person1.png',
                                                                  'Jane': 'resources/person2.png'}})

try:
    facedetector.start()

except Exception as error:
    print(error)


```

> The complete code can be found in [main_recognize_video.py](https://github.com/DoryAzar/FaceDetectPython/blob/master/main_recognize_video.py)


<br />

## Known Issues

+ OpenCV is generating a warning upon loading a video, webcam or an image indicating that some plugins are not compiled against the right Qt binaries. This is due to the GUI that needs to be compiled and that depends heavily on X11 libraries. This issue did not cause any issue for the needs of FaceDetect. It could be resolved by making sure all libraries are compatible with the latest MacOs.

+ OpenCV is not the best for drawing on top of rich media. It is however the most robust in terms of computer graphics and is a fast video and image processor. 
