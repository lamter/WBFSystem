#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2014-10-28

@author: Shawn

The only file which is directly executed. There's no reason to modify this
file.

"""

import web
import src.www
import settings
# import app.models as models
# # from skeleton.www.app.tools.web_session import Session
from app.tools.web_session import Initializer
# import skeleton.www.app as app
from app import (models, controllers)
from urls import (URLS, HANDLER)
from app.tools.app_processor import (header_html, notfound, internalerror)

''' 初始化orm '''
models.init()

web.config.debug = settings.DEBUG

application = web.application(URLS, HANDLER, autoreload=False)
application.notfound = notfound
application.internalerror = internalerror
application.add_processor(web.loadhook(header_html))

src.www.session = web.session.Session(application, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                      User=models.user.User,
                                                                                                      UserGroup=models.usergroup.UserGroup,
                                                                                                      BanLogin=controllers.login_handler.BanLogin,
                                                                                                      ))

web.config.session_parameters['cookie_name'] = 'webpy_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 10
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
web.config.session_parameters['expired_message'] = 'Session expired'


if __name__ == '__main__':
  application.run()
