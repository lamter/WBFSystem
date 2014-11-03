# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.
"""

import traceback

import web

import skeleton.www.app as app
from base_handler import *
from main_handler import *
from skeleton.www.app.models.views import Views


class Index(BaseHandler):
    """
    主页
    """
    URL = u'/'
    url = r'^/'

    def GET(self):
        try:
            print app.session.user
            if app.session.user:
                return web.redirect(Main.URL)

        except AttributeError:

            return render.login(u'登录请输入密码')

