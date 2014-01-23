# -*- coding: utf-8 -*-
''' AwsSQSTools '''
import setting
from base64 import b64encode
from boto.sqs import connect_to_region


class AwsSQSTools(object):
    ''' AwsSQSTools

        :param str queue_name: AWS SQS queue name.
    '''
    def __init__(self, queue_name):
        self.conn = connect_to_region(setting.REGION,
                                      aws_access_key_id=setting.ID,
                                      aws_secret_access_key=setting.KEY)
        self.queue = self.conn.create_queue(queue_name)

    def get_all_queues(self, *args, **kwargs):
        ''' Get all queue '''
        return self.conn.get_all_queues(*args, **kwargs)

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
        for loops in xrange(len(body_list) / 10):
            returns = self.queue.write_batch([(i, b64encode(body), 0) for i, body in enumerate(body_list[10*loops:10*(loops+1)])])
            result.append(returns)

        return result

    def get_messages(self, num_messages=10, *args, **kwargs):
        ''' Get messages from queue

            :param int num_messages: get message in one time.
            :rtype: list
            :returns: a list of message body.

            .. todo:: Need to increase `get_messages` concurrency.

        '''
        for i in self.queue.get_messages(num_messages, *args, **kwargs):
            yield i.get_body()

if __name__ == '__main__':
    import json
    from datetime import datetime

    SQS = AwsSQSTools('test_toomore')
    #print SQS.queue
    #print SQS.get_all_queues('test_')
    #print dir(SQS.queue)
    #print [SQS.write(str(i)) for i in xrange(10)]

    # ----- test write / write_batch ----- #
    print SQS.queue.clear()
    t1 = datetime.now()
    print [SQS.write(json.dumps(i)) for i in [dict(name=u'國'),]*20]
    t2 = datetime.now()
    print SQS.write_batch([json.dumps(i) for i in [dict(name=u'國'),]*20])
    t3 = datetime.now()
    print t2 - t1, t3 - t2

    # ----- test get_messages ----- #
    t1 = datetime.now()
    print list(SQS.get_messages())
    t2 = datetime.now()
    print list(SQS.get_messages())
    t3 = datetime.now()
    print t2 - t1, t3 - t2
