# -*- coding: utf-8 -*-
import sys
import os
sys.path.insert(0, '../')

import time
from awsec2tools import AwsEC2MetaData
from awsec2tools import AwsEC2Tools


# Deploy to an instance and using cron.
INSTANCE_ID = AwsEC2MetaData().get('instance-id')
SNAP_ID = AwsEC2Tools().create_snapshot([INSTANCE_ID, ])
print SNAP_ID
time.sleep(10)
print AwsEC2Tools().register_image(SNAP_ID[0].id, '/dev/sda1', True)
