# -*- coding: utf-8 -*-
''' My AWS Tools '''
import setting
from boto import ses
from email.header import Header


class AwsSESTools(object):
    ''' AWS SES tools '''
    def __init__(self):
        ''' Make a connect '''
        self.conn = ses.connection.SESConnection(
                                     aws_access_key_id=setting.ID,
                                     aws_secret_access_key=setting.KEY)

    @staticmethod
    def mail_header(name, mail):
        ''' Encode header to base64 '''
        return '"%s" <%s>' % (Header(name, 'utf-8'), mail)

    def send_email(self):
        ''' Send email '''
        return self.conn.send_email(
                source=self.mail_header(u'蔣偉志', 'me@toomore.net'),
                to_addresses=self.mail_header(u'蔣太多', 'toomore0929@gmail.com'),
                subject=u'測試寄件者中文問題',
                body=u'測試寄件者中文問題',
                format='html')

if __name__ == '__main__':
    print 'remove comment before use'
    #print AwsSESTools().send_email()
