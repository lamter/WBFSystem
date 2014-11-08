# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import server.www
from base_handler import *
from manage_handler import (ManageUser)
from server.www.app.models.views import Views
from server.www.app.models.user import User
from server.www.app.models.usergroup import UserGroup


class Main(BaseHandler):

    URL = u'/main'
    url = r'/main'

    def GET(self):
        try:
            user = User.obj(server.www.session.username)
            if not user:
                return render.login(u'登录超时，请重新登录')

            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manage_user_option(ManageUser)

            ''' 用户管理选择 '''
            return render.main(user, UserGroup, views, ManageUser)

        except:
            return self.errInfo()


