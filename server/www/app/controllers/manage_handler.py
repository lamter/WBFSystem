# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import render
import server.www
from server.www import settings
import base_handler
import main_handler
from server.www.app.models.views import Views
from server.www.app.models.user import User
from server.www.app.models.usergroup import UserGroup

class ManageUser(base_handler.BaseHandler):

    URL =u'/manage_user'
    url = r'/manage_user.*'

    # @classmethod
    # def URL(cls):
    #     '''
    #     :return:
    #     '''
    #     return main_handler.Main().URL + u'/manage_user'


    # @classmethod
    # def url(self):
    #     '''
    #     :return:
    #     '''
    #     return r'%s/manage_user.*' % main_handler.Main.URL


    def GET(self):
        try:
            if not settings.DEBUG and not server.www.session.login:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(server.www.session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            # views.render_manage_user_option()

            ''' 渲染用户列表 '''
            views.render_manage_user(ManageUser, CreateUserGroup)

            ''' 用户管理选择 '''
            return views.manage_user

        except:
            return self.errInfo()




class CreateUserGroup(base_handler.BaseHandler):
    """
    创建用户组
    """
    URL = u'/create_user_group'
    url = r'/create_user_group.*'

    ugname = u'ugname'

    # @classmethod
    # def URL(cls):
    #     return ManageUser.URL + u'/create_user_group'

    # @classmethod
    # def url(cls):
    #     return r'%s/create_user_group.*' % ManageUser.URL

    def POST(self):
        try:
            if not server.www.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            print u'创建用户中...'
            newUg = web.input()
            # print 'newUg->', newUg

            ''' 获取设定的权限 '''
            pms = 0
            for pmn, pm in UserGroup.getPermissionDic().items():
                if newUg.get(pmn) == u'on':
                    pms |= pm
            # print 'pms->', pms

            ''' 创建用户组 '''
            UserGroup.createNewUserGroup(newUg.ugname, pms)

            return u'创建用户组%s成功' % newUg.ugname

        except:
            return self.errInfo()