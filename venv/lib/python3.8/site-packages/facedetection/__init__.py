#! /usr/bin/env python
import sys
import json
import base64
import logging
import argparse
import urllib.parse
from collections import OrderedDict

import furl
import requests
from zope.interface import (
    Attribute,
    Interface,
    implementer,
)
from zope.interface.registry import Components
import oauth2client.client
import googleapiclient.discovery
import PIL.Image

import six
from six import BytesIO


__version__ = '1.2'

logger = logging.getLogger(__name__)


def get_file_name(file_or_url):
    if isinstance(file_or_url, six.string_types):
        return file_or_url
    return getattr(file_or_url, 'name', str(file_or_url))


def is_localfile(uri):
    if isinstance(uri, six.string_types):
        url_obj = urllib.parse.urlparse(uri)
        return url_obj.scheme == ''
    return True


def is_gcs_image_uri(uri):
    """Determine the Google Cloud Storage image URI"""
    url_obj = urllib.parse.urlparse(uri)
    return url_obj.scheme == 'gs'


def read_file(file_or_path):
    if hasattr(file_or_path, 'read'):
        return file_or_path.read()
    else:
        with open(file_or_path, 'rb') as fp:
            return fp.read()


def get_encoded_image(file_or_path):
    buf = read_file(file_or_path)
    return base64.b64encode(buf).decode()


class ICoord(Interface):
    """Coordinate interface"""
    x = Attribute('X coordinate')
    y = Attribute('Y coordinate')


@implementer(ICoord)
class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return 'Coord({}, {})'.format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class IDetection(Interface):
    """Image recognition interface"""

    def __call__(url_or_path):
        """Execute recognition

        The recognition result is returned and stored in the IDetectionResult.
        """


class IDetectionResult(Interface):
    """Image detection result interface"""
    coords = Attribute('List of ICoord')
    uri = Attribute('URI of image')


class IDetectionResultFactory(Interface):
    def __call__(uri, data):
        """Generate a IDetectionResult by analyzing the API Response"""


class ICrop(Interface):
    """Cropping image"""

    def __call__():
        """Execute cropping"""


@implementer(ICrop)
class AkamaiCrop:
    """Cropping for Akamai Image Converter"""

    def __call__(self, detection_result, **kwds):
        """Return a cropped URL in Akamai CDN from IDetectionResult

        >>> result = GoogleVisionAPIFaceDetectionResult()
        >>> result.uri = 'https://example.com/example.jpg'
        >>> result.coords = [
        ...    Coord(20, 30),
        ...    Coord(25, 24),
        ...    Coord(29, 21),
        ... ]
        >>> crop = AkamaiCrop()
        >>> crop(result)
        'https://example.com/example.jpg?crop=29:30%3B20,21'
        """
        start, end = self.create_rect(detection_result.coords)
        return self.build_uri(
            detection_result.uri,
            start, end, **kwds
        )

    def create_rect(self, coords):
        """
        Return looking for the upper left corner (start) and lower right (end)
        of the square from the list of ICoord

        >>> coords = [
        ...    Coord(20, 30),
        ...    Coord(25, 24),
        ...    Coord(29, 21),
        ... ]
        >>> crop = AkamaiCrop()
        >>> start, end = crop.create_rect(coords)
        >>> start.x, start.y
        (20, 21)
        >>> end.x, end.y
        (29, 30)
        """
        x_points = [coord.x for coord in coords]
        y_points = [coord.y for coord in coords]
        min_coord = Coord(min(x_points), min(y_points))
        max_coord = Coord(max(x_points), max(y_points))
        return min_coord, max_coord

    def build_uri(self, uri, start, end, width='*', height='*', composite_to='*.*',
                  bg_url=None, bg_width='*', bg_height='*', **kwds):
        """Create a cropped URL in Akamai

        >>> crop = AkamaiCrop()
        >>> crop.build_uri(
        ...    'https://example.com/test.jpg',
        ...    Coord(10, 20),
        ...    Coord(30, 40),
        ... )
        'https://example.com/test.jpg?crop=30:40%3B10,20'
        """
        furl_obj = furl.furl(uri)
        furl_obj.args['crop'] = '{}:{};{},{}'.format(
            (end.x - start.x), (end.y - end.x), start.x, start.y)
        furl_obj.args['resize'] = '{}:{}'.format(width, height)
        akamai_url = furl_obj.url

        if bg_url:
            furl_obj.args['composite-to'] = composite_to

            bg_furl_obj = furl.furl(bg_url)
            bg_furl_obj.args['resize'] = '{}:{}'.format(bg_width, bg_height)
            akamai_url += ('|' + bg_furl_obj.url)

        return akamai_url


@implementer(IDetection)
class GoogleVisionAPIFaceDetection:
    """Google Vision API Face Recognition

    Must set path to authentication json file to the environment variable
    `GOOGLE_APPLICATION_CREDENTIALS`. You can download an authentication json file
    from Google Cloud Platform Admin Site.

    ex)::

       $ export GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/gcp/authentication/file

    """

    discovery_url = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'

    def __init__(self):
        self.credentials = oauth2client.client.GoogleCredentials.get_application_default()
        self.service = googleapiclient.discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=self.discovery_url,
        )
        self.image_api = self.service.images()

    def __call__(self, file_or_url):
        is_local = is_localfile(file_or_url)
        payload = self.build_payload(file_or_url, is_local)
        data = self.request(payload=payload)
        create_result = GoogleVisionAPIFaceDetectionResultFactory()
        name = get_file_name(file_or_url)
        return create_result(name, data)

    def request(self, payload):
        """Send request to detection service api"""
        request = self.image_api.annotate(body=payload)
        return request.exexute()

    def build_payload(self, url_or_path, is_localfile=False):
        """Create request payload"""
        func = self.build_payload_for_localfile if is_localfile else self.build_payload_for_url
        return func(url_or_path)

    def build_payload_for_localfile(self, file_or_path):
        """Create a request payload for local image file"""
        return {
            'requests': [{
                'image': {
                    'content': get_encoded_image(file_or_path),
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 4,
                }],
            }],
        }

    def build_payload_for_url(self, url):
        """Create a request payload specify the image URL"""
        if not is_gcs_image_uri(url):
            logger.error('Must be a GCS URI: %s', url)

        return {
            'requests': [{
                'image': {
                    'source': {
                        'gcsImageUri': url,
                    },
                },
                'features': [{
                    'type': 'FACE_DETECTION',
                    'maxResults': 4,
                }],
            }],
        }


@implementer(IDetectionResultFactory)
class GoogleVisionAPIFaceDetectionResultFactory:
    def __call__(self, uri, data):
        result = GoogleVisionAPIFaceDetectionResult()
        result.uri = uri
        result.data = data
        result.coords = [coord for coord in self.get_coords(data)]
        return result

    def get_coords(self, data):
        """Generate coords"""
        for response in data.get('responses', []):
            for annotation in response.get('faceAnnotations', []):
                for name in ['fdBoundingPoly', 'boundingPoly']:
                    for vertice in annotation[name]['vertices']:
                        yield Coord(vertice.get('x', 0), vertice.get('y', 0))


@implementer(IDetectionResult)
class GoogleVisionAPIFaceDetectionResult:
    """Google Vision API face recognition result"""

    def __init__(self):
        self.uri = None
        self.coords = []
        self.data = None


class MSProjectoxfordDetectionError(Exception):
    pass


@implementer(IDetection)
class MSProjectoxfordDetection:
    """MS Recongnition API face recognition."""
    endpoint = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect'

    def __init__(self, api_token):
        self.api_token = api_token

        self.returnFaceId = True
        self.returnFaceLandmarks = False

        # comma-separated string like "returnFaceAttributes=age,gender".
        # Supported face attributes include age, gender, headPose, smile, facialHair, and glasses.
        # Note that each face attribute analysis has additional computational and time cost.
        self.returnFaceAttributes = None

    def __call__(self, file_or_url):
        is_local = is_localfile(file_or_url)
        headers = self.build_headers(is_local)
        payload = self.build_payload(file_or_url, is_local)
        data = self.request(headers=headers, payload=payload)
        create_result = MSProjectoxfordDetectionResultFactory()
        name = get_file_name(file_or_url)
        return create_result(name, data)

    def build_endpiont(self):
        url_parts = list(urllib.parse.urlparse(self.endpoint))
        query = OrderedDict(urllib.parse.parse_qsl(url_parts[4]))
        query['returnFaceId'] = "true" if self.returnFaceId else "false"
        query['returnFaceLandmarks'] = "false" if not self.returnFaceLandmarks else "true"
        if self.returnFaceAttributes and isinstance(self.returnFaceAttributes, list):
            query['returnFaceAttributes'] = ",".join(self.returnFaceAttributes)
        url_parts[4] = urllib.parse.urlencode(query)
        return urllib.parse.urlunparse(url_parts)

    def request(self, headers, payload):
        """Send request to detection service api"""
        res = requests.post(self.build_endpiont(), headers=headers, data=payload)
        if res.status_code != 200:
            raise MSProjectoxfordDetectionError(
                'detection failed: status={}, reason={}, content={}'.format(
                    res.status_code, res.reason, res.content))
        return res.json()

    def build_headers(self, is_localfile=False):
        """Create request headers

        >>> Detect = MSProjectoxfordDetection('dummy token')
        >>> headers = detect.build_headers()
        >>> headers['Content-Type']
        'application/json'
        >>> headers['Ocp-Apim-Subscription-Key']
        'dummy token'

        It specifies the True to `is_localfile` if a recognizing image file are local file.

        >>> headers = detect.build_headers(is_localfile=True)
        >>> headers['Content-Type']
        'application/octet-stream'
        >>> headers['Ocp-Apim-Subscription-Key']
        'dummy token'

        """
        return {
            'Content-Type': 'application/octet-stream' if is_localfile else 'application/json',  # noqa
            'Ocp-Apim-Subscription-Key': self.api_token,
        }

    def build_payload(self, url_or_path, is_localfile=False):
        """Create request payload

        >>> detect = MSProjectoxfordDetection('dummy token')
        >>> detect.build_payload('http://example.com')
        '{"url": "http://example.com"}'
        """
        func = self.build_payload_for_localfile if is_localfile else self.build_payload_for_url
        return func(url_or_path)

    def build_payload_for_localfile(self, path):
        """Create a request payload for local image file"""
        return read_file(path)

    def build_payload_for_url(self, url):
        """Create a request payload specify the image URL

        >>> detect = MSProjectoxfordDetection('dummy token')
        >>> detect.build_payload_for_url('http://example.com')
        '{"url": "http://example.com"}'
        """
        return json.dumps({'url': url})


@implementer(IDetectionResultFactory)
class MSProjectoxfordDetectionResultFactory:
    def __call__(self, uri, data):
        result = MSProjectoxfordDetectionResult()
        result.uri = uri
        result.data = data
        result.coords = [coord for coord in self.get_coords(data)]
        return result

    def get_coords(self, data):
        """Generate coords"""
        for response in data:
            rect = response['faceRectangle']
            yield Coord(rect['left'], rect['top'])
            yield Coord(rect['left'], rect['top'] + rect['height'])
            yield Coord(rect['left'] + rect['width'], rect['top'] + rect['height'])
            yield Coord(rect['left'] + rect['width'], rect['top'])


@implementer(IDetectionResult)
class MSProjectoxfordDetectionResult:
    """MS Recongnition API face detection result"""

    def __init__(self):
        self.uri = None
        self.coords = []
        self.data = None


class AllDetectionError(Exception):
    pass


@implementer(IDetection)
class AllDetection:
    """The entire image on the recognition result"""

    def __call__(self, url_or_path):
        if is_localfile(url_or_path):
            image_size = self.get_image_size_for_local(path=url_or_path)
        else:
            image_size = self.get_image_size_for_remote(url=url_or_path)
        create_result = AllDetectionResultFactory()
        return create_result(url_or_path, image_size)

    def get_image_size_for_local(self, path):
        """Get size of image size of local file"""
        with open(path, 'rb') as fp:
            return PIL.Image.open(fp).size

    def get_image_size_for_remote(self, url):
        """Get size of image size of remote file"""
        res = requests.get(url)
        with BytesIO(res.content) as fp:
            return PIL.Image.open(fp).size


@implementer(IDetectionResultFactory)
class AllDetectionResultFactory:
    def __call__(self, uri, image_size):
        """Create AllDetection result object

        :param str uri: Image url or path
        :param tuple image_size: tuple of image size (width, height)
        :rtype: AllDetectionResult
        :return: Detection result object
        """
        result = AllDetectionResult()
        result.uri = uri
        result.data = image_size
        result.coords = [
            Coord(0, 0),  # upper left corner
            Coord(0, image_size[1]),  # lower left corner
            Coord(image_size[0], 0),  # upper right corner
            Coord(image_size[0], image_size[1]),  # lower right corner
        ]
        return result


@implementer(IDetectionResult)
class AllDetectionResult:
    """AllDetection result object"""

    def __init__(self):
        self.uri = None
        self.coords = []
        self.data = None


def get_ms_param():
    import pit
    return pit.Pit.get('facedetection.face.ms', {
        'require': {
            'API_TOKEN': '',
        }
    })


def main(argv=sys.argv[1:]):
    reg = Components()
    reg.registerUtility(GoogleVisionAPIFaceDetection(),
                        IDetection, 'gcp')
    reg.registerUtility(MSProjectoxfordDetection(get_ms_param()['API_TOKEN']),
                        IDetection, 'ms')
    reg.registerUtility(AkamaiCrop(),
                        ICrop, 'akamai')

    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='gcp or ms')
    parser.add_argument('target', help='url or path')
    parser.add_argument('--crop', default='akamai')
    args = parser.parse_args(argv)

    detect = reg.queryUtility(IDetection, args.mode)
    result = detect(args.target)
    crop = AkamaiCrop()
    url = crop(result)
    print(url)

if __name__ == '__main__':
    sys.exit(main())
