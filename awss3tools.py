# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import setting


class AwsS3Tools(object):
    def __init__(self):
        self.conn = S3Connection(setting.ID, setting.KEY)

    def get_bucket(self, bucket):
        return self.conn.get_bucket(bucket)

if __name__ == '__main__':
    print AwsS3Tools().get_bucket('toomore-aet').get_all_keys()
