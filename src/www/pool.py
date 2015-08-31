# -*- coding: utf-8 -*-
"""
Created on 2015-07-23

@author: Shawn

"""

import web
# from gevent.pool import Pool

from app import settings
import loop

from app.models.task import BaseTask
from app.tools.mypool import Pool
from app.tools.mygreenlet import Greenlet
from app.tools.shutdown import getShutDown

''' 生成并发池, 不再默认使用 '''
pool = Pool(settings.ASYNC, greenlet_class=Greenlet)


''' 关服操作 '''
getShutDown()


def get():
    '''
    :return:
    '''

    ''' 添加一个测试任务 '''
    task = BaseTask()
    pool.start(task)

    ''' 主业务循环 '''
    glLoop = pool.spawn(loop.loop)
    glLoop.setNoTimeOut()

    web.pool = pool
    return pool