#coding=utf-8
'''
Created on 2014-11-04

@author: Shawn
'''

import unittest

import web
import redis
import redisco

import src.www.settings as settings
import src.www.main as main

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


    def test_render_manage_user_option(self):
        '''
        渲染 管理用户选项
        :return:
        '''
        user = User.obj(User.rootAccount)
        v = Views(user)
        # v.render_manage_user_option(None)
        # v.html('manage_user_option')


    def test_render_manage_user(self):
        '''
        渲染 manage_user页面
        :return:
        '''
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
        v.html(main.application.request(ManageUser.url).data)


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
        user = User.obj(User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(User.rootAccount)

        views = Views(user)
        views.render_user_list(ModifUser)
        views.html('user_list')



