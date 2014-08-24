# -*- coding: utf-8 -*-
''' My AWS Tools '''
import urllib2
from boto.ec2 import regions
from boto.ec2.blockdevicemapping import BlockDeviceMapping
from boto.ec2.blockdevicemapping import BlockDeviceType
from boto.ec2.connection import EC2Connection
from boto.ec2.networkinterface import NetworkInterfaceCollection
from boto.ec2.networkinterface import NetworkInterfaceSpecification
from datetime import datetime


class AwsEC2Tools(EC2Connection):
    ''' AWS tools '''

    def __init__(self, region, aws_access_key_id, aws_secret_access_key):
        ''' Make a connect '''
        super(AwsEC2Tools, self).__init__(aws_access_key_id,
                aws_secret_access_key,
                region=[i for i in regions() if i.name == region][0])

    def get_all_instances(self):
        ''' Get all on running instances

            :rtype: list
            :returns: A list of :class:`boto.ec2.instance.Reservation`
        '''

        return super(AwsEC2Tools, self).get_all_instances(filters={'instance-state-code': 16})

    def create_snapshots(self, instances_id=None, dry_run=False):
        '''Create a snapshot with running instances

           :param str instances_id: instances id.
           :param bool dry_run: dry_run.
           :returns: snapshot id
           :rtype: str
        '''
        if instances_id:
            assert isinstance(instances_id, list)
        else:
            instances_id = []
            for i in self.get_all_instances():
                print 'instance', i.instances[0].id
                instances_id.append(i.instances[0].id)

        print instances_id

        result_snap = []
        for i in instances_id:
            volumes = self.get_all_volumes(filters={
                    'attachment.instance-id': i})

            for volume in volumes:
                now = datetime.now()
                snap = volume.create_snapshot(description='%s %s' % (i, now),
                        dry_run=dry_run)
                result_snap.append(snap)
                print 'create_snapshot', snap
                print 'Add tag', self.create_tags(snap.id,
                        {'Name': 'AUTO-%02d%02d-%s' % (now.month, now.day, i),
                         'CreatedBy': 'boto'}, dry_run)

        return result_snap

    def register_image(self, snapshot_id, root_device_name,
            delete_on_termination=False):
        ''' Register a AMI

            :param str snapshot_id: snapshot id
            :param path root_device_name: path of root device
            :param bool delete_on_termination: delete on termination
            :rtype: string
            :returns: The new image id

            .. todo::
               - Remove `kernel_id` hard code.

        '''

        # To make delete_on_termination, need to create a block_device_map
        root_vol = BlockDeviceType(snapshot_id=snapshot_id,
                                   delete_on_termination=delete_on_termination)
        block_device_map = BlockDeviceMapping()
        block_device_map[root_device_name] = root_vol

        now = datetime.now()
        return super(AwsEC2Tools, self).register_image(
                name='AMI-%02d%02d-%s' % (now.month, now.day, snapshot_id),
                description='AMI-%02d%02d-%s' % (now.month, now.day,
                    snapshot_id),
                architecture='x86_64',
                kernel_id='aki-176bf516',
                root_device_name=root_device_name,
                block_device_map=block_device_map)

    def run_from_image(self, image_id):
        ''' Create instance from image in VPC

            :param str image_id: image id.
            :rtype: :class:`boto.ec2.instance.Reservation`
            :returns: The :class:`boto.ec2.instance.Reservation` associated with
                      the request for machines

            .. todo::
               - Remove `subnet_id`, `security_group_ids` hard code.

        '''
        image = self.get_image(image_id)
        image.run(instance_type='t1.micro', security_group_ids=['sg-16d2d974',],
                  subnet_id='subnet-4e8fda08', #VPC
                  instance_initiated_shutdown_behavior='terminate')
        return image

    def run_spot_instances_from_image(self, image_id, price):
        ''' Create spot instances from image_id

            :param str image_id: image id.
            :param str price: max limit price.
            :rtype: :class:`boto.ec2.spotinstancerequest.SpotInstanceRequest`
            :returns: The :class:`boto.ec2.spotinstancerequest.SpotInstanceRequest`
                      associated with the request for machines.

            .. todo::
               - Remove `network_interfaces` hard code and using setting.

        '''
        network_interfaces = NetworkInterfaceSpecification(
                                subnet_id='subnet-4e8fda08',
                                private_ip_address='10.0.11.123',
                                groups=['sg-16d2d974',],
                                associate_public_ip_address=True,
                                description='spot instances from boto')

        network_interfaces = NetworkInterfaceCollection(network_interfaces)

        return self.request_spot_instances(price=str(price),
                                         image_id=image_id,
                                         count=1,
                                         instance_type='t1.micro',
                                         kernel_id='aki-176bf516',
                                         network_interfaces=network_interfaces)

    def get_spot_price_history(self):
        ''' Get spot instances history

            :rtype: list
            :returns: A list tuples containing price and timestamp.

            .. todo::
               - Remove `availability_zone`, `instance_type` hard code.

        '''
        return super(AwsEC2Tools, self).get_spot_price_history(
                        instance_type='t1.micro',
                        product_description='Linux/UNIX (Amazon VPC)',
                        availability_zone='ap-northeast-1c',
                        max_results='20')

class AwsEC2MetaData(object):
    ''' Show EC2 user/meta data
        http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AESDG-chapter-instancedata.html
    '''
    METADATAURL = 'http://169.254.169.254/latest/meta-data'

    def __init__(self):
        pass

    @classmethod
    def get(cls, data=''):
        ''' get meta-data info

            :param str data: data name.
            :rtype: str
            :returns: instance data.
        '''
        result = urllib2.urlopen('%s/%s' % (cls.METADATAURL, data))
        return result.read()

    @classmethod
    def keys(cls):
        ''' Show all meta data keys

            :rtype: str
            :returns: all meta data key name.
        '''
        result = cls.get().split('\n')
        return result

if __name__ == '__main__':
    print 'remove comment before use'
    # ----- AwsEC2Tools ----- #
    #import setting
    #EC2 = AwsEC2Tools(setting.REGION, setting.ID, setting.KEY)
    #print EC2.get_all_instances()
    #EC2.create_snapshot()
    #EC2.create_snapshot(['i-3aa6a538',])
    #print EC2.register_image('snap-b2464c5d', '/dev/sda1', True)
    #print EC2.run_from_image('ami-73fa9972')
    #print EC2.create_tags('i-ebcd6aee', {'Name': 'From boto'})
    #for i in EC2.get_spot_price_history():
    #    print i.region, i.availability_zone, i.timestamp, i.price
    #print EC2.run_spot_instances_from_image('ami-73fa9972', '0.007')
    #print EC2.terminate_instances('i-ae776dac')
    #print EC2.cancel_spot_instance_requests('sir-6c9b0c5b')

    # ----- AwsEC2MetaData ----- #
    #print AwsEC2MetaData.get('instance-id')
    #print AwsEC2MetaData.keys()
    #for i in AwsEC2MetaData.keys():
    #    print i, AwsEC2MetaData.get(i)
