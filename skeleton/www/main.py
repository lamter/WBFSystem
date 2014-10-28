#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The only file which is directly executed. There's no reason to modify this
file.
"""

import getopt
import web
import settings
from urls import (URLS, HANDLER)
from app.tools.app_processor import (header_html, notfound, internalerror)

web.config.debug = settings.DEBUG

app = web.application(URLS, HANDLER, autoreload=False)
app.notfound = notfound
app.internalerror = internalerror
app.add_processor(web.loadhook(header_html))


settings.session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})
web.config.session_parameters['cookie_name'] = 'webpy_session_id'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 10
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
web.config.session_parameters['expired_message'] = 'Session expired'


if __name__ == '__main__':
  app.run()
