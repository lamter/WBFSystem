# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

"""


import traceback

import web

import app
from . import render
from base_handler import BaseHandler
from main_handler import Main
from index_handler import Index
from ..models.user import User
from ..models.usergroup import UserGroup


class Login(BaseHandler):

    URL = BaseHandler.URL + '/login'
    url = BaseHandler.url + r'/login.*'

    def POST(self):

        username = web.input().get("username")
        password = str(web.input().get("password"))
        if not username:
            errInfo = '请输入账号!!'
            return render.login(errInfo, Login)
        user = User.obj(username=username)

        if user is None:
            errInfo = '未注册的账号!!'
            return render.login(errInfo, Login)

        elif not user.isPW(password):
            ''' 密码错误 '''
            errInfo = '密码错误!!'
            return render.login(errInfo, Login)

        elif user.isPW(password):
            ''' 通过验证 '''
            app.session.username = '%s' % username
            app.session.login = True
            return web.redirect(Main.URL)

        else:
            errInfo = ''
            return render.login(errInfo, Login)

        return render.login('', Login)


class BanLogin(BaseHandler):
    '''
    禁止登录
    '''
    URL = BaseHandler.URL + '/ban_login'
    url = BaseHandler.url + r'/ban_login'

    def GET(self):
        if app.session.user.isHavePms(UserGroup.PERMISSION_BAN_LOGIN):
            ''' 没有登录权限 '''
            app.session.kill()
            return render.ban_login()
        else:
            ''' 不是被禁止登录，跳转回/index '''
            web.redirect(Index.URL)