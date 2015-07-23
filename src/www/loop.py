# -*- coding: utf-8 -*-
"""
Created on 2015-07-23

@author: Shawn

"""

from gevent import sleep
from gevent.queue import Queue

def loop(*arg, **kwargs):
    """
    主业务循环
    :return:
    """
    while True:
        doBusiness()
        ''' yield 出去 '''
        sleep(0)



def doBusiness():
    """
    执行业务,处理业务的时候阻塞
    :return:
    """

    for _ in xrange(queue.qsize()):
        task = queue.get_nowait()
        ''' task 可以为函数, 也可以为一个实例,作为实例的时候, 执行函数需要写在 __call__ 中 '''
        task()


queue = Queue()