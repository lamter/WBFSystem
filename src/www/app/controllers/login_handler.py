# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

"""


import traceback

import web

from . import session
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
            errInfo = '账号密码不匹配!!!'
            return render.login(errInfo, Login)

        elif not user.isPW(password):
            ''' 密码错误 '''
            errInfo = '账号密码不匹配!!'
            return render.login(errInfo, Login)

        elif user.isPW(password):
            ''' 通过验证 '''
            session().username = '%s' % username
            session().login = True
            session().user = user
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
        if session().user.isHavePms(UserGroup.PERMISSION_BAN_LOGIN):
            ''' 没有登录权限 '''
            session().kill()
            return render.ban_login()
        else:
            ''' 不是被禁止登录，跳转回/index '''
            web.redirect(Index.URL)
