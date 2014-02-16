# -*- coding: utf-8 -*-
''' AWS CloudFront Tools '''
import setting
from boto.cloudfront import CloudFrontConnection

class AwsCloudFrontTools(object):
    ''' Aws CloudFront Tools '''

    def __init__(self):
        self.conn = CloudFrontConnection(aws_access_key_id=setting.ID,
                                         aws_secret_access_key=setting.KEY)

    def get_all_distributions(self, fields=['id', 'cnames', 'domain_name',
            'origin']):
        ''' Get all distributions

            :param list fields: Get distributions info fields.
            :rtype: dict in list
        '''
        result = []
        for target in self.conn.get_all_distributions():
            result.append({key: getattr(target, key) for key in fields})

        return result

if __name__ == '__main__':
    from pprint import pprint
    cloudfront = AwsCloudFrontTools()
    pprint(cloudfront.get_all_distributions())
    #print cloudfront.conn.create_invalidation_request('...',
    #                                                  ['index.html',])
