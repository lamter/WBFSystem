# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import render
import server.www
import base_handler
import main_handler
from server.www.app.models.views import Views


class Index(base_handler.BaseHandler):
    """
    主页
    """
    URL = u'/'
    url = r'^/'

    def GET(self):
        try:
            # print "app.session.login->", app.session.login
            if server.www.session.login:
                return web.redirect(main_handler.Main.URL)
            else:
                return render.login(u'未登录')

        except AttributeError:
            traceback.print_exc()
            return render.login(u'登录请输入密码')

