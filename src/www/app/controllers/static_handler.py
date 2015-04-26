# -*- coding: utf-8 -*-

"""
Created on 2015-03-19

@author: Shawn

"""

import os
import traceback

import web

from .. import settings
from . import (render, session)
from base_handler import BaseHandler
from ..models.user import User
from ..models.usergroup import UserGroup


class BaseStaticHandler(BaseHandler):
    """
    静态文件下发
    """
    URL = BaseHandler.URL + '/static'
    url = BaseHandler.url + r'/static.*'

    folder = BaseHandler._wwwPath() + '/www/static'

    suffix = ''


    def __init__(self):
        ''' 文件路径 '''
        BaseHandler.__init__(self)

        self.files = self._getTextFiles()



    def _getTextFiles(self):
        """

        """
        def endWith(s,*endstring):
            array = map(s.endswith, endstring)
            if True in array:
                    return True
            else:
                    return False

        dic = {}

        for fileName in os.listdir(self.folder):
            if not endWith(fileName, self.suffix):
                ''' 后缀名见哈 '''
                continue

            with open(os.path.join(self.folder, fileName)) as f:
                dic[fileName] = f.read()
        return dic


    def GET(self):
        filneName = web.ctx.path.split('/')[-1]
        return self.getText(filneName)


    def getText(self, fileName):
        return self.files.get(fileName)


    @classmethod
    def load(cls, file):
        """
        :return
        """
        # if settings.IS_UNITTEST:
        #     return cls.folder + '/' +  file
        return cls.URL + '/' + file


class StaticJavaScripteHandler(BaseStaticHandler):
    """
    js 脚本的发送句柄
    """
    URL = BaseStaticHandler.URL + '/js'
    url = BaseStaticHandler.url + '/js.*'

    folder = BaseStaticHandler._wwwPath() + '/www/static/js'

    suffix = '.js'

    def __init__(self):
        BaseStaticHandler.__init__(self)
        self.files = self._getTextFiles()




class StaticCSSHandler(BaseStaticHandler):
    """
    css 的发送句柄
    """
    URL = BaseStaticHandler.URL + '/css'
    url = BaseStaticHandler.url + '/css.*'

    folder = BaseStaticHandler._wwwPath() + '/www/static/css'

    suffix = '.css'

    def __init__(self):
        BaseStaticHandler.__init__(self)

        self.files = self._getTextFiles()
