#coding=utf-8
'''
Created on 2014-10-31

@author: Shawn
'''


__author__ = 'Shawn'

import web
from skeleton.www.app.controllers import render
from skeleton.www.app.controllers.login_handler import (Login, BanLogin)
import skeleton.www.app as app
from skeleton.www.app.models.user import User
from skeleton.www.app.models.usergroup import UserGroup

class Session(object):
    def __call__(self, *args, **kwargs):
        '''
        session登录后要做的操作
        :param args:
        :param kwargs:
        :return:
        '''
        app.session.user = None

        print ''' 尚未注册的用户 '''
        if app.session.user is None:
            errInfo = u'未注册的账户...'
            print errInfo
            web.redirect(Login.URL)
            return

        ''' 禁止登录 '''
        if app.session.user.isHavePms(UserGroup.PERMISSION_BAN_LOGIN):
            web.redirect(BanLogin.URL)
            return
