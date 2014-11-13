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


    @property
    def errStr(self):
        '''
        将 self.errors转为字符串
        :return:
        '''
        _errs = []
        if self.errors:
            for errs in self.errors:
                _errs.append(u' '.join(errs))

        return u'. '.join(_errs)


    @classmethod
    def all(cls):
        '''
        获得所有实例
        :return:
        '''
        return cls.objects.filter().all()