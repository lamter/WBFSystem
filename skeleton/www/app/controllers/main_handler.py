# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.
"""

import traceback

import web

from skeleton.www.settings import session
from base_handler import *
from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User



class MainMenu(BaseHandler):

    URL = u'/main_menu'
    url = r'/main_menu'

    def GET(self):
        try:
            if session.loggedin == False:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 用户管理选择 '''
            return render.main_menu(user, views)

        except:
            return self.errInfo(traceback.format_exc())



class UserList(BaseHandler):

    URL = MainMenu.URL + u'/user_list'
    url = r'%s/user_list' % MainMenu.URL

    def GET(self):
        try:
            if session.loggedin == False:
                return render.login(u'登录超时，请重新登录')

            user = sd.getUserByUsername(session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 渲染用户列表 '''
            views.render_user_list()

            ''' 用户管理选择 '''
            return render.user_list(user, sd, views)

        except:
            return self.errInfo(traceback.format_exc())
