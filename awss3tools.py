# -*- coding: utf-8 -*-
'''
Files create, update, read, delete through AWS S3.
'''
import setting
from boto.s3.connection import S3Connection
from cStringIO import InputType
from cStringIO import OutputType
from cStringIO import StringIO


class AwsS3Tools(object):
    ''' AwsS3Tools

        :param str bucket: s3 bucket Name
        :param str open_file: filename, the same with s3 object key name.
        :rtype: :class:`boto.s3.connection`
        :return: :class:`boto.s3.connection`

        Connect bucket with filename:

        >>> FILES = AwsS3Tools('toomore-aet', 'toomore.txt')
        >>> print FILES

        Connect bucket without filename but using
        :py:func:`open`:

        >>> FILES = AwsS3Tools('toomore-aet')
        >>> FILES.open('toomore.txt')
    '''
    def __init__(self, bucket, open_file=None):
        self.conn = S3Connection(setting.ID, setting.KEY)
        self.bucket = self.conn.get_bucket(bucket)
        if open_file:
            self.open(open_file)
        else:
            self.keys = None

    def open(self, filename):
        ''' Open a file by keyname

            :param str filename: filename, the same with s3 object key name.

            >>> FILES.open('toomore.txt')

            .. note::
               No return value, key object will put into :attr:`AwsS3Tools.keys`

        '''
        get_files = self.bucket.get_key(filename)
        result = get_files if get_files else self.bucket.new_key(filename)
        self.keys = result

    def save(self, file_data, make_public=False):
        ''' Save file to S3

            :param file file_data: file data
            :param bool make_public: to be public
            :rtype: int
            :returns: file size in byte.

            >>> with open('./README.md') as file_data:
            ...     print FILES.save(file_data, True)

        '''
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
        ''' Read file from S3

            :rtype: :py:class:`cStringIO.StringIO`

            >>> content = FILES.read()
            >>> print content.read()
        '''
        result = StringIO()
        self.keys.get_contents_to_file(result)
        result.seek(0)

        return result

    def update(self, file_data, *args, **kwargs):
        ''' Update file.

            :param file file_data: file data
            :rtype: int
            :returns: file size in byte.

            >>> content = FILES.read()
            >>> print content.read()
            >>> content.writelines('Toomore is Toomore')
            >>> FILES.update(content)
            >>> print FILES.read().getvalue()

            .. todo:: update key with the same acl.
        '''
        return self.save(file_data, *args, **kwargs)

    def delete(self):
        ''' Delete file. '''
        return self.keys.delete()

if __name__ == '__main__':
    #bucket = AwsS3Tools('toomore-aet').bucket
    #print bucket.get_all_keys()
    #print dir(bucket)

    # ----- create data 1 ----- #
    #FILES = AwsS3Tools('toomore-aet', 'toomore.txt')
    #print FILES
    #print dir(FILES)

    # ----- create data 2 ----- #
    FILES = AwsS3Tools('toomore-aet')
    FILES.open('toomore.txt')

    # ----- save data ----- #
    content = StringIO()
    content.write('Toomore is 蔣太多')
    print FILES.save(content.getvalue(), True)

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
