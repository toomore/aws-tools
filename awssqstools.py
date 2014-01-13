# -*- coding: utf-8 -*-
import setting
from boto.sqs import connect_to_region


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

    def get_messages(self, num_messages=10, *args, **kwargs):
        for i in self.queue.get_messages(num_messages, *args, **kwargs):
            yield i.get_body()

if __name__ == '__main__':
    sqs = AwsSQSTools('test_toomore')
    print sqs.queue
    print sqs.get('test_')
    print dir(sqs.queue)
    #print sqs.write(str(range(10)))
    print list(sqs.get_messages())
