# -*- coding: utf-8 -*-

"""Pre-processors and customizations for the application.
"""

import traceback

import web
from .. import settings
from ..models import User
from ..controllers import (render, session)
from ..controllers.base_handler import BaseHandler
from ..controllers.login_handler import Login
# from ..controllers.main_handler import Main
from ..controllers.index_handler import Index

def header_html():
  """Global header setter for `text/html` documents.
  """
  web.header('Content-Type', 'text/html; charset=UTF-8')


def notfound():
  """Customized 404 Not Found message.
  """
  web.ctx.status = '404 Not Found'
  return web.notfound(str(render._404()))

def internalerror():
    """Customized 500 Internal Server Error message.
    """
    web.ctx.status = '500 Internal Server Error'
    return web.internalerror(str(render._500(BaseHandler.errInfo())))


def befor_handler():
    """
    之前要做的事情
    :return:
    """
    ''' 验证 session '''
    verify_session()

    ''' 设置 http 头 '''
    header_html()


def verify_session():
    """
    每次提交 http 请求都要经过这个 session验证
    :return:
    """
    ''' 这个session还没有初始化过 username 和 login 的属性 '''

    print 'web.ctx.path->', web.ctx.path

    print "hasattr(session(), 'username') ->", hasattr(session(), 'username')
    print "hasattr(session(), 'login')->", hasattr(session(), 'login')
    print "hasattr(session(), 'user')->", hasattr(session(), 'user')

    print 'id(session())->', id(session())

    if not hasattr(session(), 'username') and not hasattr(session(), 'login'):
        if Login.isMatch(web.ctx.path) or Index.isMatch(web.ctx.path):
            print ''' 如果访问的是登录界面, 不需要验证 '''
            return
        else:
            print ''' 需要前往登录页面 '''
            raise web.redirect(Index.URL)

    ''' 验证是否登录 '''
    if not settings.DEBUG and not session().login:
        return render.login('登录超时，请重新登录', Login)

    # session()

    # user = User.obj(username=session().username)
    # if not user:
    #     return render.login('登录超时，请重新登录', Login)
    #
    # # TODO 直接挂在 user  实例的session上面
    #
    # print 111111111111
    # print 'id(session())->', id(session())
    #
    # ''' 将用户实例绑定到 session上 '''
    # setattr(session(), 'user', user)