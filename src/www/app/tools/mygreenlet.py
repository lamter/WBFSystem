# -*- coding: utf-8 -*-
"""
Created on 2015-08-21

@author: Shawn

"""
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import gevent

from gevent.greenlet import Greenlet as gl
from gevent.event import Event
from gevent.pool import Pool


class Greenlet(gl):
    """
    重写并发 Greentlet
    """
    def __init__(self, run=None, *args, **kwargs):
        gl.__init__(self, run, *args, **kwargs)

        self.event = Event()


    def waitFinish(self):
        """
        等待这个并发完成
        :return:
        """
        self.event.wait()



    def run(self):
        """
        :return:
        """

        gevent.Greenlet.run(self)

        ''' 完成事件 '''
        self.event.set()



if __name__ == "__main__":
    pool = Pool(10, greenlet_class=Greenlet)
    def fun():
        print 'fun'
        gevent.sleep(2)
        print 1212121
    greentlet = pool.spawn(fun)

    def bar():
        print 'bar'
        greentlet.waitFinish()
        print 13131313
    pool.spawn(bar)
    pool.join()


