# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import (render, session)
from base_handler import *
from logout_handler import Logout
from manage_handler import (ManageUser)
from sim_terminal_handler import SimTerminalPage
from ..models.views import Views
from ..models.usergroup import UserGroup
from log_handler import *

class Main(BaseHandler):

    URL = BaseHandler.URL + '/main'
    url = BaseHandler.url + r'/main'

    def GET(self):
        """
        主页面
        :return:
        """

        user = session().user

        views = Views(user)

        ''' 渲染管理用户选项 '''
        views.render_manage_user_option(ManageUser)

        ''' 用户管理选择 '''
        return render.main(user,
                           UserGroup,
                           views,
                           ManageUser,
                           SimTerminalPage,
                           Logout,
                           ShowLog,
        )
