#coding=utf-8
'''
Created on 2014-09-27

计数器模块

@author: Shawn
'''

from redisco import models

from skeleton.www.app.models import orm


class Counter(orm.RediscoModle):
    '''
    计数器模块，用来计数
    '''

    ''' 计数项 '''
    count_user = models.Counter(unique=True)
    user = u'count_user'
    count_userGroup = models.Counter(unique=True)
    userGroup = u'count_userGroup'

    def __init__(self, **kwargs):
        orm.RediscoModle.__init__(self, **kwargs)


    def validate(self):
        for errs in self._errors:
            print u" ".join(errs)
        if self._errors:
            print u'are the reasons to '


    @classmethod
    def createNewCounter(cls):
        '''
        生成一个新的计数器
        :return:
        '''
        return cls()


    @property
    def uid(self):
        '''
        返回用户当前最大的的uid
        :return:
        '''

        return self.count_user


    @property
    def ugid(self):
        '''
        返回用户组uid
        :return:
        '''
        return self.count_userGroup


    @classmethod
    def obj(cls, *args):
        '''
        实例化计数器
        :return:
        '''
        c = cls.objects.filter().first()
        if c is None:
            c = cls.createNewCounter()
            c.save()
        return c


    # @classmethod
    # def incr(cls, att, val=1):
    #     '''
    #     重写计数器
    #     :param att: 计数项的变量名, 如 count_user
    #     :return:
    #     '''
    #     c = cls.objects.filter().first()
    #     if c is None:
    #         c = cls.createNewCounter()
    #         c.save()
    #
    #     models.Model.incr(c, att, val)
