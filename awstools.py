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

if __name__ == '__main__':
    print 'remove comment before use'
    #AwsTools().create_snapshot()
    #print AwsTools().register_image('snap-b2464c5d', '/dev/sda1', True)
