# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from awsec2tools import AwsEC2Tools
from awsec2tools import AwsEC2MetaData

# Deploy to an instance and using cron.
INSTANCE_ID = AwsEC2MetaData().get('instance-id')
print AwsEC2Tools().create_snapshot([INSTANCE_ID, ])
