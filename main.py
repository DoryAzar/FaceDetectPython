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
    facedetector.start()

except TypeError as error:
    print(error)
