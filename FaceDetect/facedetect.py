# facedetect.py
#
# FaceDetect framework that provides tools and features to detect and recognize faces in different media
# Usage: % python facedetect.py
#
# Dory Azar
# December 2020

import cv2


class FaceDetect():
    """ FaceDetect framework that provides tools and features to detect and recognize faces in different media """

    def __init__(self, settings=None, app=None):
        """Initializes the Face Detect framework"""

        # Initialize default properties
        self.canvas = cv2
        self.stream = None
        self.app = self.__main if not app or app is None else app
        self.settings = {'method': 'detect'}

        # Populating setting from input (overrides are possible)
        if settings:
            for setting in settings:
                setting = setting.lower()
                val = settings[setting].lower().strip()

                # Add to the settings only if values are provided
                if val:
                    self.settings[setting] = val

    def start(self, media_path=''):
        """Starts the video, webcam or image to start face detection and recognition"""

        # Capture the media provided
        try:
            # Get the media stream
            self.__capture(media_path)

            # Keep displaying as long as stream is open
            while self.stream and self.stream.isOpened():

                ret, frame = self.stream.read()
                if ret:
                    # small_frame = self.canvas.resize(frame, (0, 0), fx=0.25, fy=0.25)
                    self.canvas.imshow('image', frame)

                # Run the desired app
                self.app()

                # Close when 'q' is pressed
                if self.canvas.waitKey(1) & 0xFF == ord('q'):
                    return

        except TypeError as error:
            raise error

        except self.canvas.error:
            raise TypeError("We are unable to start FaceDetect")

    def __capture(self, media_input=''):
        """ Captures video, image or webcam """

        media_input = media_input if media_input else 0
        self.stream = self.canvas.VideoCapture(media_input)

    def __main(self):
        """ Main method that will run at every fetching interval """

        method = self.settings['method'] if 'method' in self.settings and self.settings['method'] else None

        # If method not defined raise exception
        if not method:
            raise TypeError("A Method needs to be defined")

        # Execute method if it exists
        try:
            self.__getattribute__('_FaceDetect__' + method)()

        # Generate exception if the method does not exist
        except AttributeError:
            raise TypeError("The provided method does not exist")

    def __detect(self):
        """ Calls the face detection """
        print('detecting')
        return self

    def __recognize(self):
        """ Calls the face recognition """
        print('recognizing')
        return self

    def __end(self):
        """ Ends the show """
        if self.stream:
            self.stream.release()

        if self.canvas:
            self.canvas.destroyAllWindows()
