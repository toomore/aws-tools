geventtools
==============================

geventtools
-----------------------------

.. automodule:: geventtools
   :members:


How to use
-----------------------------

.. code-block:: python
   :linenos:

   import urllib2
   from datetime import datetime

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
