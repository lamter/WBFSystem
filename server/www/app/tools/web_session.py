#coding=utf-8
'''
Created on 2014-10-31

@author: Shawn
'''


__author__ = 'Shawn'

import web

from server.www import settings
import server.www
# from app import session

class Initializer(object):
    def __init__(self, *args, **kwargs):
        '''
        :param app:
        :return:
        '''
        self.User = kwargs.get('User')
        self.UserGroup = kwargs.get('UserGroup')
        self.BanLogin = kwargs.get('BanLogin')


    def __call__(self, *args, **kwargs):
        '''
        session登录后要做的操作
        :param args:
        :param kwargs:
        :return:
        '''
        if not hasattr(server.www.session, 'username'):
            ''' 新的会话，动态绑定username属性 '''
            setattr(server.www.session, 'username', None)
            if settings.DEBUG:
                ''' 测试环境需要在其他地方将预设的debug_username传进来作为seesion.username的值 '''
                setattr(server.www.session, 'username', server.www.settings.debug_username)

        if not hasattr(server.www.session, 'login'):
            ''' 新的会话，动态绑定login属性，默认是未登录 '''
            setattr(server.www.session, 'login', False)
            # if settings.DEBUG:
            #     ''' 测试环境需要在其他地方将预设的debug_login传进来作为seesion.login的值 '''
            #     setattr(app.session, 'login', settings.debug_login)

        user = self.User.obj(server.www.session.username)

        # ''' 尚未注册的用户 '''
        # if app.session.user is None:
        #     errInfo = u'未注册的账户...'
        #     print errInfo
        #     web.redirect(Login.URL)
        #     return

        ''' 禁止登录 '''
        if user and user.isHavePms(self.UserGroup.PERMISSION_BAN_LOGIN):
            web.redirect(self.BanLogin.URL)
            return
