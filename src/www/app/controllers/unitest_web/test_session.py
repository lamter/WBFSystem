#coding=utf-8
'''
Created on 2015-01-13

@author: Shawn
'''

import unittest
import traceback

import web
import redis
import redisco

from src.www import app
from src.www.app.tools.web_session import Initializer
from src.www.app import (models, controllers, settings)
from src.www.app.urls import (URLS, HANDLER)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror)
from src.www.app.models.user import User
from src.www.app.models import user
from src.www.app.models.usergroup import UserGroup
from src.www.app.controllers.login_handler import Login

def suite():
    testSuite1 = unittest.makeSuite(TestAppSession, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase



class TestAppSession(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        :return:
        '''

        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        settings.REDIS_PORT = 8911
        settings.REDIS_DB = 0

        ''' redisco连接 '''
        settings.rd = redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


        ''' 启动服务 '''
        web.config.debug = settings.DEBUG

        self.appM = web.application(URLS, HANDLER, autoreload=False)
        application = self.appM.wsgifunc()

        self.appM.notfound = notfound
        self.appM.internalerror = internalerror
        self.appM.add_processor(web.loadhook(header_html))

        controllers.session.init(web.session.Session(self.appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                              User=models.user.User,
                                                                                                              UserGroup=models.usergroup.UserGroup,
                                                                                                              BanLogin=controllers.login_handler.BanLogin,
                                                                                                              settings=settings,
                                                                                                              app=app,
                                                                                                              )))


        web.config.session_parameters['cookie_name'] = 'webpy_session_id'
        web.config.session_parameters['cookie_domain'] = None
        web.config.session_parameters['timeout'] = 10
        web.config.session_parameters['ignore_expiry'] = True
        web.config.session_parameters['ignore_change_ip'] = False
        web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
        web.config.session_parameters['expired_message'] = 'Session expired'

        ''' 初始化orm，包括初始化 root 用户 '''
        app.models.init()


    def test_session(self):
        """
        测试是否生成session实例
        :return:
        """
        user = User.obj(username='root')
        print user
        controllers.session.user = user
        print controllers.session.user