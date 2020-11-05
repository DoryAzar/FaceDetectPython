# main_detection_webcam.py
# Usage: %python main_detection_webcam_extended.py

# Import the FaceDetect class
from FaceDetect.facedetect import FaceDetect


# Initialize FaceDetect
# Params:
# - settings (optional): Dictionary with settings to be passed to the FaceDetector
#   * mode:  image or video (default)
#   * custom: False (default). Set to True when the FaceDetect class is extended
#   * method: call native callback methods during detection or bypass with a custom method
#   * draw: draws the detection on the canvas if set to True (default)
#   * print: prints the face locations and labels on the console
#   * face-extraction: extracts captures of the faces into their own images. Applicable only to mode image
#   * face-features: Draws the specified face features. Off by default. Pass the list ['face'] to draw the whole face
#


class MyDetector(FaceDetect):
    # example of a method that print the detections property from FaceDetect
    def main(self):
        print(self.detections)


# Passing settings (the default ones are being passed for comparison purposes with main.py)
facedetector = MyDetector({'custom': True, 'method': 'main'})

try:
    # When the start method is not given an image or video path, it starts the webcam
    # For Image file: facedetector.start('<path to image file>')
    # For Video: facedetector.start('<path to video file>')
    # Press 'q' to exit
    facedetector.start()


# FaceDetect always generates a FaceDetect Exception
except Exception as error:
    print(error)
