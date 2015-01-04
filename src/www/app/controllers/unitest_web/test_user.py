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
        print '清空了数据库%s' % settings.REDIS_DB
        self.redis.flushdb()


    def test_createUser(self):
        '''
        :return:
        '''
        self.redis.flushdb()

        username, password = 'shawn', '123456'
        u = User.createNewUser(username, password)

        print '生成用户完毕...'
        nu = User.obj(username=username)
        if not nu.is_valid:
            raise ValueError('生成玩家失败!!!')
        print '生成用户成功...'



    def test_objNoUser(self):
        '''
        获取一个不存在的用户
        :return:
        '''
        self.redis.flushdb()

        username = 'adfgagdsdfadsg'
        u = User.obj(username=username)
        if u is not None:
            raise ValueError('不存在的用户不是None')



    def test_createSameNameUer(self):
        '''
        尝试生成同名用户
        :return:
        '''
        self.redis.flushdb()
        username, password = 'aaa111', 'bbb222'
        u = User.createNewUser(username, password)
        try:
            u = User.createNewUser(username, password)
        except:
            errInfo = traceback.format_exc()
            if user.NEW_ACCOUNT_ERR_NOT_UNIQUE in errInfo:
                print '不能创建重名账户...'
            else:
                raise errInfo



    def test_nonstandardPW(self):
        '''
        非标注密码
        :return:
        '''
        self.redis.flushdb()

        ''' 密码过长 '''
        un = 'Shawn'
        pw = ''.join(['1' for i in range(user.ACCOUNT_MAX_SIZE+1)])
        try:
            err = '能够生成过 长 的密码!!'
            u = User.createNewUser(un, pw)
            raise ValueError(err)
        except :
            errInfo = traceback.format_exc()
            if err in errInfo:
                raise ValueError(errInfo)


        un = 'Shawn'
        pw = ''.join(['1' for i in range(user.ACCOUNT_MIN_SIZE-1)])
        try:
            err = '能够生成过 短 的密码!!'
            u = User.createNewUser(un, pw)
            raise ValueError(err)
        except:
            errInfo = traceback.format_exc()
            if err in errInfo:
                raise ValueError(errInfo)




    def test_creatRoot(self):
        '''
        创建root用户
        :return:
        '''
        self.redis.flushdb()

        root = User.createRoot()
        print 'root name ->', root.username
        rootUg = root.getUserGroupByName(User.rootAccount)

        print rootUg.pms
        print root.userGroups

        root.save()

        root = User.obj(username=User.rootAccount)
        rootUg = root.getUserGroupByName(UserGroup.rootGroup)

        print rootUg.pms
        print root.userGroups



    def test_userAll(self):
        '''
        实例化所有角色
        :return:
        '''
        models.Init()
        users = User.all()
        print len(users)
        for u in users:
            print u.username


    def test_addUserGroup(self):
        '''
        测试 给用户添加用户组
        :return:
        '''

        ''' 清空数据库 '''
        self.redis.flushdb()

        ''' 生成测试用户 '''
        un = 'test01'
        pw = '123456'
        user = User.createNewUser(un, pw)

        ''' 生成测试用户组 '''
        ugn = 'testUG01'
        ug = UserGroup.createNewUserGroup(ugn)
        print 'ug->', id(ug), ug

        ''' 添加用户组 '''
        user.addUserGroup(ug)
        ug = UserGroup.obj(name=ugn)
        print 'ug->', id(ug), ug

        ''' 添加用户组 '''
        if ug not in user.userGroups:
            raise ValueError('添加  用户组失败')

        ''' 移除用户组 '''
        user.removeUserGroup(ug)
        if ug in user.userGroups:
            raise ValueError('移除 用户组失败')



