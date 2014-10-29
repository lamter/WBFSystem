#coding=utf-8
'''
Created on 2014-09-27

@author: Shawn
'''

import unittest

import redis
import redisco

from skeleton.www import settings
from skeleton.www.app.tools.counter import Counter

def suite():
    testSuite1 = unittest.makeSuite(TestCounter, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestCounter(unittest.TestCase):
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
        settings.REDIS_DB_NUM = 0

        ''' redisco连接 '''
        settings.rd = redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


    def tearDown(self):
        return
        print u'清空了数据库%s' % settings.REDIS_DB
        self.redis.flushdb()


    def test_createCounter(self):
        '''
        创建计数器
        :return:
        '''
        ''' 清空数据库 '''
        self.redis.flushdb()

        c = Counter.obj()
        c.incr(Counter.user)
        c.incr(Counter.userGroup)
        print 'id(c)->', id(c)
        print "c.uuid->", c.uuid
        print "c.uguid->", c.uguid

        print u'\n重新生成实例...'
        c = Counter.obj()
        print 'id(c)->', id(c)
        c.incr(Counter.user)
        c.incr(Counter.userGroup)
        print "c.uuid->", c.uuid
        print "c.uguid->", c.uguid




    def test_userUid(self):
        '''
        :return:
        '''
        c = Counter.createNewCounter()

        print u'userUid->', c.uuid
        c.incr('user')
        print u'after incr ...'
        print u'userUid->', c.uuid

