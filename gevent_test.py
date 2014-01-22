# -*- coding: utf-8 -*-
import gevent
from gevent import monkey
from gevent.pool import Pool
monkey.patch_all()

import urllib2
from datetime import datetime


def gevent_pool(func, spawn_list, pool_size=5):
    pool = Pool(pool_size)
    gevent_spawn_list = []

    for args, kwargs in spawn_list:
        gevent_spawn_list.append(pool.spawn(func, *args, **kwargs))

    gevent.joinall(gevent_spawn_list)
    return gevent_spawn_list

if __name__ == '__main__':
    #def fetch_data(*args, **kwargs):
    #    return args, kwargs

    def fetch_data(url):
        print datetime.now(), 'Start', url
        result = urllib2.urlopen(url)
        print datetime.now(), 'Fetch OK', url
        print url, result
        return result.info()

    url = [
            (('http://www.google.com.tw/',), {}),
            (('http://toomore.net/',), {}),
            (('http://pinkoi.toomore.net/',), {}),
            ((), {'url': 'http://www.pinkoi.com/'}),
          ]
    t1 = datetime.now()
    result = gevent_pool(fetch_data, url*20, 20)

    for i in result:
        print i.get()
    print result
    print datetime.now() - t1
