# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import setting
import time
from awsec2tools import AwsEC2MetaData
from awsec2tools import AwsEC2Tools
from boto.exception import EC2ResponseError
from datetime import datetime


# Deploy to an instance and using cron.
INSTANCE_ID = AwsEC2MetaData().get('instance-id')
EC2 = AwsEC2Tools(setting.REGION, setting.ID, setting.KEY)
SNAP_ID = EC2.create_snapshot([INSTANCE_ID, ])
print SNAP_ID
#time.sleep(10)
#print EC2.register_image(SNAP_ID[0].id, '/dev/sda1', True)

# Register image
while True:
    try:
        print EC2.register_image(SNAP_ID[0].id, '/dev/sda1', True)
        break
    except EC2ResponseError:
        print '%s: %s is not completed' % (datetime.now(), SNAP_ID[0].id)
        print 'Waitting 10 seconds ...'
        time.sleep(10)
