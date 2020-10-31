# main_detection_webcam.py
# Usage: %python main_detection_webcam.py

from FaceDetect.facedetect import FaceDetect

# Import the FaceDetect class


# Initialize FaceDetect
# Params:
# - settings (optional): Dictionary with settings to be passed to the FaceDetector
#   * mode:  image or video (default)
#   * custom: False (default). Set to True when the FaceDetect class is extended
#   * method: call native callback methods during detection or bypass with a custom method
#   * draw: draws the detection on the canvas if set to True (default)
#


# Passing settings (the default ones are being passed for comparison purposes with main.py)
facedetector = FaceDetect({'mode': 'video', 'custom': True, 'method': 'detect', 'draw': True})

try:
    # When the start method is not given an image or video path, it starts the webcam
    # For Image file: facedetector.start('<path to image file>')
    # For Video: facedetector.start('<path to video file>')
    # Press 'q' to exit
    facedetector.start()


# FaceDetect always generates TypeError exceptions
except TypeError as error:
    print(error)
