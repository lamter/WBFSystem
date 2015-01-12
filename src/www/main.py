#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2014-10-28

@author: Shawn

The only file which is directly executed. There's no reason to modify this
file.

"""

import sys

from src.www.app import settings


reload(sys)
sys.setdefaultencoding('utf-8')

import web
import app
from app.controllers import session
from app.tools.web_session import Initializer
from app.urls import (URLS, HANDLER)
from app.tools.app_processor import (notfound, internalerror, befor_handler)

web.config.debug = settings.DEBUG

appM = web.application(URLS, HANDLER, autoreload=False)
application = appM.wsgifunc()
appM.notfound = notfound
appM.internalerror = internalerror
''' 验证 session '''
appM.add_processor(web.loadhook(befor_handler))

''' 会话数据结构 '''
session.init(web.session.Session(appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                  User=app.models.user.User,
                                                                                                  UserGroup=app.models.usergroup.UserGroup,
                                                                                                  BanLogin=app.controllers.login_handler.BanLogin,
                                                                                                  settings=settings,
                                                                                                  session=session,
                                                                                                  )
                                )
            )

web.config.session_parameters['cookie_name'] = 'webpy_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 10
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
web.config.session_parameters['expired_message'] = 'Session expired'

''' 初始化orm '''
app.models.init()


if __name__ == '__main__':
  appM.run()
