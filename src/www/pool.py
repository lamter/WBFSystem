# -*- coding: utf-8 -*-
"""
Created on 2015-07-23

@author: Shawn

"""

import web
from gevent.pool import Pool

from app import settings
import loop









''' 生成并发池 '''
pool = Pool(settings.ASYNC)


def get():
    '''
    :return:
    '''

    ''' 主业务循环 '''
    pool.join(loop.loop)

    web.ctx.pool = pool
    return pool