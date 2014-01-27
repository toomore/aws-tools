# -*- coding: utf-8 -*-
import gevent
import urllib2
from datetime import datetime
from gevent.pool import Pool

from gevent import monkey
monkey.patch_all()


def gevent_pool(func, spawn_list, pool_size=5):
    pool = Pool(pool_size)
    gevent_spawn_list = []

    for args, kwargs in spawn_list:
        gevent_spawn_list.append(pool.spawn(func, *args, **kwargs))

    gevent.joinall(gevent_spawn_list)
    return gevent_spawn_list

def midfunc(*args, **kwargs):
    return args, kwargs

if __name__ == '__main__':
    def fetch_data(url):
        print datetime.now(), 'Start', url
        result = urllib2.urlopen(url)
        print datetime.now(), 'Fetch OK', url
        print url, result
        return result.info()

    url = [
            midfunc('http://www.google.com.tw/'),
            midfunc('http://toomore.net/'),
            midfunc('http://pinkoi.toomore.net/'),
            midfunc(url='http://www.pinkoi.com/'),
          ]
    t1 = datetime.now()
    result = gevent_pool(fetch_data, url*20, 20)

    for i in result:
        print i.get()
    print result
    print datetime.now() - t1
