# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.
"""

import traceback

import web

import skeleton.www.app as app
from base_handler import *
from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User
from skeleton.www.app.models.usergroup import UserGroup



class Main(BaseHandler):

    URL = u'/main'
    url = r'/main'

    def GET(self):
        try:
            user = User.obj(app.session.username)
            if not user:
                return render.login(u'登录超时，请重新登录')

            views = Views(user)

            print ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 用户管理选择 '''
            return render.main(user, UserGroup, views)

        except:
            return self.errInfo()



class UserList(BaseHandler):

    URL = Main.URL + u'/user_list'
    url = r'%s/user_list' % Main.URL

    def GET(self):
        try:
            if app.session.loggedin == False:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(app.session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 渲染用户列表 '''
            views.render_user_list()

            ''' 用户管理选择 '''
            return render.user_list(user, sd, views)

        except:
            return self.errInfo()
