# coding:utf-8
"""
Created on 2015/9/10

描述

@author: Cordial
"""

import web

from . import (render, session)
from base_handler import BaseHandler
from ..models.views import Views
import random
import json

class RefreshLog(BaseHandler):
    """
    log刷新
    """
    URL = BaseHandler.URL + '/refresh_log'
    url = BaseHandler.url + r'/refresh_log.*'

    def GET(self):

        return json.dumps({'log': ['log--->%s' % random.randint(10, 1000), 'log--->%s' % random.randint(10, 1000)]})


class ShowLog(BaseHandler):
    """
    显示log
    """
    URL = BaseHandler.URL + '/show_log'
    url = BaseHandler.url + r'/show_log.*'

    def GET(self):

        user = session().user

        views = Views(user)

        ''' 渲染管理用户选项 '''
        views.render_refresh_log(RefreshLog)

        return views.log_show

