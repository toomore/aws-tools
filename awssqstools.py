# -*- coding: utf-8 -*-
''' AwsSQSTools '''
from base64 import b64encode
from boto.sqs import regions
from boto.sqs.connection import SQSConnection


class AwsSQSTools(SQSConnection):
    ''' AwsSQSTools

        :param str aws_access_key_id: aws_access_key_id
        :param str aws_secret_access_key: aws_secret_access_key
        :param str region: region.
        :param str queue_name: AWS SQS queue name.
    '''
    def __init__(self, aws_access_key_id, aws_secret_access_key, region,
            queue_name):
        super(AwsSQSTools, self).__init__(aws_access_key_id,
                aws_secret_access_key,
                region=[i for i in regions() if i.name == region][0])
        self.queue = self.create_queue(queue_name)

    def get_all_queues(self, *args, **kwargs):
        ''' Get all queue

            :rtype: list
            :returns: A list of :class:`boto.sqs.queue.Queue` instances.
        '''
        return super(AwsSQSTools, self).get_all_queues(*args, **kwargs)

    def write(self, body):
        ''' Write a message into queue

            :param str body: message body
            :rtype: :class:`boto.sqs.message.Message`
            :returns: :class:`boto.sqs.message.Message`
        '''

        return self.queue.write(self.queue.new_message(body))

    def write_batch(self, body_list):
        ''' Write huge messages will be split 10 messages
            in each single request.

            :param list body_list: a list of message raw data.
            :rtype: list
            :returns: :class:`boto.sqs.batchresults.BatchResults` in list

            .. todo:: default args.
        '''
        result = []
        for loops in xrange(len(body_list) / 10 + 1):
            batch = []
            for no_msg, body in enumerate(body_list[10*loops:10*(loops+1)]):
                batch.append((no_msg, b64encode(body), 0))

            result.append(self.queue.write_batch(batch))

        return result

    def get_messages(self, num_messages=10, *args, **kwargs):
        ''' Get messages from queue

            :param int num_messages: get message in one time.
            :rtype: list
            :returns: A list of :class:`boto.sqs.message.Message` instances

            .. todo::
               - Need to increase `get_messages` concurrency.
               - Maybe auto convert json object.

        '''
        for msg in self.queue.get_messages(num_messages, *args, **kwargs):
            yield msg

if __name__ == '__main__':
    print 'remove comment before use'
    #import json
    #import setting
    #from datetime import datetime

    #SQS = AwsSQSTools(setting.ID, setting.KEY, setting.REGION, 'test_toomore')
    #print SQS.queue
    #print SQS.get_all_queues('test_')
    #print dir(SQS.queue)
    #print [SQS.write(str(i)) for i in xrange(10)]

    # ----- test write / write_batch ----- #
    #print SQS.queue.clear()
    #t1 = datetime.now()
    #print [SQS.write(json.dumps(i)) for i in [dict(name=u'國'),]*23]
    #t2 = datetime.now()
    #print SQS.write_batch([json.dumps(i) for i in [dict(name=u'國'),]*23])
    #t3 = datetime.now()
    #print t2 - t1, t3 - t2

    # ----- test get_messages ----- #
    #t1 = datetime.now()
    #print list(SQS.get_messages())
    #t2 = datetime.now()
    #print list(SQS.get_messages())
    #t3 = datetime.now()
    #print t2 - t1, t3 - t2
