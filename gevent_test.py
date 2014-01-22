# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

import urllib2
from datetime import datetime


def fetch_data(url):
    print datetime.now(), 'Start', url
    result = urllib2.urlopen(url)
    print datetime.now(), 'Fetch OK', url
    print url, result
    return result.info()

def gevent_pool(func, spawn_list, pool_size=5):
    pool = Pool(pool_size)
    gevent_spawn_list = []

    for i in spawn_list:
        gevent_spawn_list.append(pool.spawn(func, *i))

    gevent.joinall(gevent_spawn_list)
    return gevent_spawn_list

if __name__ == '__main__':
    url = [
            ('http://www.google.com.tw/',),
            ('http://www.yahoo.com/',),
            ('http://toomore.net/',),
            ('http://pinkoi.toomore.net/',),
          ]

    result = gevent_pool(fetch_data, url*20, 5)

    for i in result:
        print i.get()
    print result
