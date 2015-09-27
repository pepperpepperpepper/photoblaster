"""Creates a gradient image and adds effects to it"""

from config import DEFAULT_WIDTH, DEFAULT_HEIGHT, DEFAULT_FINALFORMAT, \
    BIN_CONVERT, BEVELBORDER, OUTPUT_IMAGE_TYPES
from pb import Pb

_DEFAULT_COLOR_1 = "white"
_DEFAULT_COLOR_2 = "black"

_DEFAULT_BEVEL_PERCENT = "12"

_halftone_values = {
    "checkeredfade": "h6x6a",
    "etchedtransition": "o8x8",
    "bendaydots": "h16x16o",
    "smallerdots1": "h8x8o",
    "smallerdots2": "c7x7w",
    "flatstripes": "o2x2",
}

class PbGradient(Pb):
    example_params = {
        "width" : "200",
        "color1" : "#ffdead",
        "color2" : "blue",
        "stripes" : "true",
        "stripenumber" : "20",
        "gradienttype" : "radial",
        "stripeintensity" : "20",
        "halftone" : "checkeredfade",
        "percentbeveled" : "30",
        "flip" : "true",
        "bevel" : "flatinner",
        "rotate" : "20",
        "height" : "200",
        "filetype" : "jpg",
        "username" : "whatever"
    }
    def __init__(self, **kwargs):
        super(PbGradient, self).__init__(**kwargs)
        _definitions = {
            'width': {'type':'int', 'default': DEFAULT_WIDTH},
            'height': {'type':'int', 'default' : DEFAULT_HEIGHT},
            'color1': {'type':'color', 'default': _DEFAULT_COLOR_1},
            'color2': {'type':'color', 'default': _DEFAULT_COLOR_2},
            'stripes': {'type':'bool'},
            'stripenumber': {'type':'int', 'default': 0},
            'stripeintensity': {'type':'int', 'default': 0},
            'blurriness': {'type':'int', 'default': 0},
            'contrast': {'type':'int', 'default': 100},
            'brightness': {'type':'int', 'default': 100},
            'saturation': {'type':'int', 'default': 100},
            'hue': {'type':'int', 'default': 100},
            'halftone': {'type':'enum', 'enum_values' : [
                'checkeredfade', 'etchedtransition', 'bendaydots',
                'smallerdots1', 'smallerdots2', 'flatstripes',
            ]},
            'bevel': {'type':'enum', 'enum_values' : [
                'flatout', 'flatinner', 'evenlyframed', 'biginner',
                'bigouter', 'dramaticflatout', 'dramaticflatinner',
            ]},
            'percentbeveled': {'type':'int', 'default': _DEFAULT_BEVEL_PERCENT},
            'tilt': {'type':'int'},
            'rotate': {'type':'int'},
            'flip': {'type':'bool'},
            'flop': {'type':'bool'},
            'filetype': {
                'type': 'enum',
                'enum_values': OUTPUT_IMAGE_TYPES,
                'default': DEFAULT_FINALFORMAT
            },
            'gradienttype': {'type':'enum', 'enum_values':[
                'gradient', 'canvas', 'radial', 'colorspace',
                'mirrored', 'plasmawash', 'gradientwash', 'noise'
            ], 'default': 'gradient'},
            'username': {'type':'string'}
        }
        self.params.definitions_import(_definitions, kwargs, classname=self.__class__.__name__)

        self.filename, self.filepath = self._filename_filepath_create()

    def _filename_create(self):
        _base = "{}{}-{}_{}".format(
            self.__class__.__name__,
            str(self.params.color1).replace('#', '').replace('(', '-').replace(')', '-'),
            str(self.params.color2).replace('#', '').replace('(', '-').replace(')', '-'),
            self._now,
        )
        if self.params.username: _base += "_%s" % self.params.username
        return _base + ".%s" % self.params.filetype


    def _build_cmd(self):
        cmd = [BIN_CONVERT]
        cmd.extend([
            '-size',
            "{}x{}".format(self.params.width, self.params.height)
        ])

        if self.params.rotate:
            cmd.extend(["-rotate", self.params.rotate])
        if self.params.tilt:
            cmd.extend(["-distort", "SRT", self.params.tilt])
        if self.params.flip == "true":
            cmd.append("-flip")
        if self.params.flop == "true":
            cmd.append("-flop")
        if self.params.contrast:
            cmd.extend(["-contrast-stretch", self.params.contrast])
        _gradients = {
            "gradient" : ["gradient:{}-{}".format(self.params.color1, self.params.color2)],
            "canvas" : ["canvas:{}".format(self.params.color1)],
            "radial" : [
                "radial-gradient:{}-{}".format(self.params.color1, self.params.color2)
            ],
            "colorspace" : [
                "-colorspace",
                "Gray",
                "plasma:{}-{}".format(self.params.color1, self.params.color2)
            ],
            "mirrored" : [
                "plasma:{}-{}".format(self.params.color1, self.params.color2),
                "\(", "+clone", "-flop", "\)",
                "append"
            ],
            "plasmawash" : [
                "plasma:{}-{}".format(self.params.color1, self.params.color2),
                "-set", "colorspace", "HSB"
            ],
            "gradientwash" : [
                "gradient:{}-{}".format(self.params.color1, self.params.color2),
                "-set", "colorspace", "HSB"
            ],
            "noise" : ["xc:", "+noise", "Random", "-virtual-pixel", "tile"]
            }
        cmd += _gradients[str(self.params.gradienttype)]

        if self.params.blurriness:
            cmd.extend(["-blur", "0x{}".format(self.params.blurriness), "-auto-level"])

        if self.params.stripes == "true" and len(self.params.stripenumber):
            cmd.extend(["-function", "Sinusoid"])
            if self.params.stripeintensity:
                cmd.append("{},{}".format(self.params.stripenumber, self.params.stripeintensity))
            else:
                cmd.append(self.params.stripenumber)
        if str(self.params.halftone) in _halftone_values:
            cmd.extend([
                "-ordered-dither",
                _halftone_values[str(self.params.halftone)]
            ])
        cmd += [
            '-modulate',
            "{},{},{}".format(
                self.params.brightness or "100",
                self.params.saturation or "100",
                self.params.hue or "100"
            )
        ]
        cmd.append(self.filepath)
        self._call_cmd(cmd)
        if self.params.bevel: self._make_bevel()

    def _get_bevelvalue(self):
        w, h = map(int, (self.params.width, self.params.height))
        if h >= w:
            bevpercentval = str(int(self.params.percentbeveled)*0.005*int(h))
        else:
            bevpercentval = str(int(self.params.percentbeveled)*0.005*int(w))
        return {
            "flatout": ["-s", bevpercentval, "-m", "outer"],
            "flatinner": ["-s", bevpercentval, "-m", "inner"],
            "evenlyframed": ["-s ", bevpercentval, "-m", "split"],
            "biginner": ["-s", bevpercentval, "-m", "outer", "-c", "50", "-b", "red", "-a", "25"],
            "bigouter": ["-s", bevpercentval, "-m", "split", "-c", "50", "-b", "red", "-a", "25"],
            "dramaticflatout": ["-s", bevpercentval, "-m", "outer", "-a", "25", "-b", "blue"],
            "dramaticflatinner": ["-s", bevpercentval, "-m", "outer", "-a", "25", "-b", "blue"],
        }[str(self.params.bevel)]

    def _make_bevel(self):
        cmd = [BEVELBORDER]
        cmd += self._get_bevelvalue()
        cmd += [self.filepath, self.filepath]
        self._call_cmd(cmd)

    def create(self):
        self._build_cmd()
        super(PbGradient, self).create()
