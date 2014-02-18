# -*- coding: utf-8 -*-
''' AWS CloudFront Tools '''
from boto.cloudfront import CloudFrontConnection


class AwsCloudFrontTools(object):
    ''' Aws CloudFront Tools

        :param str aws_access_key_id: aws_access_key_id
        :param str aws_secret_access_key: aws_secret_access_key
    '''

    def __init__(self, aws_access_key_id, aws_secret_access_key):
        self.conn = CloudFrontConnection(aws_access_key_id=aws_access_key_id,
                        aws_secret_access_key=aws_secret_access_key)

    def get_all_distributions(self, fields=['id', 'cnames', 'domain_name',
            'origin']):
        ''' Get all distributions

            :param list fields: Get distributions info fields.
            :rtype: dict in list

            .. todo::
               - Add show all distributions data.

        '''
        result = []
        for target in self.conn.get_all_distributions():
            result.append({key: getattr(target, key) for key in fields})

        return result

if __name__ == '__main__':
    import setting
    from pprint import pprint
    cloudfront = AwsCloudFrontTools(setting.ID, setting.KEY)
    pprint(cloudfront.get_all_distributions())
    #print cloudfront.conn.create_invalidation_request('...',
    #                                                  ['index.html',])
