# -*- coding: utf-8 -*-
import setting
from boto.cloudfront import CloudFrontConnection

class AwsCloudFrontTools(object):

    def __init__(self):
        self.conn = CloudFrontConnection(aws_access_key_id=setting.ID,
                                         aws_secret_access_key=setting.KEY)

    def get_all_distributions(self, fields=['id', 'cnames', 'domain_name',
            'origin']):
        result = []
        for target in self.conn.get_all_distributions():
            result.append({key: getattr(target, key) for key in fields})

        return result

if __name__ == '__main__':
    cloudfront = AwsCloudFrontTools()
    print cloudfront.get_all_distributions()
