#!/usr/bin/python2.7
import os
import random
import re
from photoblaster.config import BIN_CONVERT
from photoblaster.modules import Pb

DEFAULT_FINALFORMAT = "png"

_subtle_break_mark = 'pron'
_extreme_break_mark = 'sugar'

_header_offset = 2000
_default_breakmode = "subtle"

_BREAKTYPE_TRANSLATE = {
    'CLASSIC': 'jpg',
    'REDUX': 'pcds',
    'BLURRY_BREAK': 'viff',
    'BLURRY_BREAK_2': 'mat',
    'SWIPE': 'miff',
    'RGB_WASH': 'psd',
    'RGB_WASH_2': 'psb',
    'NOISY_BREAK': 'palm',
    'NOISY_BREAK_2': 'fig',
    'BROKEN_VIGNETTE': 'pbm',
    'FAX_MACHINE': 'cals',
    'STRIPES': 'exr',
    'PHOTOCOPY': 'art',
}


class PbBreaker(Pb):
    example_params = {
        "url": "http://i.asdf.us/im/de/HolyMountain2_1322275112_seamonkey.gif",
        "breaktype": "RGB_WASH",
        "finalformat": "png",
        "breakmode": "extreme",
        "breakangle": "10",
        "username": "donkey",
        "expanded": "false"
    }

    def __init__(self, **kwargs):
        super(PbBreaker, self).__init__(**kwargs)
        _definitions = {
            'username': {'type': 'string'},
            'breaktype': {'type': 'string'},
            'breakmode': {
                'type': 'enum',
                'enum_values': ['subtle', 'extreme', 'gradual'],
                'default': _default_breakmode
            },
            'breakangle': {'type': 'float'},
            'expanded': {'type': 'bool'},
            'url': {'type': 'img_url'},
            'finalformat': {'type': 'enum',
                            'enum_values': ['png', 'gif', 'jpg']}
        }
        self.params.definitions_import(_definitions,
                                       kwargs,
                                       classname=self.__class__.__name__)
        self._files_created.append(self.params.url.path)
        self.params.breaktype.set_val(self._get_breaktype(
                                      str(self.params.breaktype)))

        # psd returns an animation
        if not self.params.finalformat and self.params.url.mimetype == "gif":
            self.params.finalformat.set_val("gif")
        elif self.params.breaktype == 'miff':
            self.params.finalformat.set_val("jpg")
            self.params.breakmode.set_val("subtle")
        elif not self.params.finalformat:
            self.params.finalformat.set_val(DEFAULT_FINALFORMAT)
        self._width_and_height_set(filepath=self.params.url.path)

        self.filename, self.filepath = self._filename_filepath_create(
            url=self.params.url.url,
            extension=self.params.finalformat
        )
        self._conversion_file = self._tempfilepath_create(
            namepart="conversion",
            extension=self.params.breaktype
        )

        self._db_url_param = str(self.params.url['url'])

    def _get_breaktype(self, key):
        return _BREAKTYPE_TRANSLATE[key]

    def _rotate(self):
        cmd = [
            BIN_CONVERT, self.params.url.path,
            "-rotate", self.params.breakangle,
            "+repage", self.params.url.path
        ]
        self._call_cmd(cmd)

    def _rotate_back(self):
        angle = str(360-int(self.params.breakangle))
        cmd = [BIN_CONVERT,
               self.filepath, "-rotate", angle, "+repage", self.filepath]
        self._call_cmd(cmd)
        if not self.params.expanded:
            cmd = [BIN_CONVERT,
                   self.filepath,
                   "-gravity",
                   "Center",
                   "-crop",
                   "{}x{}+0+0".format(self.width, self.height),
                   "+repage",
                   self.filepath]
            self._call_cmd(cmd)

    def _subtle_break(self):
        # assume the header is no longer than _header_offset bytes
        breakpoint = random.randint(_header_offset, len(self._file_data))
        newfile = self._file_data[0:breakpoint] +\
            _subtle_break_mark +\
            self._file_data[breakpoint:]
        self._file_data = newfile[0:len(self._file_data)]

    def _extreme_break(self):
        increment = len(self._file_data)/10
        i = 0
        newfile = ""
        for b in self._file_data:
            if i > _header_offset and not i % increment:
                b += _extreme_break_mark
            newfile += b
            i += 1
        self._file_data = newfile[0:len(self._file_data)]

    def _enforce_jpg(self):
        if self.params.breaktype in ["exr", "bmp", "miff"] and not \
                                 re.match(r'jpe?g$',
                                          self.params.url.mimetype,
                                          re.IGNORECASE):
            jpg_file = self._tempfilepath_create(extension="jpg")
            self._call_cmd([BIN_CONVERT, self.params.url.path, jpg_file])
            self._files_created.append(jpg_file)
            self._conversion_file = jpg_file

    def _first_conversion(self):
        if self.params.url.mimetype == self.params.breaktype:
            self._conversion_file = self.params.url.path
            return
        self._call_cmd([BIN_CONVERT,
                        self.params.url.path,
                        self._conversion_file])
        self._files_created.append(self._conversion_file)

    def _prepare_filedata(self):
        if self.params.url.mimetype == "gif" and\
                                    self.params.breaktype not in ['mat', 'psd']:
            self._choose_gif_frame(self.params.url.path)
        if self.params.breakangle:
            self._rotate()
        self._enforce_jpg()
        self._first_conversion()
        self._file_data = self._file_read(self._conversion_file)
        if not self._file_data:
            self.err_warn("Unable to get file data")

    def _add_false_data(self):
        if self.params.breakmode == "subtle":
            self._subtle_break()
        elif self.params.breakmode == "extreme":
            self._extreme_break()
        f = open(self._conversion_file, 'w')
        f.write(self._file_data)
        f.close()

    def _final_conversion(self):
        self._call_cmd([BIN_CONVERT, self._conversion_file, self.filepath])

        def psd_psbfilepath(num):
            return os.path.join(re.sub(r'\.', "-%s." % num, self.filepath))
        if str(self.params.breaktype) == 'psd':
            self._call_cmd(['mv', psd_psbfilepath(1), self.filepath])
            self._files_created.append(psd_psbfilepath(0))
        if str(self.params.breaktype) == 'psb':
            self._call_cmd(['mv', psd_psbfilepath(0), self.filepath])
            self._files_created.append(psd_psbfilepath(1))
        if self.params.breakangle:
            self._rotate_back()

    def create(self):
        self._prepare_filedata()
        self._add_false_data()
        self._final_conversion()
        super(PbBreaker, self).create()
