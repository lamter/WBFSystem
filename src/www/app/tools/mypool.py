# -*- coding: utf-8 -*-
"""
Created on 2015-08-28

@author: Shawn

"""

import gevent
from gevent import Timeout
from gevent.greenlet import Greenlet as gl
from gevent.event import Event
from gevent.pool import Pool as PL



class Pool(PL):
    """
    重写并发 Greentlet
    """


    def spawn_later(self, seconds, *args, **kwargs):
        """
        延迟多久后执行
        :param seconds:
        :param args:
        :param kwargs:
        :return:
        """
        greenlet = self.greenlet_class(*args, **kwargs)
        self.start_later(seconds, greenlet)
        return greenlet


    def start_later(self, seconds, greenlet):
        """
        :param seconds:
        :param greenlet:
        :return:
        """

        self.add(greenlet)
        greenlet.start_later(seconds)


if __name__ == "__main__":
    from mygreenlet import Greenlet
    pool = Pool(10, Greenlet)
    def foo():
        print 'foo'
        print 'foo over'

    def bar(fo):
        print 'bar'
        fo.waitFinish()
        print 'bar over'

    wait = 3
    fo = pool.spawn_later(wait, foo)
    ba = pool.spawn_later(wait, bar, fo)
    pool.join()







