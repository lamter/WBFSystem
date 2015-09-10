# -*- coding: utf-8 -*-
"""
Created on 2014-10-28

@author: Shawn

The only file which is directly executed. There's no reason to modify this
file.

"""

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

from gevent import monkey
monkey.patch_all()

from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import web

from app import settings
if settings.isMac():
    import conf_debug
import log
import pool
import app
from app.controllers import session

from app.tools.web_session import Initializer
from app.urls import (URLS, HANDLER)
from app.tools.app_processor import (header_html, notfound, internalerror, verify_session)

web.config.debug = settings.DEBUG

appM = web.application(URLS, HANDLER, autoreload=False)

application = appM.wsgifunc()

''' 日志 '''
log = log.new(application)

appM.notfound = notfound
appM.internalerror = internalerror

''' 会话数据结构, 将初始化 session 插入到 app 的 processor 的流程中 '''
session.init(web.session.Session(appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                  User=app.models.user.User,
                                                                                                  UserGroup=app.models.usergroup.UserGroup,
                                                                                                  BanLogin=app.controllers.login_handler.BanLogin,
                                                                                                  settings=settings,
                                                                                                  session=session,
                                                                                                  )
                                )
            )

''' 校验session, 添加到app的 processor 流程中，顺序需要在 session初始化之后 '''
appM.add_processor(web.loadhook(verify_session))
''' 初始化 html 头, 添加到app的 processor 流程中 '''
appM.add_processor(web.loadhook(header_html))

''' 设置session的参数 '''
settings.setSessionParameters(web.config.session_parameters)

''' 初始化orm，包括初始化 root 用户 '''
app.models.init()


''' 生成并发池 '''
thePool = pool.get()


if __name__ == '__main__':
    # appM.run()
    # 测试提交

    # 监听协议为 http,
    # WSGIServer(('', settings.WEB_LISTEN_PORT), application, spawn=pool).serve_forever()

    # 监听协议为 socket, 用于nginx 转发
    WSGIServer(("", settings.WEB_LISTEN_PORT), application, spawn=thePool, log=log, handler_class=WebSocketHandler).serve_forever()