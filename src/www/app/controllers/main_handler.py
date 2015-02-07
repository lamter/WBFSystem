# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

from . import session
from base_handler import *
from login_handler import Login
from manage_handler import (ManageUser)
from ..models.views import Views
from ..models.user import User
from ..models.usergroup import UserGroup


class Main(BaseHandler):

    URL = BaseHandler.URL + '/main'
    url = BaseHandler.url + r'/main'

    def GET(self):
        try:
            user = User.obj(username=session().username)
            if not user:
                return render.login('登录超时，请重新登录', Login)

            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manage_user_option(ManageUser)

            ''' 用户管理选择 '''
            return render.main(user, UserGroup, views, ManageUser)

        except:
            return self.errInfo()


