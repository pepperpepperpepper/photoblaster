from photoblaster.config import *
import base64
from photoblaster.modules import Pb
import urlparse, re

class PbLandscape(Pb):
    example_params = {
        'imgdata' : open('photoblaster/modules/pblandscape/_base64img', 'rb').read(),
        'texture' : 'http://someurl.biz/someimg.jpg',
        'heightmap' : 'http://someurl.biz/someimg.jpg',
        'name' : 'donkey'
    }
    def __init__(self, **kwargs):
        super(PbLandscape, self).__init__(**kwargs)
        _definitions = {
            'heightmap': {'type': 'string'},
            'imgdata': {'type': 'raw'},
            'texture': {'type': 'string'},
            'username': {'type': 'string'},
        }
        self.params.definitions_import(_definitions, kwargs, classname=self.__class__.__name__)
        _namepart = re.sub(r'https?:?/?/?', '', str(self.params.texture))
        self.filename, self.filepath = self._filename_filepath_create(url=_namepart, extension="png")

        self._db_url_param = str(self.params.texture)

    def _saveImgData(self):
        try:
            up = urlparse.urlparse(str(self.params.imgdata))
            head, data = up.path.split(',', 1)
            bits = head.split(';')
            #mime_type = bits[0] if bits[0] else 'text/plain'
            #charset, b64 = 'ASCII', False
            #for bit in bits[1]:
            #    if bit.startswith('charset='):
            #        charset = bit[8:]
            #    elif bit == 'base64':
            #        b64 = True

            # Do something smart with charset and b64 instead of assuming
            plaindata = base64.b64decode(data)

            with open(self.filepath, 'wb') as f:
                f.write(plaindata)
        except Exception as e:
            self.err_warn(str(e))

    def create(self, breakmode=""):
        self._saveImgData()
        super(PbLandscape, self).create()
