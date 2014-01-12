# -*- coding: utf-8 -*-
import setting
from boto.sqs import connect_to_region
from boto.sqs.connection import SQSConnection


class AwsSQSTools(object):
    def __init__(self, queue_name):
        self.conn = connect_to_region(setting.REGION,
                                      aws_access_key_id=setting.ID,
                                      aws_secret_access_key=setting.KEY)
        self.queue = self.conn.create_queue(queue_name)

    def get(self, *args, **kwargs):
        return self.conn.get_all_queues(*args, **kwargs)

    def write(self, body):
        return self.queue.write(self.queue.new_message(body))

if __name__ == '__main__':
    sqs = AwsSQSTools('test_toomore')
    print sqs.queue
    print sqs.get('test_')
    print dir(sqs.queue)
    print sqs.write(str(range(10)))
