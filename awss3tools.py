# -*- coding: utf-8 -*-
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from cStringIO import InputType
from cStringIO import OutputType
from cStringIO import StringIO
import setting


class AwsS3Tools(object):
    def __init__(self, bucket, open_file=None):
        self.conn = S3Connection(setting.ID, setting.KEY)
        self.bucket = self.conn.get_bucket(bucket)
        self.keys = self.open(open_file)

    def open(self, filename):
        get_files = self.bucket.get_key(filename)

        if get_files:
            return get_files

        return self.bucket.new_key(filename)

    def save(self, file_data, make_public=None):
        if isinstance(file_data, (file, InputType, OutputType)):
            if isinstance(file_data, (InputType, OutputType)):
                file_data.seek(0)

            result = self.keys.set_contents_from_file(file_data)
        elif isinstance(file_data, str):
            result = self.keys.set_contents_from_string(file_data)
        else:
            return type(file_data)

        self.keys.make_public() if make_public else None
        return result

    def read(self):
        result = StringIO()
        self.keys.get_contents_to_file(result)
        result.seek(0)

        return result

    def update(self, file_data, *args, **kwargs):
        return self.save(file_data, *args, **kwargs)

if __name__ == '__main__':
    #bucket = AwsS3Tools('toomore-aet').bucket
    #print bucket.get_all_keys()
    #print dir(bucket)

    # ----- create data ----- #
    files = AwsS3Tools('toomore-aet', 'toomore.txt')
    print files
    print dir(files)

    # ----- save data ----- #
    #content = StringIO()
    #content.write('Toomore is 蔣太多')
    #print files.save(content.getvalue(), True)

    # ----- save files ----- #
    #with open('./README.md') as file_data:
    #    print files.save(file_data, True)

    # ----- read files ----- #
    content = files.read()
    print content.read()

    # ----- update files ----- #
    content.writelines('Toomore is Toomore')
    content.writelines('Toomore is Toomore')
    print files.update(content)
    print files.read().getvalue()

    # ----- delete files ----- #
    #print files.delete()

    # ----- generate url ----- #
    #print files.generate_url(30)
