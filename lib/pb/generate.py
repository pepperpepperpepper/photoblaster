from config import BIN_CONVERT, OUTPUT_IMAGE_TYPES, DEFAULT_FINALFORMAT
from pb import Pb
_DEFAULT_TAG = "im"

_GRAVITY_PARAMS = [
    "NorthWest", "North", "NorthEast", "West",
    "Center", "East", "SouthWest", "South", "SouthEast"
]
_GRAVITY_DEFAULT = "Center"
_COMPOSE_PARAMS = [
    "Over", "ATop", "Dst_Over", "Dst_In", "Dst_Out", "Multiply",
    "Screen", "Divide", "Plus", "Difference", "Exclusion", "Pin_Light",
    "Lighten", "Darken", "Overlay", "Hard_Light", "Soft_Light",
    "Linear_Dodge", "Linear_Burn", "Color_Dodge", "Color_Burn"
]
_DISPOSE_PARAMS = ["None", "Previous", "Background"]
_DISPOSE_DEFAULT = "None"
class PbGenerate(Pb):
#{{{ example params
    example_params = {
        """Example params. Used with the classmethod Pb.run_example"""
        'nearest': 'true',
        'compose': 'Soft_Light',
        'coalesce': 'true',
        'dispose': 'None',
        'gravity': 'Center',
        'width': '200',
        'black': 'black',
        'tile': 'true',
        'white': 'white',
        'contrast': '100',
        'hue': '90',
        'saturation': '100',
        'merge_early': 'true',
        'format': 'gif',
        'background': 'http://i.asdf.us/im/bc/new_1430440747.gif',
        'subtract': '#EE7AE9',
        'transparent': 'true',
        'name': 'yo',
        'url': 'http://asdf.us/im/new.gif',
        'flop': 'true',
        'flip': 'false',
        'callback': 'jsonp1430442384162',
        'fuzz': '5'
    }
#}}}
    def __init__(self, **kwargs):
        super(PbGenerate, self).__init__(**kwargs)
        """
        Used to assert the value-types of the incoming parameters.
        Types are defined as in their individual params classes.
        """
        _definitions = {
            #IMAGES
            'url': {'type': 'img_url'},
            'background': {'type': 'img_url'},

            #BOOLS
            'coalesce': {'type': 'bool'},
            'nearest': {'type': 'bool'},
            'merge_early': {'type': 'bool'},
            'flip': {'type': 'bool'},
            'flop': {'type': 'bool'},
            'tile': {'type': 'bool'},
            'transparent': {'type': 'bool'},

            #COLORS
            'black': {'type': 'color', 'default': 'black'},
            'white': {'type': 'color', 'default': 'white'},
            'subtract': {'type': 'color'},

            #INTS
            'fuzz': {'type': 'int'},
            'width': {'type': 'int'},
            'height': {'type': 'int'},
            'brightness': {'type': 'int'},
            'contrast': {'type': 'int'},
            'saturation': {'type': 'int'},
            'rotate': {'type': 'int'},
            'hue': {'type': 'int'},

            #ENUMS
            'compose': {'type': 'enum', 'enum_values': _COMPOSE_PARAMS, 'default': 'Atop'},
            'gravity': {
                'type': 'enum', 'enum_values': _GRAVITY_PARAMS, 'default': _GRAVITY_DEFAULT
            },
            'dispose': {
                'type': 'enum', 'enum_values': _DISPOSE_PARAMS, 'default': 'None'
            },
            'format': {
                'type': 'enum', 'enum_values': OUTPUT_IMAGE_TYPES, 'default': DEFAULT_FINALFORMAT
            },

            #STRINGS
            "username": {'type': "string"},
            "callback": {'type': "string"},
        }

        """Definitions and arguments are merged into attributes of the params object"""
        self.params.definitions_import(
            _definitions, kwargs, classname=self.__class__.__name__
        )

        """Used for the database tag column. Allows for tracking of the type
        of overlay method used."""
        self.tag = _DEFAULT_TAG
        if self.params.background:
            self.tag = self.params.compose
        if self.params.transparent:
            self.tag = self.params.transparent

        self.filename, self.filepath = self._filename_filepath_create(
            url=self.params.url['url'], extension=self.params.format
        )

        self._db_url_param = str(self.params.url['url'])

    def _composite(self):
        """Imagemagick composite command"""
        cmd = [
            BIN_CONVERT, self.params.background['path'],
            "null:", self.filepath, "-matte",
            "-dispose", self.params.dispose,
            "-gravity", self.params.gravity,
            "-compose", self.params.compose, "-layers", "composite",
            self.filepath
        ]
        self._call_cmd(cmd)

    def _convert(self):
        """Imagemagick convert command"""
        cmd = [BIN_CONVERT, self.params.url['path']]
        if self.params.rotate:
            cmd += ["-rotate", self.params.rotate]
        if self.params.flip:
            cmd += ["-flip"]
        if self.params.flop:
            cmd += ["-flop"]
        if self.params.transparent:
            if self.params.fuzz:
                cmd += ["-fuzz", "{}%".format(self.params.fuzz)]
            cmd += ["-transparent", self.params.subtract]
        if self.params.width or self.params.height:
            if self.params.nearest and self.params.format == "gif":
                cmd += ["-coalesce", "+map", "-interpolate", "Nearest", "-interpolative-resize"]
            else:
                cmd.append("-resize")
            cmd += ["{}x{}".format(self.params.width or "", self.params.height or "")]
        if self.params.black != "black" or self.params.white != 'white':
            cmd += ["+level-colors", "{},{}".format(self.params.black, self.params.white)]
        if self.params.contrast:
            cmd += ['-contrast-stretch', self.params.contrast]
        if self.params.brightness or self.params.saturation or self.params.hue:
            cmd += [
                "-modulate", "{},{},{}".format(
                    self.params.brightness or 100,
                    self.params.contrast or 100,
                    self.params.hue or 100
                )
            ]
        cmd.append("-coalesce")#why? #FIXME
        cmd += [self.filepath]
        self._call_cmd(cmd)

    def create(self):
        self._convert()
        if self.params.background:
            self._composite()
        super(PbGenerate, self).create()
