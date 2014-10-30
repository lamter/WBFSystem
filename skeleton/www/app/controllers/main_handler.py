# -*- coding: utf-8 -*-

"""
This module contains the main handler of the application.
"""

import traceback

import web
from skeleton.www.settings import session
import base_handler
from . import render


class Index(base_handler.BaseHandler):
    """
    主页
    """
    URL = u'/'
    url = r'^/'

    def GET(self):
        try:
            if session.loggedin:
                return web.redirect(MainMenu.URL)

        except:

            return render.login(u'登录请输入密码')


class Login(base_handler.BaseHandler):
    URL = u'/login'
    url = r'/login'
    def POST(self):

        username = web.input().get("username")
        password = str(web.input().get("password"))

        views = Views()

        if not username:
            errInfo = u'请输入账号!!'
            return pages.login(errInfo)

        user = serverdata.globa.getUserByUsername(username)

        if user is None:
            errInfo = u'未注册的账号!!'
            return pages.login(errInfo)

        elif user.password != password:
            ''' 密码错误 '''
            errInfo = u'密码错误!!'
            return pages.login(errInfo)

        elif user.password == password:
            ''' 通过验证 '''
            session.loggedin = True
            session.username = username
            return web.redirect(MainMenu.URL)

        else:
            errInfo = u''
            return pages.login(errInfo)


class MainMenu(ManagerServerBase):

    URL = u'/main_menu'
    url = r'/main_menu'

    def GET(self):
        try:
            if session.loggedin == False:
                return pages.login(u'登录超时，请重新登录')

            user = sd.getUserByUsername(session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 用户管理选择 '''
            return pages.main_menu(user, sd, views)

        except:
            return self.errInfo(traceback.format_exc())


class UserList(ManagerServerBase):

    URL = MainMenu.URL + u'/user_list'
    url = r'%s/user_list' % MainMenu.URL

    def GET(self):
        try:
            if session.loggedin == False:
                return pages.login(u'登录超时，请重新登录')

            user = sd.getUserByUsername(session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            views.render_manager_user_option()

            ''' 渲染用户列表 '''
            views.render_user_list()

            ''' 用户管理选择 '''
            return pages.user_list(user, sd, views)

        except:
            return self.errInfo(traceback.format_exc())
