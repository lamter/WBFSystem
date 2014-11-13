# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.

@author: Shawn

"""

__author__ = 'Shawn'

import traceback

import src.www.settings as settings
from src.www.app.controllers import render


class BaseHandler(object):
    URL = u"/"
    url = r'^/'

    def errInfo(self):
        '''
        将Traceback的错误组织好后返回
        :return:
        '''
        errStr = traceback.format_exc()
        if settings.DEBUG:
            traceback.print_exc()
        errStr = errStr.replace('\n', "<br/>")
        return render.traceback(errStr)
