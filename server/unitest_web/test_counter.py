#coding=utf-8
'''
Created on 2014-09-27

@author: Shawn
'''

import unittest

import redis
import redisco

from server.www import settings
from server.www.app.models.counter import Counter

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
        print "c.uuid->", c.uid
        print "c.uguid->", c.ugid

        print u'\n重新生成实例...'
        c = Counter.obj()
        print 'id(c)->', id(c)
        c.incr(Counter.user)
        c.incr(Counter.userGroup)
        print "c.uuid->", c.uid
        print "c.uguid->", c.ugid



    def test_addCountItem(self):
        '''
        旧数据中的计数器能否兼容添加新的计数项
        :return:
        '''
        ''' 清空数据库 '''
        # self.redis.flushdb()

        ''' 生成数据 '''
        c = Counter.obj()
        c.incr(Counter.user)

        ''' 生成新统计项数据 '''
        c = Counter.obj()
        c.incr(Counter.userGroup)

        print "c.uuid->", c.uid
        print "c.uguid->", c.ugid


        # ''' 添加计数项 test_item1'''
        # Counter.count_test_item1 = models.Counter(unique=True)
        # Counter.test_item1 = u'count_test_item1'

        # ''' 重新生成实例 '''
        # c = Counter.obj()
        # c.incr(Counter.test_item1)
        #
        # print "Counter.count_test_item1->", Counter.count_test_item1

