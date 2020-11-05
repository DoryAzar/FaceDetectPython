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
#   * print: prints the face locations and labels on the console
#   * face-extraction: extracts captures of the faces into their own images. Applicable only to mode image
#   * face-features: Draws the specified face features. Off by default. Pass the list ['face'] to draw the whole face
#
# Dory Azar
# December 2020

import os
import cv2
from PIL import Image
import numpy
import face_recognition


class FaceDetect:
    """ FaceDetect framework that provides tools and features to detect and recognize faces in different media """

    # Defining constant settings
    FACE_FEATURES = ['chin', 'left_eye', 'right_eye', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip',
                     'top_lip', 'bottom_lip']
    DEFAULT_SETTINGS = {
        'mode': 'video',
        'draw': True,
        'custom': False,
        'method': 'detect',
        'face-extraction': False,
        'print': True,
        'face-features': [],
        'known-faces': {'John': 'resources/person1.png', 'Jane': 'resources/person2.png'}
    }
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
        self.known_faces_encodings = []  # Face Encodings of known faces
        self.known_faces_labels = []  # Face Labels of known faces
        self.face_labels = []  # Face labels
        self.detections = None  # Face detection results
        self.face_landmarks = None  # Face landmarks
        self.face_extracts = []  # Collection of face extracted face images

        # Populating setting from input (overrides are possible)
        if settings:
            for setting in settings:

                # Sanitize the key
                sanitized_setting = setting.lower()

                # Get the value and sanitize if string, otherwise take as is
                val = settings.get(setting)
                val = val.lower().strip() if type(val) is str else val

                # Set the settings to the sanitized keys and values
                self.settings[sanitized_setting] = val if val else self.settings[sanitized_setting]

    ####################################################
    # Public methods for face detection and recognition
    ####################################################

    def start(self, media_path=''):
        """ Interface starter that starts either an image app or a video/webcam app"""

        try:

            # Execute before calling engine
            self.__preload()

            # If mode is image than run static detection mode
            if self.__get_setting('mode') == 'image':
                self.__detect_static(media_path)

            # if mode is video than run streaming mode
            else:
                self.__detect_stream(media_path)

        # Raise TypeError exceptions
        except TypeError as error:
            raise Exception(error)

        # Raise exceptions caused by canvas (cv2) and raise as FaceDetect Exception
        except self.canvas.error:
            raise Exception("There was a problem starting the FaceDetect canvas")

        # Any other exception classify as data runtime issue and raise as FaceDetect Exception
        except Exception as error:
            raise Exception(error)

    ####################################################
    # Detection mechanisms
    # - Static: For images
    # - Stream: For video and webcam
    ####################################################

    def __detect_static(self, media_path):
        """ Loads an image for face detection and recognition"""

        # Check if valid image type
        if not media_path or not self.__is_valid_media('image', media_path):
            raise Exception('Provide a valid image file')

        # Load the image in cv2 for display
        self.frame = self.canvas.imread(media_path)

        # Load the image in face_recognition for calculations
        self.stream = face_recognition.load_image_file(media_path)

        # Start the detection
        self.__detect()

        # Call a native or custom callback method
        self.__callback()

        # Execute Settings if there are detections
        if self.detections:
            self.__execute_setting()

        # Open the cv2 media player
        while True:

            # Display the final result
            self.canvas.imshow('FaceDetect', self.frame)

            # Close when 'q' is pressed
            if self.canvas.waitKey(1) & 0xFF == ord('q'):
                return

    def __detect_stream(self, media_path=''):
        """ Starts the video or the webcam for face detection and recognition"""

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

                # Execute Settings if there are detections
                if self.detections:
                    self.__execute_setting()

                self.canvas.imshow('FaceDetect', self.frame)

            # Close when 'q' is pressed
            if self.canvas.waitKey(1) & 0xFF == ord('q'):
                return

    ####################################################
    # FaceDetect Flow Methods
    ####################################################

    def __preload(self):
        """ Assesses the provided (or default) settings and preloads features """

        # With recognition activated
        if self.__get_setting('method') == 'recognize':

            #  Get the known face files provided
            known_faces = self.__get_setting('known-faces')
            known_faces = known_faces if type(known_faces) is dict else {}

            # Get the list of tuples from the setting input
            known_faces = [(known_face_label, image_path) for known_face_label, image_path in known_faces.items()]

            # Iterate through each setting input and load the images
            for (known_face_label, image_path) in known_faces:
                try:
                    loaded_image = face_recognition.load_image_file(image_path)
                    self.known_faces_encodings.append(face_recognition.face_encodings(loaded_image)[0])
                    self.known_faces_labels.append(known_face_label)

                # Raise FileNotFoundError onto a FaceDetect Exception
                except FileNotFoundError:
                    raise Exception("Some of the image paths provided are invalid")

                # Raise any other Exception on a FaceDetect Exception
                except Exception:
                    raise Exception("We were not able to start face recognition")

    def __detect(self):
        """ Detects faces in the media provided and calls on drawing or printing locations out """

        # Initialize variables
        mode = self.__get_setting('mode')
        self.face_labels = []

        # Resize frame of video to 1/4 size for faster face detections
        small_frame = self.canvas.resize(self.frame, (0, 0), fx=0.25, fy=0.25)

        # If it's video, convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        # If it is an image take the stream
        rgb_small_frame = small_frame[:, :, ::-1] if mode != 'image' else self.stream

        # Find all the faces in the frame and their encodings
        self.face_locations = face_recognition.face_locations(rgb_small_frame)
        self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

        # Find all the faces landmarks
        self.face_landmarks = face_recognition.face_landmarks(rgb_small_frame)
        # Resize the data to match original size
        if mode != 'image':

            # Resize data to bring to original size
            self.face_locations = [(top*4, bottom*4, left*4, right*4) for (top, bottom, left, right)
                                   in self.face_locations]

            # Resize the data to bring to original size
            for landmark in self.face_landmarks:
                for feature in landmark:
                    landmark[feature] = [(x * 4, y * 4) for (x, y) in landmark[feature]]

        # Iterate through the detected face locations and append an unknown label
        for count, location in enumerate(self.face_locations):
            label = "Face " + str(count + 1)
            self.face_labels.append(label)

        # Upon face detection
        self.__generate_detections()

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
            raise Exception("The provided method does not exist")

    def __execute_setting(self):
        """ Assesses the provided (or default) settings and executes the detection features """

        # If there are detections print and drawing is off, print them off
        if self.__get_setting('print'):
            print(self)

        # Draw detections if they are available and the setting is on
        if self.__get_setting('draw'):
            self.__draw_detections()

        # Extract face images
        if self.__get_setting('mode') == 'image' and self.__get_setting('face-extraction'):
            self.__extract_face_images()

        # Draw Face Landmarks

        # Get the face-features setting
        features = self.__get_setting('face-features')

        # Force to an empty list if
        features = [] if type(features) is not list else list(map(str.lower, features))

        # Default features to be drawn unless specified
        features = self.FACE_FEATURES if 'face' in features else features

        if self.face_landmarks and features:
            self.__draw_landmarks(features)

    def __recognize(self):
        """ Compares faces to a known set of images and identifies them in the canvas """

        if self.face_encodings:

            # Clear the face labels to prepare for recognition
            self.face_labels = []

            # Iterate through the different face_encodings identified
            for face_encoding in self.face_encodings:

                # Default label is unknown
                label = 'Unknown'

                # Compare the face encodings and get all the potential matches
                face_matches = face_recognition.compare_faces(self.known_faces_encodings, face_encoding)

                # Find the best match based on the face distances
                face_distances = face_recognition.face_distance(self.known_faces_encodings, face_encoding)
                best_match = int(numpy.argmin(face_distances))

                # When a best match use the label provided as the label
                if face_matches[best_match]:
                    label = self.known_faces_labels[best_match]

                # Append the face label to the collection
                self.face_labels.append(label)

            # Update the detections account for the  new names
            self.__generate_detections()

    ####################################################
    # OpenCV & PIL  Utility methods
    ####################################################

    def __capture(self, media_input=''):
        """ Captures video or webcam using OpenCV """

        # If invalid media video, it will open the video cam by default
        media_input = media_input if media_input and self.__is_valid_media('video', media_input) else 0
        self.stream = self.canvas.VideoCapture(media_input)

    def __draw_detections(self):
        """ Draws the rectangles over the detections """

        # Check if there is recognition
        is_recognize = self.__get_setting('method') == 'recognize'

        # Iterate through the zipped tuples of locations and labels
        for (top, right, bottom, left), label in self.detections:

            # Define the colors based on whether or not recognition is activated
            b = 255 if not is_recognize else 0
            g = 255 if is_recognize and label != 'Unknown' else 0
            r = 255 if is_recognize and label == 'Unknown' else 0

            # Draw a box around the face
            self.canvas.rectangle(self.frame, (left, top), (right, bottom), (b, g, r), 2)

            # Draw a label with a label below the face
            self.canvas.rectangle(self.frame, (left, bottom - 35), (right, bottom), (b, g, r), self.canvas.FILLED)
            font = self.canvas.FONT_HERSHEY_DUPLEX
            self.canvas.putText(self.frame, label, (left + 6, bottom - 6), font, 0.9, (255, 255, 255), 1)

    def __extract_face_images(self):
        """ Extracts individual face images from image. Works in mode image only """

        # Iterate through the zipped tuples of locations and labels
        for (top, right, bottom, left), label in self.detections:
            # frame the detected face
            face_image = self.stream[top:bottom, left:right]

            # Change the image to PIL image for manipulation
            pil_image = Image.fromarray(face_image)

            # Save the extracted PIL images
            self.face_extracts.append(pil_image)

            # Display the pil image
            pil_image.show()

    def __draw_landmarks(self, features=None):
        """ Draws the facial features of a detected face """

        # Iterate through the detected face landmarks
        for landmark in self.face_landmarks:

            # Iterate through the features of each face
            for feature in landmark:

                # Draw them as closed lines on the canvas except the chin will be an open line
                if features and feature in features:

                    # Draw closed lines around the feature unless it's the chin
                    points = numpy.array(landmark[feature])
                    self.canvas.polylines(self.frame, [points], feature != 'chin', (255, 0, 0), 2)

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

    def __generate_detections(self):
        """ Generates and updates the detections """

        # Condense the face locations and labels into tuples
        self.detections = zip(self.face_locations, self.face_labels) if self.face_locations else None

        # Format onto tuples if there are self detections
        if self.detections:
            self.detections = [(detection[0], detection[1]) for detection in self.detections]

    def __end(self):
        """ Ends the show """
        if self.stream:
            self.stream.release()

        if self.canvas:
            self.canvas.destroyAllWindows()
