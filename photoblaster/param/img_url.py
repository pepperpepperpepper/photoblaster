"""Img_url param class definition lives here"""
import os
from photoblaster.param import Param
from photoblaster.config import MAX_SIZE, SPECIAL_DOWNLOADERS,\
    SPECIAL_DOWNLOADERS_MAX_SIZE,\
    BIN_IDENTIFY
import urllib2
from subprocess import Popen, PIPE
import sys

class Img_url(Param):
    def __init__(self, value, key="", classname=""):
        """Defines the float param type.
           Takes in a url, sends a get request to the url, writes the response
           to a temporary filename, and checks the mimetype with imagemagick.
           Img_url class is different from other params in that it has
           the attributes:
               url: the original url used to retrieve the image
               filename: the filename created to store the image
               filepath: complete path to the stored image file
               mimetype: the mimetype of the image
       Args:
           value: the image url string
           key: the intended name of the param instance
           classname: the name of the class to which the param belongs
        """
        super(Img_url, self).__init__(classname=classname)
        if value:
            self.filename = self._filename_temporary(key)

            self.path = os.path.join(self._working_dir, self.filename)
            self._image_download(value, self.path)
            self.mimetype = self._image_mimetype(self.path)
            self.url = value

    def _filename_temporary(self, s):
        return "_tmp-{}-{}_{}".format(self._classname, self._now, s)

    def __dict__(self):
        return {
            'filename' : self.filename,
            'path': self.path,
            'url': self.url,
            'mimetype': self.mimetype
        }

    def __getitem__(self, item):
        return self.__dict__().__getitem__(item)

    def __str__(self):
        return str(self.__dict__())

    def __nonzero__(self):
        return True if self.path and self.mimetype else False

    def _image_download(self, url, path):
        """downloads the image to the path specified in the local
        filesystem"""
        max_size = MAX_SIZE
        if self.username in SPECIAL_DOWNLOADERS:
            max_size = SPECIAL_DOWNLOADERS_MAX_SIZE
        try:
            self._download(url, path, max_size=max_size)
        except Exception as e:
            self.err_warn("Download failed")

    def _browser_request(self, url, data=None):
        """sends a get request to the url using browser User-Agent headers"""
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Accept': '*/*',
        }
        try:
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
        except IOError as e:
            if hasattr(e, 'code'):
                self.err_warn('browser request error: %s - ERROR %s' % (url, e.code))
            raise IOError
        return response

    def _download(self, url, destination, max_size=MAX_SIZE):
        """generic download method, checks the size of the filedata"""
        response = self._browser_request(url, None)

        rawimg = response.read()
        if len(rawimg) == 0:
            self.err_warn("got zero-length file")
        if len(rawimg) > max_size:
            self.err_warn("file too big: max size {} KB / {} is {} KB".format(
                str(MAX_SIZE/1024),
                destination,
                str(len(rawimg)/1024)
            ))
        f = open(destination, "w")
        f.write(rawimg)
        f.close()

    def _image_mimetype(self, f):
        """retrieves the image mimetype from the file header using imagemagick"""
        try:
            mimetype = Popen(
                [BIN_IDENTIFY, f], stdout=PIPE
            ).communicate()[0].split(" ")[1].lower()
            return mimetype
        except Exception as e:
            self.err_warn("Couldn't determine mimetype")
