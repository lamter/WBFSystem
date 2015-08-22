# -*- coding: utf-8 -*-
"""
Created on 2015-08-21

@author: Shawn

"""

import gevent
from gevent import Timeout
from gevent.greenlet import Greenlet as gl
from gevent.event import Event
from gevent.pool import Pool


''' 超时时间 '''
TIME_TO_WAIT = 30   # second


''' 超时 '''
class TooLong(Exception):
    pass



class Greenlet(gl):
    """
    重写并发 Greentlet
    """
    def __init__(self, run=None, *args, **kwargs):
        gl.__init__(self, run, *args, **kwargs)

        self.event = Event()


    def waitFinish(self, second=TIME_TO_WAIT):
        """
        等待这个并发完成
        :return:
        """
        self.event.wait(second)


    def run(self):
        """
        :return:
        """
        with Timeout(TIME_TO_WAIT, TooLong):
            gevent.Greenlet.run(self)

        ''' 完成事件 '''
        self.event.set()



if __name__ == "__main__":
    pool = Pool(10, greenlet_class=Greenlet)
    def fun():
        print 'fun'
        gevent.sleep(6)
        print 1212121
    glFun = pool.spawn(fun)
    print 'glFun.ready() ->', glFun.ready()

    def bar():
        print 'bar'
        print 'glFun.started->', glFun.started
        glFun.waitFinish()
        print 13131313

    glBar = pool.spawn(bar)
    print 'glBar->', glBar.ready()
    pool.join()

    print 'glFun ->', glFun.ready()
    print 'glFun.exception->', glFun.exception

    print 'glBar->', glBar.ready()
    print 'glBar.exception->', glBar.exception

