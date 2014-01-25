# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, '../')

import time
from awsec2tools import AwsEC2MetaData
from awsec2tools import AwsEC2Tools
from boto.exception import EC2ResponseError
from datetime import datetime


# Deploy to an instance and using cron.
INSTANCE_ID = AwsEC2MetaData().get('instance-id')
SNAP_ID = AwsEC2Tools().create_snapshot([INSTANCE_ID, ])
print SNAP_ID
#time.sleep(10)
#print AwsEC2Tools().register_image(SNAP_ID[0].id, '/dev/sda1', True)

# Register image
AMIOK_LOOP = True
while AMIOK_LOOP:
    try:
        print AwsEC2Tools().register_image(SNAP_ID[0].id, '/dev/sda1', True)
        AMIOK_LOOP = False
    except EC2ResponseError:
        print '%s: %s is not completed' % (datetime.now(), SNAP_ID[0].id)
        print 'Waitting 10 seconds ...'
        time.sleep(10)
