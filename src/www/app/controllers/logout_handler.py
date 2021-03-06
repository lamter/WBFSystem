# -*- coding: utf-8 -*-

"""
Created on 2015-02-28

@author: Shawn

"""


import traceback

import web

from . import session
from base_handler import BaseHandler


class Logout(BaseHandler):

    URL = '/logout'
    url = r'/logout'

    def GET(self):
        """
        :return:
        """

        ''' 清除这一次会话session '''
        session().kill()
        jumpto = BaseHandler.URL
        if not jumpto:
            jumpto += '/'
        else:
            if jumpto[-1] != '/':
                jumpto += '/'
        return web.seeother(jumpto)