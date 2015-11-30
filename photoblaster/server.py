"""All webserver logic lives here, including routes"""
from flask import Flask, Response
from flask import request, jsonify, render_template, send_from_directory

import sys
import re
import cherrypy
from paste.translogger import TransLogger
import simplejson as json
import urllib2

from photoblaster.modules import PbGenerate, PbGrid, PbBreaker, PbPattern,\
    PbLandscape, PbGradient, PbProcessError, Pb
from photoblaster.db.models.imcmd import ImCmd
from photoblaster.param import BadParamError
from photoblaster.config import SERVER_HOST, SERVER_PORT, STATIC_FOLDER, \
    GALLERY_TAG_TRANS, WORKING_DIR, LOCAL

# and this jsonp thing

_CLASSNAME_ALIASES = {
    'generate': 'PbGenerate',
    'imgrid': 'PbGrid',
    'imbreak': 'PbBreaker',
    'impattern': 'PbPattern',
    'imgradient': 'PbGradient',
    'landscape': 'PbLandscape',
}


class InvalidUsage(Exception):
    """error class for InvalidUsage"""
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Server(object):
    """Main server class"""
    def __init__(self):
        # self.app = Flask(__name__)
        self.app = Flask(__name__, static_folder=STATIC_FOLDER)
        self._wsgi_server = None
        self._classname_aliases = _CLASSNAME_ALIASES

        @self.app.route('/test', methods=['GET'])
        def test():
            return "HELLO WORLD!"

        @self.app.route('/im/api/<pb_classname>', methods=['POST'])
        def pb(pb_classname):
            x_forwarded_headers = request.headers.getlist("X-Forwarded-For")
            if x_forwarded_headers:
                host = x_forwarded_headers[0]
                regex = re.compile(r'[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+')
                forwarded_ip = regex.search(host).group()
            else:
                forwarded_ip = None
            return self._response_post(
                pb_classname,
                request.form.to_dict(),
                remote_addr=forwarded_ip
            )

        @self.app.errorhandler(InvalidUsage)
        def handle_invalid_usage(error):
            response = jsonify(error.to_dict())
            response.status_code = error.status_code
            return response

        # Static Routes (for local development only!!!)
        @self.app.route('/<path:path>')
        def send_static(path):
            # send_static_file will guess the correct MIME type
            return self.app.send_static_file(path)

        @self.app.route('/proxy', methods=['GET'])
        def proxy_image():
            url = request.args.get("url")
            req = urllib2.Request(url=url)
            req = urllib2.urlopen(req)
            header = req.headers.getheader('content-type')
            if re.match(r'image', header, re.IGNORECASE):
                return req.read()
            else:
                raise InvalidUsage('Improper Usage', status_code=410)

        @self.app.route('/im/data', methods=['GET'])
        def get_data():
            args_dict = request.args.to_dict()
            query_dict = {}
            for elem in ["newfile", "time"]:
                if args_dict.get(elem):
                    query_dict[elem] = args_dict.get(elem)
            if args_dict:
                try:
                    return Response(
                        # flask prevents from returning arrays,
                        # so we need the json module
                        json.dumps(ImCmd.search(**query_dict)),
                        mimetype='application/json'
                    )
                except Exception as e:
                    return str(e)
            else:
                raise InvalidUsage('Improper Usage', status_code=410)

        @self.app.route('/im/gallery/', methods=['GET'])
        @self.app.route('/im/gallery', methods=['GET'])
        def gallery():
            search_params = {}
            qs = []
            if request.args.get('tag'):
                search_params['tag'] = GALLERY_TAG_TRANS[request.args['tag']]
                qs.append("tag=" + request.args['tag'])
            if request.args.get('name'):
                search_params['name'] = request.args['name']
                qs.append("name=" + request.args['name'])
            if request.args.get('addr'):
                search_params['remote_addr'] = request.args['remote_addr']
                qs.append("addr=" + request.args['addr'])
            limit = request.args.get('limit') or 20
            if limit > 100:
                limit = 100
            offset = int(request.args.get('start', 0))
            if request.args.get('random'):
                results = ImCmd.search_random(**search_params)
                qs.append("random=" + request.args['random'])
            else:
                results = ImCmd.search(**search_params)
            images = results.limit(limit).offset(offset).all()
            if LOCAL:
                images = ["/im/cache/%s" % image.newfile for image in images]
            else:
                images = [
                    "http://i.asdf.us/im/%s/%s" %
                    (image.dir, image.newfile) for
                    image in images
                ]
            older = offset + limit
            newer = offset - limit
            qs = "&".join(qs)

            return render_template(
                'gallery.html',
                images=images,
                older=older,
                newer=newer,
                qs=qs
            )

        @self.app.route('/im/cache/<path:path>', methods=['GET'])
        def local_cache(path):
            """
            FOR LOCAL DEVELOPMENT ONLY

            send static file from the WORKING_DIR directory
            this allows the gallery to work locally without s3
            send_static_file will guess the correct MIME type
            FIXME (add WORKING_DIR to function call)
            """
            return send_from_directory(WORKING_DIR, path)

    def _find_class_by_name(self, pb_classname):
        pb_classname = self._classname_aliases.get(pb_classname, None) \
            or pb_classname
        try:
            return filter(
                lambda c: c.__name__ == pb_classname, Pb.__subclasses__()
            )[0]
        except IndexError:
            raise InvalidUsage('No such api', status_code=410)

    def _response_post(self, pb_classname, request_form, remote_addr=None):
        pb_class = self._find_class_by_name(pb_classname)
        # classnames = map(lambda c: c.__name__, Pb.__subclasses__())
        try:
            pb = pb_class(**request_form)
            pb.create()
            if not LOCAL:
                pb.file_s3move()
            pb.db_send(remote_addr=remote_addr)
            json_data = jsonify(pb.file_dict())
            if pb.params.callback:  # accounts for jsonp
                return "%s(%s)" % (pb.params.callback, json_data)
            return json_data

        except BadParamError:
            for i in request_form.keys():
                sys.stderr.write('\'%s\':\'%s\'\n' % (
                    i, request_form[i] or None
                ))
            return jsonify({'error': 'Bad Params'})
        except PbProcessError:
            sys.stderr.write(dict(request_form))
            return jsonify({'error': 'Problem with server-side processing'})

    def run(self, host=SERVER_HOST, port=SERVER_PORT):
        self.app.run(host=host, port=port, debug=True)

    def run_wsgi(self, server_port=SERVER_PORT, host=SERVER_HOST):
        # http://fgimian.github.io/blog/2012/12/08/setting-up-a-rock-solid-python-development-web-server/
        # Enable WSGI access logging via Paste
        app_logged = TransLogger(self.app)

        # Mount the WSGI callable object (app) on the root directory
        cherrypy.tree.graft(app_logged, '/')

        # Set the configuration of the web server
        cherrypy.config.update({
            'engine.autoreload_on': True,
            'log.screen': True,
            'server.socket_port': server_port,
            'server.socket_host': host
        })
        cherrypy.engine.start()
        cherrypy.engine.block()
