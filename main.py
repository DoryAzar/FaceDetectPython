from FaceDetect.facedetect import FaceDetect


def temp():
    print('yay')


hello = FaceDetect()
try:
    hello.start()

except TypeError as error:
    print(error)
