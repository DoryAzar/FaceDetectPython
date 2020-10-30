# main.py
# Usage: %python main.py

# Import the FaceDetect class
from FaceDetect.facedetect import FaceDetect


# Initialize FaceDetect
# Params:
# - settings (optional): Dictionary with settings to be passed to the FaceDetector
#   * mode:  image or video (default)
#   * custom: False (default). Set to True when the FaceDetect class is extended
#   * method: call native callback methods during detection or bypass with a custom method
#   * draw: draws the detection on the canvas if set to True (default)
#
class MyDetector(FaceDetect):
    def recognize(self):
        print(self.detections)


facedetector = FaceDetect({'mode': 'image'})

try:
    # When the start method is not given an image or video path, it starts the webcam
    # For Image file: facedetector.start('<path to image file>')
    # For Video: facedetector.start('<path to video file>')
    facedetector.start('resources/people.jpg')


# FaceDetect always generates TypeError exceptions
except TypeError as error:
    print(error)
