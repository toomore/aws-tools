# -*- coding: utf-8 -*-
''' My AWS Tools '''
from boto import ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.blockdevicemapping import BlockDeviceType
from datetime import datetime
import setting


class AwsTools(object):
    ''' AWS tools '''

    def __init__(self):
        ''' Make a connect '''
        self.conn = ec2.connect_to_region(setting.REGION,
                                     aws_access_key_id=setting.ID,
                                     aws_secret_access_key=setting.KEY)

    def get_all_instances(self):
        ''' Get all on running instances'''
        return self.conn.get_all_instances(filters={'instance-state-code': 16})

    def create_snapshot(self, dry_run=False):
        '''Create a snapshot with running instances '''
        for i in self.get_all_instances():
            print 'instance', i.instances[0].id
            volumes = self.conn.get_all_volumes(filters={
                    'attachment.instance-id': i.instances[0].id})
            print 'volume', volumes

            for volume in volumes:
                now = datetime.now()
                snap = volume.create_snapshot('AUTO SNAPSHOT %s' % now, dry_run)
                print 'create_snapshot', snap
                print 'Add tag', self.conn.create_tags(snap.id,
                        {'Name': 'AUTO-SNAP-%s%s' % (now.month, now.day),
                         'CreatedBy': 'boto'}, dry_run)

    def register_image(self, snapshot_id, root_device_name,
            delete_on_termination=False):
        ''' Register a AMI '''

        # To make delete_on_termination, need to create a block_device_map
        root_vol = BlockDeviceType(snapshot_id=snapshot_id,
                                   delete_on_termination=delete_on_termination)
        block_device_map = BlockDeviceMapping()
        block_device_map[root_device_name] = root_vol

        now = datetime.now()
        return self.conn.register_image(name='AMI-%s%s' % (now.month, now.day),
                                        description='AMI-%s%s' % (now.month,
                                                                  now.day),
                                        architecture='x86_64',
                                        kernel_id='aki-176bf516',
                                        root_device_name=root_device_name,
                                        block_device_map=block_device_map)

    def run_from_image(self, image_id):
        ''' Create instance from image in VPC '''
        image = self.conn.get_image(image_id)
        image.run(instance_type='t1.micro', security_group_ids=['sg-16d2d974',],
                  subnet_id='subnet-4e8fda08', #VPC
                  instance_initiated_shutdown_behavior='terminate')
        return image

    def run_spot_instances_from_image(self, image_id, price):
        ''' Create spot instances from image '''
        return self.conn.request_spot_instances(price=str(price),
                                         image_id=image_id,
                                         count=1,
                                         #security_groups=['default',],
                                         instance_type='t1.micro',
                                         kernel_id='aki-176bf516',
                                         subnet_id='subnet-4e8fda08',
                                         security_group_ids=['sg-16d2d974',])

    def get_spot_price_history(self):
        ''' Get spot instances history '''
        return self.conn.get_spot_price_history(
                        instance_type='t1.micro',
                        product_description='Linux/UNIX (Amazon VPC)',
                        availability_zone='ap-northeast-1c',
                        max_results='20')

if __name__ == '__main__':
    print 'remove comment before use'
    #AwsTools().create_snapshot()
    #print AwsTools().register_image('snap-b2464c5d', '/dev/sda1', True)
    #print AwsTools().run_from_image('ami-73fa9972')
    #print AwsTools().conn.create_tags('i-ebcd6aee', {'Name': 'From boto'})
    #for i in AwsTools().get_spot_price_history():
    #    print i.region, i.availability_zone, i.timestamp, i.price
    #print AwsTools().run_spot_instances_from_image('ami-73fa9972', '0.008')
    #print AwsTools().conn.terminate_instances('i-ae776dac')
    #print AwsTools().conn.cancel_spot_instance_requests('sir-6c9b0c5b')
