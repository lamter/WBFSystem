# -*- coding: utf-8 -*-

"""
Created on 2015-03-29

@author: Shawn

"""

import os
import traceback

import web

from . import session
from . import render
from base_handler import BaseHandler
from static_handler import BaseStaticHandler
from ..models.user import User
from ..models.usergroup import UserGroup


class BasePublicHandler(BaseStaticHandler):
    """
    公共文件文件下发
    """
    URL = BaseHandler.URL + '/public'
    url = BaseHandler.url + r'/public.*'


    def __init__(self):

        ''' 文件路径 '''
        self.folder = self._wwwPath() + '/www/public'

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
                ''' 后缀名检查 '''
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





class PublicJavaScripteHandler(BasePublicHandler):
    """
    js 脚本的发送句柄
    """
    URL = BasePublicHandler.URL + '/js'
    url = BasePublicHandler.url + '/js.*'
    def __init__(self):

        self.folder = self._wwwPath() + '/www/public/js'

        self.suffix = '.js'

        self.files = self._getTextFiles()
