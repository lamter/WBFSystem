# -*- coding: utf-8 -*-
"""
Created on 2015-04-21

@author: Shawn

This module contains the main handler of the application.
"""

import datetime
import traceback
import gevent as g

import web


from . import (render, session)
from .. import settings
from base_handler import BaseHandler
from ..models.views import Views
from ..models.user import User
from ..models.usergroup import UserGroup
from base_handler import *
from logout_handler import Logout
from static_handler import StaticCSSHandler


class TestLongWait(BaseHandler):

    URL = BaseHandler.URL + '/test_long_wait'
    url = BaseHandler.url + r'/test_long_wait.*'

    def GET(self):

        b = datetime.now()

        g.sleep(5)

        e = datetime.now()

        return '%s to %s' % (b, e)


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