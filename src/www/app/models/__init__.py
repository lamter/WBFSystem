#coding=utf-8
'''
Created on 2014-10-27

@author: Shawn
'''

import sys
import os

if os.path.abspath(os.path.join(os.path.dirname('settings.py'),os.path.pardir)) not in sys.path:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname('settings.py'),os.path.pardir)))

from user import User
from usergroup import UserGroup

class Init(object):


    def __call__(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''

        self.root()


    def root(self):
        '''
        如果初始化出用户后没有超级用户，那么使用默认配置初始化出超级用户
        :return:
        '''

        root = User.obj(username=User.rootAccount)

        if root:
            ''' 如果已经存在root 用户，那么删除掉 '''
            root.delete()

        root = User.createRoot()
        root.save()


init = Init()


