#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''


import json
import time

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()

import traceback
from redisco import models



class RediscoModle(models.Model):
    def log(self):
        '''
        :return:
        '''
        print u'%s====================' % self.__class__.__name__
        for k,v in self.__dict__.items():
            print k,':', v
        print u'%s====================' % self.__class__.__name__

    @classmethod
    def obj(cls, *args):
        '''
        实例化
        :return:
        '''
        c = cls.objects.filter().first()
        return c