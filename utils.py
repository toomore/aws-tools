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
ORGANIZER;CN=Meetup Reminder:MAILTO:%(admin_mail)s
CLASS:PUBLIC
CREATED:%(created)s
LOCATION:%(location)s
URL:http://www.meetup.com/Taipei-py/events/219688456/
LAST-MODIFIED:%(created)s
UID:%(admin_mail)s
END:VEVENT
END:VCALENDAR
'''
# date format: 20150108T073253Z
# DTSTART: 20150113T190000
# DTEND: 20150113T220000
# GEO:25.02;121.44

def dateisoformat(date=None):
    if not date:
        date = datetime.utcnow() + timedelta(hours=8)

    return date.strftime('%Y%m%dT%H%M%SZ')

if __name__ == '__main__':
    print dateisoformat()
