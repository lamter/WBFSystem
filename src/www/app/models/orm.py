#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''


import json
import time

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()

from redisco import models


class RediscoModle(models.Model):
    def log(self):
        '''
        :return:
        '''
        print '%s====================' % self.__class__.__name__
        for k,v in self.__dict__.items():
            print k,':', v
        print '%s====================' % self.__class__.__name__


    @classmethod
    def obj(cls, **kwargs):
        '''
        实例化，属性名=属性值
        如 id=1
        这个属性必须是强制唯一的，即初始化时有参数unique=True
        :param kwargs:
        :return:
        '''
        if 'id' in kwargs:
            # c = cls.objects.filter().get_by_id(kwargs.get('id'))
            c = cls.objects.get_by_id(kwargs.get('id'))
        else:
            c = cls.objects.filter(**kwargs).first()
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
                _errs.append(' '.join(errs))

        return '. '.join(_errs)


    @classmethod
    def all(cls):
        '''
        获得所有实例
        :return:
        '''
        return cls.objects.filter().all()