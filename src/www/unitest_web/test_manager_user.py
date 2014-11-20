#coding=utf-8
'''
Created on 2014-11-04

@author: Shawn
'''

import unittest

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
from src.www.app.models.usergroup import UserGroup
from src.www.app.models.views import Views
from src.www.app.controllers.manage_handler import (ManageUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)
from src.www.app.controllers.login_handler import Login
from src.www.app.controllers.manage_handler import (CreateUserGroup,CreateUser,ModifUser)


def suite():
    testSuite1 = unittest.makeSuite(TestManageUser, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestManageUser(unittest.TestCase):
    '''
    计数器counter的测试
    '''
    def setUp(self):
        '''
        :return:
        '''

        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        settings.REDIS_PORT = 8911
        # settings.REDIS_DB_NUM = 0

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
        self.redis.flushdb()

    def test_render_manage_user_option(self):
        '''
        渲染 管理用户选项
        :return:
        '''
        User.createRoot()
        user = User.obj(User.rootAccount)
        v = Views(user)
        # v.render_manage_user_option(None)
        # v.html('manage_user_option')


    def test_render_manage_user(self):
        '''
        渲染 manage_user页面
        :return:
        '''
        User.createRoot()
        user = User.obj(User.rootAccount)
        views = Views(user)
        views.render_manage_user(ManageUser,CreateUserGroup,CreateUser,ModifUser)
        views.html('manage_user')


    def test_CreateUserGroup(self):
        '''
        测试 创建用户组
        :return:
        '''

        settings.debug_username = User.rootAccount

        user = User.obj(settings.debug_username)
        if not user:
            User.createRoot()
            user = User.obj(settings.debug_username)

        v = Views(user)
        v.html(self.appM.request(ManageUser.url).data)


    def test_render_modif_user(self):
        '''
        测试 修改用户信息界面
        :return:
        '''
        user = User.obj(User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(User.rootAccount)

        views = Views(user)
        views.render_modif_user(user, ModifUserN, ModifUserPW, AddUG, RemoveUG)
        views.html('modif_user')



    def test_render_user_list(self):
        '''
        渲染 用户列表
        :return:
        '''
        # self.redis.flushdb()

        user = User.obj(User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(User.rootAccount)

        un = 'test1'
        pw = '123456'
        User.createNewUser(un, pw)

        views = Views(user)
        views.render_user_list(ModifUser)
        views.html('user_list')


    def test_render_user_group_list(self):
        '''
        渲染 用户组信息列表
        :return:
        '''
        User.createRoot()
        user = User.obj(User.rootAccount)
        ugn = u'测试1'
        pms = UserGroup.getAllPms()
        UserGroup.createNewUserGroup(ugn, pms)

        views = Views(user)
        views.render_user_group_list()
        views.html('user_group_list')


    def test_render_create_user_group(self):
        '''
        渲染 用户组信息列表
        :return:
        '''
        User.createRoot()
        user = User.obj(User.rootAccount)
        ugn = u'测试1'
        pms = UserGroup.getAllPms()
        UserGroup.createNewUserGroup(ugn, pms)

        views = Views(user)
        views.render_create_user_group(CreateUserGroup)
        views.html('create_user_group')


    def test_render_create_user(self):
        '''
        测试 渲染 创建用户 界面
        :return:
        '''

        User.createRoot()
        user = User.obj(User.rootAccount)

        ugn = u'测试1'
        pms = UserGroup.getAllPms()
        UserGroup.createNewUserGroup(ugn, pms)

        views = Views(user)
        views.render_create_user(CreateUser)
        views.html('create_user')


    def test_ManageUser(self):
        '''
        :return:
        '''
        User.createRoot()
        ''' 渲染 '''
        settings.debug_username = User.rootAccount
        user = User.obj(settings.debug_username)

        v = Views(user)
        v.html(self.appM.request(localpart=ManageUser.URL, method='GET').data)