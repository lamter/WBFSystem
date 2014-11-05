#coding=utf-8
'''
Created on 2014-10-31

@author: Shawn
'''


__author__ = 'Shawn'

import web

from skeleton.www import settings
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
        if not hasattr(app.session, 'username'):
            ''' 新的会话，动态绑定username属性 '''
            setattr(app.session, 'username', None)
            if settings.DEBUG:
                ''' 测试环境需要在其他地方将预设的debug_username传进来作为seesion.username的值 '''
                setattr(app.session, 'username', settings.debug_username)

        if not hasattr(app.session, 'login'):
            ''' 新的会话，动态绑定login属性，默认是未登录 '''
            setattr(app.session, 'login', False)
            # if settings.DEBUG:
            #     ''' 测试环境需要在其他地方将预设的debug_login传进来作为seesion.login的值 '''
            #     setattr(app.session, 'login', settings.debug_login)

        user = User.obj(app.session.username)

        # ''' 尚未注册的用户 '''
        # if app.session.user is None:
        #     errInfo = u'未注册的账户...'
        #     print errInfo
        #     web.redirect(Login.URL)
        #     return

        ''' 禁止登录 '''
        if user and user.isHavePms(UserGroup.PERMISSION_BAN_LOGIN):
            web.redirect(BanLogin.URL)
            return
