# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn



This module contains the main handler of the application.
"""

import traceback

import web

from skeleton.www.app import session
from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User
from skeleton.www.app.models.usergroup import UserGroup
from base_handler import *
from main_handler import Main


class ManageUser(BaseHandler):

    URL = Main.URL + u'/manage_user'
    url = r'%s/manage_user.*' % Main.URL

    def GET(self):
        try:
            if not settings.DEBUG and not session.login:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manage_user_option()

            ''' 渲染用户列表 '''
            views.render_manage_user()

            ''' 用户管理选择 '''
            return views.manage_user

        except:
            return self.errInfo()




class CreateUserGroup(BaseHandler):

    URL = ManageUser.URL + u'/create_user_group'
    url = r'%s/create_user_group.*' % ManageUser.URL

    ugname = u'ugname'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(app.session.username)
            views = Views(user)

            ugname = web.input().get(self.ugname)

            ''' 渲染管理用户选项 '''
            views.render_manage_user_option()

            ''' 渲染用户列表 '''
            views.render_manage_user()

            ''' 用户管理选择 '''
            return views.manage_user

        except:
            return self.errInfo()