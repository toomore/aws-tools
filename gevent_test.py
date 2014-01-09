# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

import urllib2
from datetime import datetime

pool = Pool(5)

def fetch_data(url):
    print datetime.now(), 'Start', url
    result = urllib2.urlopen(url)
    print datetime.now(), 'Fetch OK', url
    print url, result
    return result.info()

url = [
        'http://www.google.com.tw/',
        'http://www.yahoo.com/',
        'http://toomore.net/',
        'http://pinkoi.toomore.net/',
      ]

gevent_spawn_list = []

for i in url:
    gevent_spawn_list.append(pool.spawn(fetch_data, i))

gevent.joinall(gevent_spawn_list)

for i in gevent_spawn_list:
    print i.get()
