#coding=utf-8
'''
Created on 2015-02-05

@author: Shawn
'''

import unittest
import os

import web
import redis
import redisco

from src.www.app.controllers import session
from src.www.app.tools.web_session import Initializer
from src.www.app import (models, controllers, settings)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror, verify_session)
from src.www.app.urls import (URLS, HANDLER)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror)
from src.www.app.models.user import User
from src.www.app.models.usergroup import UserGroup
from src.www.app.models.views import Views
from src.www.app.models.term_server import TerminalServer
from src.www.app.controllers.manage_handler import (ManageUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)
from src.www.app.controllers.login_handler import Login
from src.www.app.controllers.sim_terminal_handler import (SimTermLocalServer)
from src.www.app.controllers.static_handler import (StaticJavaScripteHandler, StaticCSSHandler)
from src.www.app.controllers.test_handler import Test

def suite():
    testSuite1 = unittest.makeSuite(TestStatic, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestStatic(unittest.TestCase):
    '''
    测试伪终端
    '''
    def setUp(self):
        '''
        :return:
        '''
        settings.IS_UNITTEST = True
        settings.DEBUG = True
        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        # settings.REDIS_PORT = 8911
        # settings.REDIS_DB = 0

        ''' redisco连接 '''
        settings.rd = redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        # ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 启动服务 '''
        web.config.debug = settings.DEBUG

        self.appM = web.application(URLS, HANDLER, autoreload=False)
        application = self.appM.wsgifunc()

        self.appM.notfound = notfound
        self.appM.internalerror = internalerror
        self.appM.add_processor(web.loadhook(header_html))

        session.init(web.session.Session(self.appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                              User=models.user.User,
                                                                                                              UserGroup=models.usergroup.UserGroup,
                                                                                                              BanLogin=controllers.login_handler.BanLogin,
                                                                                                              settings=settings,
                                                                                                              session=session,
                                                                                                              ))
        )

        ''' 校验session, 添加到app的 processor 流程中，顺序需要在 session初始化之后 '''
        self.appM.add_processor(web.loadhook(verify_session))
        ''' 初始化 html 头, 添加到app的 processor 流程中 '''
        self.appM.add_processor(web.loadhook(header_html))

        web.config.session_parameters['cookie_name'] = 'webpy_session_id'
        web.config.session_parameters['cookie_domain'] = None
        web.config.session_parameters['timeout'] = 10
        web.config.session_parameters['ignore_expiry'] = True
        web.config.session_parameters['ignore_change_ip'] = False
        web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
        web.config.session_parameters['expired_message'] = 'Session expired'


    def test_JavaHandler(self):
        """

        :return:
        """
        user = User.obj(username=User.rootAccount)
        settings.debug_user = user
        v = Views(user)
        v.html(self.appM.request(localpart=StaticJavaScripteHandler.load("jquery.min.js"), method='GET').data)


    def test_css(self):
        """
        :return:
        """
        user = User.obj(username=User.rootAccount)
        settings.debug_user = user
        v = Views(user)
        print 1212, StaticCSSHandler.load("button.css")
        v.html(self.appM.request(localpart=StaticCSSHandler.load("button.css"), method='GET').data)


    def test_test(self):
        """

        :return:
        """

        user = User.obj(username=User.rootAccount)
        settings.debug_user = user
        v = Views(user)

        v.html(self.appM.request(localpart=Test.URL, method='GET').data)