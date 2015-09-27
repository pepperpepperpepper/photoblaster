MAX_SIZE = 1024 * 1024 * 1.2 * 1.5

#PATHS
BIN_CONVERT = "/usr/bin/convert"
BIN_COMPOSITE = "/usr/bin/composite"
BIN_IDENTIFY = "/usr/bin/identify"
THREEDROTATE = "./bin/3Drotate"
GRID = "./bin/grid"
BEVELBORDER = "./bin/bevelborder"

#common parameters
DEFAULT_FINALFORMAT = "png";
DEFAULT_HEIGHT = 400
DEFAULT_WIDTH = 600

OUTPUT_IMAGE_TYPES = ["png", "jpg", "gif"]

#mounted on tmpfs
WORKING_DIR = "/var/www/cache"


#server
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 9000

#s3
AWS_ACCESS_KEY_ID = 'nope'
AWS_SECRET_ACCESS_KEY = 'nope'
BUCKET_NAME = 'i.asdf.us'
SPECIAL_DOWNLOADERS = ['nobody']
SPECIAL_DOWNLOADERS_MAX_SIZE = 1000


#database
DB_HOST = "nope.com"
DB_USER = "nope"
DB_PASSWORD = "nope"
DB_NAME = "nope"
