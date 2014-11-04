#coding=utf-8
'''
Created on 2014-10-28

@author: Shawn
'''

import web
from skeleton.www.settings import (absolute)
from skeleton.www.app.controllers import render
import skeleton.www.app.controllers.main_handler
from skeleton.www.app.models.usergroup import UserGroup
from skeleton.www.app.models.user import User


class Views(object):
    """
    用于传递页面上各个模块的内容
    """
    def __init__(self, user=None):
        self.user = user
        if self.user == None:
            raise ValueError(u'模板需要一个用户对象self.user')

    def isHasAttr(self, attr):
        return hasattr(self, attr)


    def html(self, attr):
        '''
        将制定的html生成html文件保存到www.tmp下
        :param attr:
        :return:
        '''
        if self.isHasAttr(attr):
            with open(absolute('tmp/test.html'), 'wb') as h:
                a = u'%s' % getattr(self, attr)
                h.write(a)
        else:
            with open(absolute('tmp/test.html'), 'wb') as h:
                h.write(attr)



    def render_manage_user_option(self):
        '''
        管理用户选项
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_CREATE_USER | UserGroup.PERMISSION_CREATE_USER_GROUP | UserGroup.PERMISSION_USER_GROUP_LIST | UserGroup.PERMISSION_USER_LIST

        if not self.user.isHavePms(pms):
            ''' 拥有权限才能渲染模板 '''
            return

        self.manage_user_option = render.manage_user_option(self.user, UserGroup, skeleton.www.app.controllers.main_handler)



    def render_manage_user(self):
        '''
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_USER_GROUP_LIST

        ''' 拥有权限才能渲染模板 '''
        if not self.user.isHavePms(pms):
            return

        ''' 管理用户选项 '''
        self.render_manage_user_option()

        ''' 所有用户 '''
        users = User.all()

        self.manage_user = render.manage_user(self.user, UserGroup, self, users)
