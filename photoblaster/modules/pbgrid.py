from photoblaster.config import DEFAULT_FINALFORMAT, DEFAULT_HEIGHT,\
    DEFAULT_WIDTH, OUTPUT_IMAGE_TYPES,\
    THREEDROTATE, GRID, BIN_CONVERT, BIN_COMPOSITE
from photoblaster.modules import Pb

_DEFAULT_LINE_COLOR = "silver"

class PbGrid(Pb):
    """
    Creates or overlays a grid on an image, and adds 3D perspective
    """
    example_params = {
        'bgimage': 'http://i.asdf.us/im/1a/imBreak_1424909483_xx_abridged___.gif',
        'planebgimage': 'http://i.imgur.com/FICZtph.png',
        'tilt': '30',
        'spacing': '30',
        'hlines': 'true',
        'roll': '30',
        'shadow': 'true',
        'trim': 'true'
    }
    def __init__(self, **kwargs):
        super(PbGrid, self).__init__(**kwargs)
        _definitions = {
            'width': {'type':'int'},
            'height': {'type':'int'},
            'linethickness': {'type':'int', 'default': 1},
            'opacity': {'type':'float', "default": 1.0},
            'linecolor': {'type':'color', 'default': 'whitesmoke'},
            'spacing': {'type':'int', 'default': 10},
            'vlines': {'type':'bool'},
            'hlines': {'type':'bool'},
            'shadow': {'type':'bool'},
            'bgimage': {'type':'img_url'},
            'bgcolor': {'type':'color', 'default': 'transparent'},
            'imageinstead': {'type':'img_url'},
            'planebgcolor': {'type':'color', 'default': 'transparent'},
            'planebgimage': {'type':'img_url'},
            'swing': {'type':'int'},
            'tilt': {'type':'int'},
            'roll': {'type':'int'},
            'zoom': {'type':'float'},
            'skycolor': {'type':'color', 'default': 'transparent'},
            'transition': {
                'type':'enum',
                'enum_values' :[
                    'background', 'dither', 'edge', 'mirror', 'random', 'tile'
                ],
                'default': 'background'
            },
            'trim': {'type':'bool'},
            'finalformat': {
                'type':'enum',
                'enum_values': OUTPUT_IMAGE_TYPES,
                'default': DEFAULT_FINALFORMAT
            },
            'username': {'type':'string'},
        }
        self.params.definitions_import(
            _definitions, kwargs, classname=self.__class__.__name__
        )
        if self.params.imageinstead:
            self.filename, self.filepath = self._filename_filepath_create(
                url=self.params.imageinstead['url'], extension=self.params.finalformat
            )
        elif self.params.planebgimage:
            self.filename, self.filepath = self._filename_filepath_create(
                url=self.params.planebgimage['url'], extension=self.params.finalformat
            )
        else:
            self.filename, self.filepath = self._filename_filepath_create(
                extension=self.params.finalformat
            )

        self._db_url_param = str(
            filter(
                lambda n: n, [
                    self.params.imageinstead, self.params.planebgimage, self.params.bgimage, "NULL"
                ]
            )[0]
        )

    #makes a canvas file...step 1 (if not bgimage)
    def _make_canvas(self):
        dimensions = "{}x{}".format(
            self.params.width or DEFAULT_WIDTH,
            self.params.height or DEFAULT_HEIGHT
        )
        if self.params.bgimage:
            return
        bgcolor = "xc:{}".format(self.params.bgcolor or 'transparent')
        cmd = [BIN_CONVERT, "-size", dimensions, bgcolor, self.filepath]
        self._call_cmd(cmd)

    #2nd step-- run grid
    def _grid_command(self):
        cmd = [GRID]
        if self.params.spacing:
            if self.params.vlines:
                width = 2 * int(self.params.width or DEFAULT_WIDTH)
                cmd += ["-s", "{},{}".format(self.params.spacing, width)]
            elif self.params.hlines:
                height = 2 * int(self.params.height or DEFAULT_HEIGHT)
                cmd += ["-s", "{},{}".format(height, self.params.spacing)]
            else:
                cmd += ["-s", self.params.spacing]
        cmd += ["-c", self.params.linecolor or _DEFAULT_LINE_COLOR]
        if self.params.linethickness:
            cmd += ['-t', self.params.linethickness]
        if self.params.opacity:
            cmd += ['-o', self.params.opacity]
        cmd += [self.filepath, self.filepath]
        self._call_cmd(cmd)

    def _shadow_cmd(self):
        """
        convert 1.png \
        \( +clone -background black -shadow 110x1+9+9 \) \
        +swap -background none -layers merge +repage 2.png
        """
        cmd = [
            BIN_CONVERT,
            self.filepath,
            "(", "+clone", "-background", "black", "-shadow", "100x2+20+10", ")",
            "+swap", "-background", "none", "-layers", "merge", "+repage",
            self.filepath
        ]
        self._call_cmd(cmd)


    def _threed_rotate_cmd(self):
    #3rd step--run 3Drotate
        cmd = [THREEDROTATE]
        if self.params.swing: cmd += ["pan={}".format(self.params.swing)]
        if self.params.tilt: cmd += ["tilt={}".format(self.params.tilt)]
        if self.params.roll: cmd += ["roll={}".format(self.params.roll)]
        if self.params.zoom:
            cmd += ["zoom={}".format(self.params.zoom)]
        if cmd == [THREEDROTATE]: #if nothing has been added
            return
        if self.params.planebgcolor and not self.params.planebgimage:
            cmd += ["bgcolor={}".format(self.params.planebgcolor)]
        else:
            cmd += ["bgcolor=none"]
        cmd += ["skycolor={}".format(self.params.skycolor or 'none')]
        if self.params.transition: cmd += ["vp={}".format(self.params.transition)]
        cmd += [self.filepath, self.filepath]
        self._call_cmd(cmd)


    def _trim_cmd(self):
        cmd = [BIN_CONVERT, self.filepath, "-trim", "+repage", self.filepath]
        self._call_cmd(cmd)

    def _prepare_gridimage(self, image):
        if image['mimetype'] == 'gif':
            _frame = self._choose_gif_frame(image['path'])
        if image['mimetype'] != 'png':
            cmd = [BIN_CONVERT, image['path'], self.filepath]
        else:
            cmd = ['cp', image['path'], self.filepath]
        self._call_cmd(cmd)


    def _overlay_planebgimage(self):
        cmd = [
            BIN_COMPOSITE,
            "-compose", "Dst_Over", "-gravity", "center",
            self.params.planebgimage["path"],
            self.filepath,
            self.filepath
        ]
        self._call_cmd(cmd)

    def create(self):
        if self.params.bgimage:
            self._prepare_gridimage(self.params.bgimage)
            self._grid_command()
        elif self.params.imageinstead:
            self._prepare_gridimage(self.params.imageinstead)
        else:
            self._make_canvas()
            self._grid_command()
        if self.params.shadow: self._shadow_cmd()
        self._threed_rotate_cmd()
        if self.params.planebgimage: self._overlay_planebgimage()
        if self.params.trim: self._trim_cmd()
        super(PbGrid, self).create()
