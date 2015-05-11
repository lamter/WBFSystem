# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""
from datetime import *
import gevent as g

import web

from . import (render, session)
from .. import settings
from base_handler import BaseHandler
from ..models.views import Views
from ..models.user import User
from ..models.usergroup import UserGroup


class TestLongWait(BaseHandler):

    URL = BaseHandler.URL + '/test_long_wait'
    url = BaseHandler.url + r'/test_long_wait.*'

    def GET(self):

        b = datetime.now()

        g.sleep(5)

        e = datetime.now()

        return '%s to %s' % (b, e)

