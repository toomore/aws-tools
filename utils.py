# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timedelta


BASEICS = u'''
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Toomore//Toomore Events v1.0//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VTIMEZONE
TZID:Asia/Taipei
BEGIN:STANDARD
TZOFFSETFROM:+0800
TZOFFSETTO:+0800
TZNAME:CST
DTSTART:19700101T000000
END:STANDARD
END:VTIMEZONE
BEGIN:VEVENT
DTSTAMP:%(created)s
DTSTART;TZID=Asia/Taipei:%(start)s
DTEND;TZID=Asia/Taipei:%(end)s
STATUS:CONFIRMED
SUMMARY:%(title)s
DESCRIPTION:%(description)s
ORGANIZER;CN=%(admin)s Reminder:MAILTO:%(admin_mail)s
CLASS:PUBLIC
CREATED:%(created)s
LOCATION:%(location)s
URL:%(url)s
LAST-MODIFIED:%(created)s
UID:%(admin_mail)s
END:VEVENT
END:VCALENDAR
'''
# created, start, end, title, description, location, admin_mail
# date format: 20150108T073253Z
# DTSTART: 20150113T190000
# DTEND: 20150113T220000
# GEO:25.02;121.44

def dateisoformat(date=None, with_z=True):
    if not date:
        date = datetime.utcnow() + timedelta(hours=8)

    if with_z:
        return date.strftime('%Y%m%dT%H%M%SZ')
    return date.strftime('%Y%m%dT%H%M%SZ')[:-1]


def render_ics(title, description, location, start, end, created, admin,
        admin_mail, url):
    data = {
            'title': title,
            'description': description,
            'location': location,
            'start': dateisoformat(start, False),
            'end': dateisoformat(end, False),
            'created': dateisoformat(created),
            'admin': admin,
            'admin_mail': admin_mail,
            'url': url,
            }
    return BASEICS % data

if __name__ == '__main__':
    print dateisoformat()
    print render_ics(
            title=u'吃火鍋',
            description=u'冬天到了要吃火鍋！',
            location=u'台北市中正區衡陽路51號',
            start=datetime(2015, 1, 29, 10),
            end=datetime(2015, 1, 29, 18, 30),
            created=None,
            admin=u'Toomore',
            admin_mail=u'toomore0929@gmail.com',
            url=u'http://toomore.net/'
            )
