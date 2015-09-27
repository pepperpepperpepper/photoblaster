"""All s3 related methods stored here"""
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET_NAME
import sys
from boto.s3.connection import S3Connection
from boto.s3.key import Key
class S3Cli(object):
    def __init__(self):
        try:
            self.conn = S3Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, is_secure=False)
            self.bucket = self.conn.get_bucket(BUCKET_NAME)
        except Exception as e:
            sys.stderr.write("Could not connect to s3\n")
            sys.stderr.write(str(e))
            sys.exit(1)

    def s3move(self, filename, objectname):
        try:
            k = Key(self.bucket)
            k.key = objectname
            k.set_contents_from_filename(filename)
            k.set_acl('public-read')
            k.storage_class = 'REDUCED_REDUNDANCY'
        except Exception as e:
            sys.stderr.write(str(e))
            sys.exit(1)
