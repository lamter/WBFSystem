# -*- coding: utf-8 -*-

"""
Created on 2015-04-21

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import (render, session)
from base_handler import *
from logout_handler import Logout
from static_handler import JavaScripteHandler
from sim_terminal_handler import SimTerminalPage
from ..models.views import Views
from ..models.usergroup import UserGroup


class Test(BaseHandler):

    URL = BaseHandler.URL + '/test'
    url = BaseHandler.url + r'/test.*'


    def GET(self):
        """
        :return:
        """
        # user = session().user
        import time
        time.sleep(5)
        # views = Views(user)

        # views.render_test(StaticCSSHandler)

        # return views.test
        return '等了 5 秒'