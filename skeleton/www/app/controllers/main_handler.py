# -*- coding: utf-8 -*-

"""This module contains the main handler of the application.
"""

import web
from settings import session
from . import render


class IndexHandler(object):
  """Homepage of the app.
  """
  def GET(self):
    """Returns the homepage (`index.html`) of the app.
    """
    # try:
    #     if session.loggedin:
    #         user = serverdata.globa.getUserByUsername(session.username)
    #         return main_menu_render(user, serverdata.globa)
    # except:
    #     return render.login('')

    return render.login(u'登录请输入密码')


class LoginHandler(object):
    def POST(self):
        username = web.input().get("username")
        password = str(web.input().get("password"))

        if not username:
            errInfo = u'请输入账号!!'
            return render.login(errInfo)

        # user = serverdata.globa.getUserByUsername(username)

        if user is None:
            errInfo = u'未注册的账号!!'
            return render.login(errInfo)

        elif user.password != password:
            ''' 密码错误 '''
            errInfo = u'密码错误!!'
            return render.login(errInfo)
        #
        # elif user.password == password:
        #     ''' 通过验证 '''
        #     session.loggedin = True
        #     session.username = username
        #     return main_menu_render(user, serverdata.globa)

        else:
            errInfo = u''
            return render.login(errInfo)

