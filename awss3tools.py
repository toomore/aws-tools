# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from cStringIO import StringIO
import setting


class AwsS3Tools(object):
    def __init__(self, bucket):
        self.conn = S3Connection(setting.ID, setting.KEY)
        self.bucket = self.conn.get_bucket(bucket)

    def open(self, filename):
        get_files = self.bucket.get_key(filename)

        if get_files:
            return get_files

        return self.bucket.new_key(filename)

    @staticmethod
    def set_contents(key, file_data):
        return key.set_contents_from_file(file_data)

if __name__ == '__main__':
    bucket = AwsS3Tools('toomore-aet').bucket
    print bucket.get_all_keys()
    print dir(bucket)

    files = AwsS3Tools('toomore-aet').open('toomore.txt')
    print files
    print dir(files)

    # ----- save data ----- #
    #conutent = StringIO()
    #content.write('Toomore is 蔣太多')
    #print files.set_contents_from_string(content.getvalue())

    # ----- save files ----- #
    with open('./README.md') as file_data:
        print AwsS3Tools.set_contents(files, file_data)
