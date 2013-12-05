# -*- coding: utf-8 -*-
from boto import ec2
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.blockdevicemapping import BlockDeviceType
import setting


class AwsTools(object):

    def __init__(self):
        self.conn = ec2.connect_to_region(setting.REGION,
                                     aws_access_key_id=setting.ID,
                                     aws_secret_access_key=setting.KEY)

    def get_all_instances(self):
        return self.conn.get_all_instances(filters={'instance-state-code': 16})

    def create_snapshot(self, dry_run=False):
        for i in self.get_all_instances():
            print 'instance', i.instances[0].id
            volume = self.conn.get_all_volumes(filters={'attachment.instance-id': i.instances[0].id})
            print 'volume', volume

            for v in volume:
                snap = v.create_snapshot('From boto.', dry_run)
                print 'create_snapshot', snap
                print 'Add tag', self.conn.create_tags(snap.id, {'Name': 'AUTO-SNAP','CreatedBy': 'boto'}, dry_run)

    def register_image(self, snapshot_id, root_device_name, delete_on_termination=False):
        root_vol = BlockDeviceType(snapshot_id=snapshot_id,
                                   delete_on_termination=delete_on_termination)
        block_device_map = BlockDeviceMapping()
        block_device_map[root_device_name] = root_vol

        return self.conn.register_image(name='TESTAMI',
                                        description='TEST useing boto.',
                                        architecture='x86_64',
                                        kernel_id='aki-176bf516',
                                        root_device_name=root_device_name,
                                        block_device_map=block_device_map)

if __name__ == '__main__':
    #AwsTools().create_snapshot()
    print AwsTools().register_image('snap-5e6abe7a', '/dev/sda1', True)
