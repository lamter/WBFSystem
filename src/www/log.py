# -*- coding: utf-8 -*-
"""
Created on 2015-07-27

@author: Shawn

"""
import sys, logging

from wsgilog import WsgiLog

from app import settings

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = '%(message)s',
            tofile = True,
            toprint = False,
            file = settings.log,
            # interval = 0.1,
            # backups = 1,
            )



def new(application):
    if settings.IS_LOG_TO_FILE:
        return Log(application)
    else:
        return 'default'
