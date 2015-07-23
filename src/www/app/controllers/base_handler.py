# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.

@author: Shawn

"""

__author__ = 'Shawn'

import traceback
import os

from web import utils

from .. import settings
from . import render


class BaseHandler(object):
    URL = ""
    url = r''

    @staticmethod
    def errInfo():
        '''
        将Traceback的错误组织好后返回
        :return:
        '''
        errStr = traceback.format_exc()
        if settings.DEBUG:
            traceback.print_exc()
        errStr = errStr.replace('\n', "<br/>")
        return errStr
        # return render.traceback(errStr)


    @classmethod
    def isMatch(cls, url):
        """
        这个 url 的请求是否 由这个 handler 来处理
        :return:
        """
        pat = cls.url
        what = cls.__name__

        if isinstance(what, basestring):
            what, result = utils.re_subm('^' + pat + '$', what, url)
        else:
            result = utils.re_compile('^' + pat + '$').match(url)

        return result


    @staticmethod
    def _wwwPath():
        """
        """

        return os.getcwd().split("/www/app")[0]