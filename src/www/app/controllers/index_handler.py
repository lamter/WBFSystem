# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import (render, session)
from base_handler import BaseHandler
from main_handler import Main
import login_handler


class Index(BaseHandler):
    """
    主页
    """
    URL = BaseHandler.URL + ''
    url = BaseHandler.url + r'/'

    def GET(self):

        if session().login:
            return web.redirect(Main.URL)
        else:
            return render.login('未登录', login_handler.Login)

