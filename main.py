# main.py
# Usage: %python main.py

# Import the FaceDetect class
from FaceDetect.facedetect import FaceDetect

# Initialize FaceDetect
# Params:
# - settings (optional): Dictionary with settings to be passed to the FaceDetector
# - app (optional): Callback function that can be defined and called from the main
# and that will run at every detection interval

facedetector = FaceDetect()

try:
    # When the start method is not given an image or video path, it starts the webcam
    # For Image file: facedetector.start('<path to image file>')
    # For Video: facedetector.start('<path to video file>')
    facedetector.start()


# FaceDetect always generates TypeError exceptions
except TypeError as error:
    print(error)
