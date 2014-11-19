#coding=utf-8
'''
Created on 2014-10-27

@author: Shawn
'''
__author__ = 'Shawn'

import unittest

import redis
import redisco

from src.www import settings
from src.www.app.models.usergroup import UserGroup


def suite():
    testSuite1 = unittest.makeSuite(TestUserGroup, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestUserGroup(unittest.TestCase):
    '''
    ServerData的测试
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
        ug = UserGroup.obj(ugname)
        if not ug.is_valid:
            raise ValueError(u'生成用户组失败!!!')
        print u'生成用户组成功...'


    def test_UserGroupAll(self):
        ugs = UserGroup.all()
        UserGroup.createRootGroup()
        print u'查询到用户组%d个' % len(ugs)
        for ug in ugs:
            print ug.name