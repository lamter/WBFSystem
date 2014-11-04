# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

"""


import traceback

import web

import skeleton.www.app as app
from base_handler import BaseHandler
from index_handler import Index
from main_handler import *
# from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User
from skeleton.www.app.models.usergroup import UserGroup


class Login(BaseHandler):

    URL = u'/login'
    url = r'/login'

    def POST(self):

        username = web.input().get("username")
        password = str(web.input().get("password"))

        if not username:
            errInfo = u'请输入账号!!'
            return render.login(errInfo)

        user = User.obj(username)

        if user is None:
            errInfo = u'未注册的账号!!'
            return render.login(errInfo)

        elif not user.isPW(password):
            ''' 密码错误 '''
            errInfo = u'密码错误!!'
            return render.login(errInfo)

        elif user.isPW(password):
            ''' 通过验证 '''
            app.session.username = u'%s' % username
            app.session.login = True
            return web.redirect(Main.URL)

        else:
            errInfo = u''
            return render.login(errInfo)

        return render.login(u'')


class BanLogin(BaseHandler):
    '''
    禁止登录
    '''
    URL = u'/ban_login'
    url = r'/ban_login'

    def GET(self):
        if app.session.user.isHavePms(UserGroup.PERMISSION_BAN_LOGIN):
            ''' 没有登录权限 '''
            app.session.kill()
            return render.ban_login()
        else:
            ''' 不是被禁止登录，跳转回/index '''
            web.redirect(Index.URL)
