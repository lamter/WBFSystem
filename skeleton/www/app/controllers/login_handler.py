# -*- coding: utf-8 -*-

import traceback

import web

global session

from . import render
from base_handler import *
from main_handler import *
from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User


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
        views = Views(user)

        if user is None:
            errInfo = u'未注册的账号!!'
            return render.login(errInfo)

        elif user.password != password:
            ''' 密码错误 '''
            errInfo = u'密码错误!!'
            return render.login(errInfo)

        elif user.password == password:
            ''' 通过验证 '''
            print 'id(session)->', session
            session.loggedin = True
            session.username = username
            return web.redirect(MainMenu.URL)

        else:
            errInfo = u''
            return render.login(errInfo)

