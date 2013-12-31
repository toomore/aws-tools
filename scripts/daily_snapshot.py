# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from awsec2tools import AwsEC2Tools
from awsec2tools import AwsEC2MetaData

instance_id = AwsEC2MetaData().get('instance-id')
print AwsEC2Tools().create_snapshot([instance_id, ])
