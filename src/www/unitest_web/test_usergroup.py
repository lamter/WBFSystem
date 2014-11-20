#coding=utf-8
'''
Created on 2014-10-27

@author: Shawn
'''

import unittest
import traceback

import web
import redis
import redisco

from src.www import settings
from src.www import app
from src.www.app.tools.web_session import Initializer
from src.www.app import (models, controllers)
from urls import (URLS, HANDLER)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror)
from src.www.app.models.counter import Counter
from src.www.app.models.user import User
from src.www.app.models import user
from src.www.app.models.usergroup import UserGroup
from src.www.app.models.views import Views
from src.www.app.controllers.manage_handler import (ManageUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)
from src.www.app.controllers.login_handler import Login
from src.www.app.controllers.manage_handler import (CreateUserGroup,CreateUser,ModifUser)


def suite():
    testSuite1 = unittest.makeSuite(TestUser, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestUser(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        :return:
        '''

        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        settings.REDIS_PORT = 8911
        settings.REDIS_DB_NUM = 0

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

        app.session = web.session.Session(self.appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                              User=models.user.User,
                                                                                                              UserGroup=models.usergroup.UserGroup,
                                                                                                              BanLogin=controllers.login_handler.BanLogin,
                                                                                                              settings=settings,
                                                                                                              app=app,
                                                                                                              ))

        web.config.session_parameters['cookie_name'] = 'webpy_session_id'
        web.config.session_parameters['cookie_domain'] = None
        web.config.session_parameters['timeout'] = 10
        web.config.session_parameters['ignore_expiry'] = True
        web.config.session_parameters['ignore_change_ip'] = False
        web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
        web.config.session_parameters['expired_message'] = 'Session expired'
    def tearDown(self):
        # return
        print u'清空了数据库%s' % settings.REDIS_DB
        self.redis.flushdb()


    def test_createUserGroup(self):
        '''
        测试生成用户组
        :return:
        '''

        self.redis.flushdb()

        ugname = 'GM'
        ug = UserGroup.createNewUserGroup(ugname, UserGroup.getAllPms())

        print u'生成用户组完毕...'
        ug = UserGroup.obj(name=ugname)
        if not ug.is_valid:
            raise ValueError(u'生成用户组失败!!!')
        print u'生成用户组成功...'



    def test_UserGroupAll(self):
        ugs = UserGroup.all()
        UserGroup.createRootGroup()
        print u'查询到用户组%d个' % len(ugs)
        for ug in ugs:
            print ug.name

