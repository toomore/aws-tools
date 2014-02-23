# -*- coding: utf-8 -*-
''' My AWS Glacier Tools '''
from boto.glacier.layer2 import Layer2

class AwsGlacierTools(Layer2):
    def __init__(self, *args, **kwargs):
        super(AwsGlacierTools, self).__init__(*args, **kwargs)

if __name__ == '__main__':
    import setting
    glacier = AwsGlacierTools(aws_access_key_id=setting.ID,
            aws_secret_access_key=setting.KEY,
            region_name=setting.REGION)
    print glacier.list_vaults()
