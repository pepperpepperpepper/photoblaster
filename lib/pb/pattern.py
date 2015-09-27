from config import BIN_CONVERT, BIN_COMPOSITE
from pb import Pb
from PIL import Image

_FUSE_MODE="Pin_Light"

class PbPattern(Pb):
    example_params = {
         "pattern_data" : '{"matrix":[["0","0","0","0","0","1","0","0","0","0"],["0","0","0","0","1","1","1","0","0","0"],["0","0","1","1","1","0","1","0","0","0"],["0","1","1","0","0","0","0","0","0","0"],["0","1","0","0","1","0","0","0","0","0"],["0","1","0","0","1","0","0","0","1","0"],["0","1","0","0","1","1","0","0","1","0"],["0","1","0","0","0","1","1","1","1","0"],["0","1","1","1","1","0","0","0","0","0"],["0","0","0","0","1","0","0","0","0","0"]],"width":"10","height":"10"}',
         "image_url" : "http://i.asdf.us/im/be/PinkHijab_1425078647_reye.gif",
#        "username" : "garfield",
#        "pattern_url" : "http://asdf.us/impattern/patterns/1.png",
    } 
    def __init__(self, **kwargs): 
        super(PbPattern, self).__init__(**kwargs)
        _definitions = {
            'image_url': {'type':'img_url'},
            'pattern_url': {'type':'img_url'},
            'pattern_data': {'type':'json'},
            'username': {'type':'string'},
        }
        self.params.definitions_import(_definitions, kwargs, classname=self.__class__.__name__)
        self.filename, self.filepath = self._filename_filepath_create(
            url=self.params.image_url['url'], extension=self.params.image_url['mimetype']
        )
        if self.params.pattern_data:
            _pattern_filename, self._pattern_filepath = self._filename_filepath_create(namepart="pattern")
            self._from_pattern_data()
        elif not self.params.pattern_url:
            self.err_warn("pattern must be supplied as json array or as a png url")
        else:
            self._pattern_filepath = self.params.pattern_url['path']

        self._db_url_param = str(self.params.image_url.url)


    def _from_pattern_data(self):
        def boolToColor(boolean):
            if boolean:
                return (0, 0, 0, 255)
            else:
                return (255, 255, 255, 255)
        specs = self.params.pattern_data.value
        if int(specs['width']) > 100 or int(specs['height']) > 100:
            self.err_warn("height and width need to be less than 100 px")
        img = Image.new('RGBA', (int(specs['width']), int(specs['height'])))
        pixels = img.load()
        for i in range(0, len(specs['matrix'])):
            for j in range(0, len(specs['matrix'][i])):
                pixels[j, i] = boolToColor(int(specs['matrix'][i][j]))

        img.save(self._pattern_filepath, "PNG")
        
    #first step
    def _make_canvas(self):
        _width, _height = self._dimensions(self.params.image_url['path']) # same here
        cmd = [BIN_CONVERT, "-size", _width + "x" + _height, "canvas:transparent", self.filepath]
        self._call_cmd(cmd)

    #second step use the Canvas as a background
    def _make_mask(self):
        #tile the pattern pattern on the canvas
        cmd = [BIN_COMPOSITE, "-tile", self._pattern_filepath, self.filepath, self.filepath]
        self._call_cmd(cmd)
        #fuse the tiled file to create a mask
        #convert thebg.gif -compose Dst_In null: thefile.gif -matte -layers composite new.gif
        cmd = [
            BIN_CONVERT, self.filepath, "-compose", "Dst_In", "null:", 
            self.params.image_url['path'], "-matte", "-layers", "composite", self.filepath
        ]
        self._call_cmd(cmd)
    
    #third step
    def _fuse_mask(self, fuse_mode=_FUSE_MODE):
        cmd = [
            BIN_CONVERT, "-dispose", "2", self.filepath, "null:", 
            self.params.image_url['path'], "-matte", "-compose", fuse_mode, "-layers", "composite", 
            self.filepath
        ]
        self._call_cmd(cmd)

    def create(self):
        self._make_canvas()
        self._make_mask()
        self._fuse_mask()
        super(PbPattern, self).create()
