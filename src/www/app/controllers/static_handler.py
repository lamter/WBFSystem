# -*- coding: utf-8 -*-

"""
Created on 2015-03-19

@author: Shawn

"""

import os
import traceback

import web

from . import session
from . import render
from base_handler import BaseHandler
from ..models.user import User
from ..models.usergroup import UserGroup


class BaseStaticHandler(BaseHandler):
    """
    静态文件下发
    """
    URL = BaseHandler.URL + '/static'
    url = BaseHandler.url + r'/static.*'



    def __init__(self):

        ''' 文件路径 '''
        self.folder = self.__wwwPath() + '/www/static'

        self.suffix = ''

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


    @staticmethod
    def _wwwPath():
        """
        """

        return os.getcwd().split("/www/app")[0]


    def GET(self):
        filneName = web.ctx.path.split('/')[-1]
        return self.getText(filneName)


    def getText(self, fileName):
        return self.files.get(fileName)





class JavaScripteHandler(BaseStaticHandler):
    """
    js 脚本的发送句柄
    """
    URL = BaseStaticHandler.URL + '/js'
    url = BaseStaticHandler.url + '/js.*'
    def __init__(self):

        self.folder = self._wwwPath() + '/www/static/js'

        self.suffix = '.js'

        self.files = self._getTextFiles()
