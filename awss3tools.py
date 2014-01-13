# -*- coding: utf-8 -*-
''' AwsS3Tools  '''
import setting
from boto.s3.connection import S3Connection
from cStringIO import InputType
from cStringIO import OutputType
from cStringIO import StringIO


class AwsS3Tools(object):
    ''' AwsS3Tools '''
    def __init__(self, bucket, open_file=None):
        self.conn = S3Connection(setting.ID, setting.KEY)
        self.bucket = self.conn.get_bucket(bucket)
        self.keys = self.open(open_file)

    def open(self, filename):
        ''' Open a file by keyname '''
        get_files = self.bucket.get_key(filename)

        if get_files:
            return get_files

        return self.bucket.new_key(filename)

    def save(self, file_data, make_public=None):
        ''' Save file to S3 '''
        if isinstance(file_data, (file, InputType, OutputType)):
            if isinstance(file_data, (InputType, OutputType)):
                file_data.seek(0)

            result = self.keys.set_contents_from_file(file_data)
        elif isinstance(file_data, str):
            result = self.keys.set_contents_from_string(file_data)
        else:
            return type(file_data)

        if make_public:
            self.keys.make_public()

        return result

    def read(self):
        ''' Read file from S3 '''
        result = StringIO()
        self.keys.get_contents_to_file(result)
        result.seek(0)

        return result

    def update(self, file_data, *args, **kwargs):
        ''' Update file. '''
        return self.save(file_data, *args, **kwargs)

    def delete(self):
        ''' Delete file. '''
        return self.keys.delete()

if __name__ == '__main__':
    #bucket = AwsS3Tools('toomore-aet').bucket
    #print bucket.get_all_keys()
    #print dir(bucket)

    # ----- create data ----- #
    FILES = AwsS3Tools('toomore-aet', 'toomore.txt')
    print FILES
    print dir(FILES)

    # ----- save data ----- #
    #content = StringIO()
    #content.write('Toomore is 蔣太多')
    #print FILES.save(content.getvalue(), True)

    # ----- save files ----- #
    #with open('./README.md') as file_data:
    #    print FILES.save(file_data, True)

    # ----- read files ----- #
    #content = FILES.read()
    #print content.read()

    # ----- update files ----- #
    #content.writelines('Toomore is Toomore')
    #content.writelines('Toomore is Toomore')
    #print FILES.update(content)
    #print FILES.read().getvalue()

    # ----- get keys acl ----- #
    #print dir(FILES.keys)
    #print dir(FILES.keys.get_acl())
    #print FILES.keys.get_acl().to_xml()

    # ----- delete files ----- #
    #print FILES.delete()

    # ----- generate url ----- #
    #print FILES.generate_url(30)
