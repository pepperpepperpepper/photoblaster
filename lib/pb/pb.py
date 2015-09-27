"""contains only the Pb class which is used by the Pb.* modules for inheritance"""

import re
from config import WORKING_DIR, BIN_CONVERT, BIN_IDENTIFY,\
    DEFAULT_HEIGHT, DEFAULT_WIDTH
import time
import urllib, urllib2
import sys, os
import random
from subprocess import Popen, PIPE, call
from params import Params
import sha
import simplejson as json
from s3cli import S3Cli
from db import Db
BASE_URL = "http://i.asdf.us"

_MAX_FILENAME_LENGTH = 20

class PbProcessError(Exception):
    pass

class Pb(object):
    """Default Pb class. USED ONLY FOR INHERITANCE"""
    def __init__(self, **kwargs):
        self._input_kwargs = kwargs
        self._now = str(int(time.time()))
        self.params = Params(classname=self.__class__.__name__, now=self._now)
        self._files_created = []
        self.commands = []
        self._working_dir = WORKING_DIR
        self._tag = self.__class__.__name__
        self._hashdir = None
        self._db_url_param = None

        #FIXME move to separate class
        self.file_size = None
        self.width = None
        self.height = None
        self.filename = None
        self.filepath = None
        self.file_height = None
        self.file_width = None

    def _filename_create(self, url=None, namepart="", extension=""):
        if url:
            _basename = os.path.basename(url)
            namepart = re.split(r'\.', _basename)[0]
            namepart = self._url_sanitize(namepart)[0:_MAX_FILENAME_LENGTH]
        name = ""
        if namepart: name += "%s-" % namepart
        name += "%s_%s" % (self.__class__.__name__, self._now)
        if self.params.username: name += "_%s" % self.params.username
        if extension: name += ".%s" % extension
        return name

    def _filepath_create(self, filename, directory=WORKING_DIR):
        return os.path.join(directory, filename)

    def _filename_filepath_create(self, url=None, namepart="", directory=WORKING_DIR, extension=""):
        _filename = self._filename_create(url=url, namepart=namepart, extension=extension)
        _filepath = self._filepath_create(_filename, directory=directory)
        return _filename, _filepath

    def _tempfilepath_create(self, namepart="temp", directory=WORKING_DIR, extension=""):
        _filename = self._filename_create(namepart=namepart, extension=extension)
        return self._filepath_create(_filename, directory=directory)

    def _hashdir_create(self):
        self._hashdir = sha.new(self.filename).hexdigest()[:2]

    def _url_sanitize(self, s):
        return re.sub(r'\W+', '', s)

    def _call_cmd(self, cmd):
        try:
            cmd = map(lambda i: str(i), cmd)
            call(cmd)
            self.commands.append(" ".join(cmd))
        except Exception:
            raise Exception("Unable to call cmd {}".format(str(cmd)))

    def _dimensions(self, filepath):
        try:
            ident = (Popen([BIN_IDENTIFY, filepath], stdout=PIPE).communicate()[0]).split(" ")
            return ident[2].split("x")
        except Exception as e:
            self.err_warn("Unable to get file dimensions:\n")
            self.err_ward(str(e))

    def _file_dimensions(self):
        self.file_width, self.file_height = self._dimensions(self.filepath)

    def _width_and_height_set(self, filepath=None, width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT):
        if filepath:
            self.width, self.height = self._dimensions(filepath)
            return
        self.width = width
        self.height = height

    def _file_size_get(self):
        try:
            self.file_size = os.stat(self.filepath)[6]
        except Exception as e:
            self.err_warn("Couldn't determine filesize of %s\n" % self.filepath)
            self.err_warn(str(e))

    def _file_read(self, filepath):
        f = open(filepath, 'r')
        data = f.read()
        f.close()
        return data

    def err_warn(self, s):
        sys.stderr.write("ERROR:{} - {}\n".format(self.__class__.__name__, s))
        raise PbProcessError

    def _cleanup(self):
        if not self._files_created: return
        map(lambda n: os.remove(n), self._files_created)

    def _file_clean_local(self):
        os.remove(self.filepath)

    def err_fatal(self, s):
        sys.stderr.write("ERROR[FATAL]:%s - %s\n" % (self.__class__.__name__, s))
        sys.exit(1)

    @classmethod
    def example_run(cls, params=None, verbose=True):
        example_params = params or cls.example_params
        if not example_params:
            raise AttributeError("Must supply test params to test %s" % cls.__name__)
        b = cls(**example_params)
        b.create()
        if verbose:
            sys.stderr.write("generated %s\n" % b.filepath)
            sys.stderr.write("files created %s\n" % b._files_created)
            sys.stderr.write("commands:\n  %s\n" % ";\n  ".join(b.commands))
        return b

    @staticmethod
    def gif_frames(filepath):
        try:
            info = Popen([BIN_IDENTIFY, filepath], stdout=PIPE).communicate()[0]
            frames = filter((lambda x: x), map(
                (lambda x: x.split(" ")[0]),
                (info).split('\n')
            ))
            return frames
        except Exception as e:
            self.err_warn("couldn't get gif frames")
            raise e

    def _choose_gif_frame(self, filepath):
        _gif_frames = Pb.gif_frames(filepath)
        frame = random.choice(_gif_frames)
        self._call_cmd([BIN_CONVERT, frame, filepath])

    def db_send(self, remote_addr=None, db_connection=None):
        try:
            db = db_connection or Db()
        except Exception as e:
            sys.stderr.write("Could not connect to db:\n{}".format(e))
            sys.exit(1)
        try:

            _insert_data = {
                'date' : self._now,
                'remote_addr' : remote_addr,
                'username' : str(self.params.username),
                'url' : self._db_url_param,
                'directory' : self._hashdir,
                'oldfile' : None,
                'newfile' : self.filename,
                'dataobj' : json.dumps(dict(self._input_kwargs)),
                'cmd' : "; ".join(self.commands),
                'tag' : self._tag,
            }
            db.insert_cmd(**_insert_data)
        except Exception as e:
            self.err_warn("Problem sending to database:\n %s" % str(e))

    def file_s3move(self):
        self._hashdir_create()
        s3cli = S3Cli()
        s3cli.s3move(self.filepath, "im/{}/{}".format(self._hashdir, self.filename))
        self._file_clean_local()

    def file_dict(self):
        return {
            'url' : "%s/im/%s/%s" % (BASE_URL, self._hashdir, self.filename),
            'size' : self.file_size,
            'width' : "%spx" % self.file_width,
            'height' : "%spx" % self.file_height,
        }

    def create(self):
        #base methods FIXME move into File class
        self._file_dimensions()
        self._file_size_get()
        self._cleanup()
