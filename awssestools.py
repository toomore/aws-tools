# -*- coding: utf-8 -*-
''' My AWS Tools '''
from boto.ses.connection import SESConnection
from email.header import Header
from email.mime.text import MIMEText


class AwsSESTools(SESConnection):
    ''' AWS SES tools

        :param str aws_access_key_id: aws_access_key_id
        :param str aws_secret_access_key: aws_secret_access_key

        .. todo::
           - Add integrated with jinja2 template.

    '''
    def __init__(self, aws_access_key_id, aws_secret_access_key):
        ''' Make a connect '''
        super(AwsSESTools, self).__init__(aws_access_key_id,
                                          aws_secret_access_key)

    @staticmethod
    def mail_header(name, mail):
        ''' Encode header to base64

            :param str name: user name
            :param str mail: user mail
            :rtype: string
            :returns: a string of "name <mail>" in base64.
        '''
        return '"%s" <%s>' % (Header(name, 'utf-8'), mail)

    def send_email(self, *args, **kwargs):
        ''' Send email

            seealso `send_email` in :class:`boto.ses.connection.SESConnection`
        '''
        return super(AwsSESTools, self).send_email(*args, **kwargs)

    def send_raw_email(self, **kwargs):
        msg = MIMEText("""123國<br><a href="http://toomore.net/">link</a>""", 'html', 'utf-8')
        msg['Subject'] = kwargs['subject']
        msg['From'] = kwargs['source']
        msg['To'] = kwargs['to_addresses']

        return super(AwsSESTools, self).send_raw_email(msg.as_string(), kwargs['source'])

if __name__ == '__main__':
    print 'remove comment before use'
    import setting
    from datetime import datetime
    #print AwsSESTools(setting.ID, setting.KEY).send_email(
    #        source=AwsSESTools.mail_header(u'蔣偉志', 'me@toomore.net'),
    #        to_addresses=AwsSESTools.mail_header(u'蔣太多',
    #                'toomore0929@gmail.com'),
    #        subject=u'測試寄件者中文問題',
    #        body=u'測試寄件者中文問題',
    #        format='html')
    print AwsSESTools(setting.ID, setting.KEY).send_raw_email(
            source=AwsSESTools.mail_header(u'蔣偉志', 'me@toomore.net'),
            to_addresses=AwsSESTools.mail_header(u'蔣太多',
                    'toomore0929@gmail.com'),
            subject=u'測試寄件者中文問題 %s' % datetime.now(),
            body=u'測試寄件者中文問題',
            format='html')
