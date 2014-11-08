#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''

__author__ = 'Shawn'

import unittest
import traceback

import redis
import redisco

import redis
from redis.exceptions import *
from redisco.containers import *
from server.www import settings



def suite():
    testSuite1 = unittest.makeSuite(RedisConnection, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase



class RedisConnection(unittest.TestCase):
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
        # redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


    def test_rediscoConnFaild(self):
        '''
        测试redisco连接失败
        :return:
        '''
        host = 'localhost'
        port = 123
        db = 0
        redisco.connection_setup(host=host, port=port, db=db)

        try:
            redisco.connection.ping()
        except ConnectionError:
            print u'错误连接，正常断开...'




