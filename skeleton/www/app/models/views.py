#coding=utf-8
'''
Created on 2014-10-28

@author: Shawn
'''

import web

from skeleton.www.app.controllers import render
from skeleton.www.app.models.usergroup import UserGroup


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



    def render_manager_user_option(self):
        '''
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_CREATE_USER | UserGroup.PERMISSION_CREATE_USER_GROUP | UserGroup.PERMISSION_USER_GROUP_LIST | UserGroup.PERMISSION_USER_LIST

        if not self.user.isHavePms(pms):
            ''' 拥有权限才能渲染模板 '''
            return

        self.manager_user_option = render.manager_user_option(self.user)



    def render_user_list(self):
        '''

        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_USER_GROUP_LIST

        ''' 拥有权限才能渲染模板 '''
        if not self.user.isHavePms(pms):
            return

        self.user_list = render.user_list(self.user)
