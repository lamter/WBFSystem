# -*- coding: utf-8 -*-
"""
Created on 2015-07-23

@author: Shawn

"""

import web
from gevent.pool import Pool

from app import settings
import loop

from app.models.task import BaseTask

''' 生成并发池 '''
pool = Pool(settings.ASYNC)



def get():
    '''
    :return:
    '''

    ''' 添加一个测试任务 '''
    task = BaseTask()
    pool.start(task)

    ''' 主业务循环 '''
    pool.spawn(loop.loop)

    web.ctx.pool = pool
    return pool