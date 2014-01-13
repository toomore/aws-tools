# -*- coding: utf-8 -*-
''' AwsSQSTools '''
import setting
from boto.sqs import connect_to_region


class AwsSQSTools(object):
    ''' AwsSQSTools '''
    def __init__(self, queue_name):
        self.conn = connect_to_region(setting.REGION,
                                      aws_access_key_id=setting.ID,
                                      aws_secret_access_key=setting.KEY)
        self.queue = self.conn.create_queue(queue_name)

    def get_all_queues(self, *args, **kwargs):
        ''' Get all queue '''
        return self.conn.get_all_queues(*args, **kwargs)

    def write(self, body):
        ''' Write a message into queue '''

        return self.queue.write(self.queue.new_message(body))

    def get_messages(self, num_messages=10, *args, **kwargs):
        ''' Get messages from queue '''
        #TODO Need to increase `get_messages` concurrency.
        for i in self.queue.get_messages(num_messages, *args, **kwargs):
            yield i.get_body()

if __name__ == '__main__':
    SQS = AwsSQSTools('test_toomore')
    print SQS.queue
    print SQS.get_all_queues('test_')
    print dir(SQS.queue)
    #print SQS.write(str(range(10)))
    print list(SQS.get_messages())
