# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

__author__ = 'Shawn'


from skeleton.www.app.controllers import render



class BaseHandler(object):
    URL = u"/"
    url = r'^/'

    def errInfo(self, errStr):
        '''
        将Traceback的错误组织好后返回
        :return:
        '''
        errStr = errStr.replace('\n', "<br/>")
        return render.traceback(errStr)
