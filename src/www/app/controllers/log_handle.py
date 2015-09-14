# -*- coding: utf-8 -*-

"""
Created on 2015-09-11

@author: Shawn


"""

import traceback

import web

from . import (render, session)
from base_handler import BaseHandler


class QueryLogCache(BaseHandler):
    """
    查询日志缓存
    """
    URL = BaseHandler.URL + '/query_log_cache'
    url = BaseHandler.url + r'/query_log_cache'

    def GET(self):

        if session().login:
            return web.redirect(Main.URL)
        else:
            return render.login('未登录', login_handler.Login)


