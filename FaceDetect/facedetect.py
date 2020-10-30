# facedetect.py
#
# FaceDetect framework that provides tools and features to detect and recognize faces in different media
#
# Usage:
#  - Import FaceDetect into your python script
#  - Instantiate a FaceDetect object

# Default Face Detection:
#  - Call the start() method (default settings will be run)
#  - This will automatically start face detection
#
# Customize Face Detection:
#  - Pass a settings dictionary to the FaceDetect constructor
#  - Setting capabilities:
#   * mode:  image or video (default)
#   * custom: False (default). Set to True when the FaceDetect class is extended
#   * method: call native callback methods during detection or bypass with a custom method
#   * draw: draws the detection on the canvas if set to True (default)
#
# Dory Azar
# December 2020

import os
import cv2
import face_recognition


class FaceDetect:
    """ FaceDetect framework that provides tools and features to detect and recognize faces in different media """

    # Defining constant settings
    DEFAULT_SETTINGS = {'mode': 'video', 'draw': True, 'custom': False, 'method': 'detect'}
    ACCEPTED_VIDEO_FORMAT = ['avi', 'mp4', 'mov']
    ACCEPTED_IMAGE_FORMAT = ['jpeg', 'jpg', 'gif', 'png']

    def __init__(self, settings=None):
        """ Initializes the Face Detect framework"""

        # Initialize default properties
        self.canvas = cv2
        self.stream = None
        self.settings = self.DEFAULT_SETTINGS

        # Initialize face detection and recognition properties
        self.frame = None  # The detection frame
        self.face_locations = []  # Face locations
        self.face_encodings = []  # Face Signatures
        self.face_labels = []  # Face labels
        self.detections = None  # Face detection results

        # Populating setting from input (overrides are possible)
        if settings:
            for setting in settings:
                setting = setting.lower()

                # Sanitize if string, otherwise take as is
                val = settings[setting].lower().strip() if isinstance(settings[setting], str) else settings[setting]

                self.settings[setting] = val

    ####################################################
    # Public methods for face detection and recognition
    ####################################################

    def start(self, media_path=''):
        """ Interface starter that starts either an image app or a video/webcam app"""

        # If mode is image than run static detection mode
        if self.__get_setting('mode') == 'image':
            self.__detect_static(media_path)

        # if mode is video than run streaming mode
        else:
            self.__detect_stream(media_path)

    ####################################################
    # Detection mechanisms
    # - Static: For images
    # - Stream: For video and webcam
    ####################################################

    def __detect_static(self, media_path):
        """ Loads an image for face detection and recognition"""
        try:
            # Check if valid image type
            if not media_path or not self.__is_valid_media('image', media_path):
                raise TypeError('Provide a valid image file')

            # Load the image in cv2 for display
            self.frame = self.canvas.imread(media_path)

            # Load the image in face_recognition for calculations
            self.stream = face_recognition.load_image_file(media_path)

            # Start the detection
            self.__detect()

            # Call a native or custom callback method
            self.__callback()

            # Open the cv2 media player
            while True:

                # Display the final result
                self.canvas.imshow('FaceDetect', self.frame)

                # Close when 'q' is pressed
                if self.canvas.waitKey(1) & 0xFF == ord('q'):
                    return

        except TypeError as error:
            raise error

        except self.canvas.error:
            raise TypeError("We are unable to start FaceDetect")

    def __detect_stream(self, media_path=''):
        """ Starts the video or the webcam for face detection and recognition"""

        # Capture the media provided
        try:
            # Get the media stream
            self.__capture(media_path)

            # Keep displaying as long as stream is open
            while self.stream and self.stream.isOpened():

                ret, self.frame = self.stream.read()
                if ret:

                    # Start the detection
                    self.__detect()

                    # Call a native or custom callback method
                    self.__callback()

                    self.canvas.imshow('FaceDetect', self.frame)

                # Close when 'q' is pressed
                if self.canvas.waitKey(1) & 0xFF == ord('q'):
                    return

        except TypeError as error:
            raise error

        except self.canvas.error:
            raise TypeError("We are unable to start FaceDetect")

    def __detect(self):
        """ Detects faces in the media provided and calls on drawing or printing locations out """

        # Initialize variables
        mode = self.__get_setting('mode')
        self.face_labels = []

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = self.canvas.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1] if mode != 'image' else self.stream

        # Find all the faces in the frame
        self.face_locations = face_recognition.face_locations(rgb_small_frame)

        # Iterate through the detected face locations and append an unknown label
        for count, location in enumerate(self.face_locations):
            label = "Face " + str(count + 1)
            self.face_labels.append(label)

        # Condense the face locations and labels into tuples
        self.detections = zip(self.face_locations, self.face_labels) if self.face_locations else None

        # Draw detections if they are available and the setting is on
        if self.detections and self.__get_setting('draw'):
            self.detections = [(detection[0], detection[1]) for detection in self.detections]
            self.__draw_detections()

        # If there are detections print and drawing is off, print them off
        elif self.detections:
            print(self)

    def __callback(self):
        """ Callback method that will run at every fetching interval and that will execute
        a method determined in the settings """

        method = self.settings['method'] if self.__get_setting('method') else None

        # Execute method if it exists
        try:
            if method and self.__get_setting('custom'):
                self.__getattribute__(method)()
            elif method and method != 'detect':
                self.__getattribute__('_FaceDetect__' + method)()

        # Generate exception if the method does not exist
        except AttributeError:
            raise TypeError("The provided method does not exist")

    ####################################################
    # Additional callback methods
    ####################################################

    def __recognize(self):
        """ Calls the face recognition """
        print('recognizing')
        return self

    ####################################################
    # OpenCV Utility methods
    ####################################################

    def __capture(self, media_input=''):
        """ Captures video or webcam using OpenCV """

        # If invalid media video, it will open the video cam by default
        media_input = media_input if media_input and self.__is_valid_media('video', media_input) else 0
        self.stream = self.canvas.VideoCapture(media_input)

    def __draw_detections(self):
        """ Draws the rectangles over the detections """

        # Iterate through the zipped tuples of locations and labels
        for (top, right, bottom, left), label in self.detections:

            if self.__get_setting('mode') != 'image':
                # Resize the face locations since the initial detected frame was scaled down
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

            # Draw a box around the face
            self.canvas.rectangle(self.frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Draw a label with a label below the face
            self.canvas.rectangle(self.frame, (left, bottom - 35), (right, bottom), (255, 0, 0), self.canvas.FILLED)
            font = self.canvas.FONT_HERSHEY_DUPLEX
            self.canvas.putText(self.frame, label, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

    ####################################################
    # Utility methods
    ####################################################

    def __str__(self):
        """ Stringify the object by exposing the detections and recognitions"""
        results = ''
        for detection in self.detections:
            results = results + '(%s, %s)' % (detection[0], detection[1])
        return results

    def __is_valid_media(self, media_type, media_path):
        """ Validates if a media path is of an acceptable format """

        # Get the file name and extension
        file_name, file_extension = os.path.splitext(media_path)

        # Sanitize the file extension to get rid of the .
        file_extension = file_extension.strip('.')

        # Check if it is an accepted video format
        if media_type.lower() == 'video' and file_extension.lower() in self.ACCEPTED_VIDEO_FORMAT:
            return True

        # Check if it is an accepted image format
        elif media_type.lower() == 'image' and file_extension.lower() in self.ACCEPTED_IMAGE_FORMAT:
            return True
        return False

    def __get_setting(self, key):
        """ Getter to get a value from the settings """
        if key.lower() in self.settings and self.settings[key]:
            return self.settings[key]
        return None

    def __end(self):
        """ Ends the show """
        if self.stream:
            self.stream.release()

        if self.canvas:
            self.canvas.destroyAllWindows()
