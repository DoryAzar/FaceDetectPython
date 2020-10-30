facedetection
=============

It returns the position by the facial recognition.

Install
-------

::

   $ pip install facedetection

How to use it
--------------

Supported API

- Google Vision Face Detection API
- Microsoft Projectoxford Detection API
- Akamai Image Converter API

::

   >>> from facedetection import MSProjectoxfordDetection
   >>> detect = MSProjectoxfordDetection('YOUR API TOKEN')
   >>> detect('http://your.image.url/path/to/image')


Contributors
------------

- peketamin


