# -*- coding: utf-8 -*-
"""
Created on 2015-07-27

@author: Shawn

"""
import sys, logging

from wsgilog import WsgiLog, DATEFORMAT, LOGFORMAT

from app import settings

# DATEFORMAT = '%a, %d %b %Y %H:%M:%S'
# LOGFORMAT = '%(name)s: %(asctime)s %(levelname)-4s %(message)s'

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            # logformat = '%(message)s',
            tofile = True,
            toprint = False,
            file = settings.log,
            # interval = 0.1,
            # backups = 1,
            )



def new(application):
    if settings.IS_LOG_TO_FILE:
        log = Log(application)
        return log
    else:
        return 'default'
