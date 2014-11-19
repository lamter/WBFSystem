# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import web

from . import render
import app
import settings
import base_handler
from ..models.views import Views
from ..models.user import User
from ..models.usergroup import UserGroup

class ManageUser(base_handler.BaseHandler):

    URL =u'/manage_user'
    url = r'/manage_user.*'

    def GET(self):
        try:
            if not settings.DEBUG and not app.session.login:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(app.session.username)
            views = Views(user)

            ''' 渲染管理用户选项 '''
            # views.render_manage_user_option()

            ''' 渲染用户列表 '''
            views.render_manage_user(ManageUser, CreateUserGroup, CreateUser, ModifUser)

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

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_CREATE_USER_GROUP):
                return u'没有创建用户组的权限...'

            # print u'创建用户中...'
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



class CreateUser(base_handler.BaseHandler):
    """
    创建用户
    """
    URL = u'/create_user'
    url = r'/create_user.*'

    name = u'username'
    passwd = u'userpasswd'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_CREATE_USER):
                return u'没有创建用户的权限...'

            # print u'创建用户中...'
            newU = web.input()

            # print 'newU->', newU

            ''' 创建用户 '''
            u = User.createNewUser(newU.username, newU.userpasswd)

            ''' 设定用户组 '''
            try:
                for ug in UserGroup.all():
                    if getattr(newU, ug.name) == u'on':
                        u.addUserGroup(ug)
            except:
                raise ValueError(u'创建用户成功, 但是添加用户组失败')

            return u'创建用户%s成功' % u.username

        except:
            return self.errInfo()



class ModifUser(base_handler.BaseHandler):
    """
    修改用户信息界面
    """
    URL = u'/modif_user_info'
    url = r'/modif_user_info.*'

    uname = u'username'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
                return u'没有修改用户信息的权限...'

            views = Views(user)

            modifU = web.input()
            print 'modifU->', modifU

            ''' 获得待修改的用户实例 '''
            modfUser = User.obj(modifU.username)
            if modfUser is None:
                raise ValueError(u'指定的用户%s不存在...' % modifU.username)

            views.render_modif_user(modfUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)

            return views.modif_user

        except:
            return self.errInfo()



class ModifUserN(base_handler.BaseHandler):
    """
    修改用户名
    """
    URL = u'/modif_user_name'
    url = r'/modif_user_name.*'

    uname = u'uname'
    newN = u'newN'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
                return u'没有修改用户信息的权限...'

            modifU = web.input()
            print 'modifU->', modifU
            ''' 获得用户实例 '''
            u = User.obj(modifU.uname)
            if u is None:
                raise ValueError(u'指定的用户%s不存在...' % modifU.uname)

            ''' 修改密码 '''
            u.username = u'%s' % modifU.newN
            if u.errors:
                raise ValueError(u.errStr)

            ''' 修改后存库 '''
            u.save()
            return u'修改用户%s的用户名%s为成功' % (modifU.uname, modifU.newN)

        except:
            return self.errInfo()



class ModifUserPW(base_handler.BaseHandler):
    """
    修改用户密码
    """
    URL = u'/modif_user_pw'
    url = r'/modif_user_pw.*'

    name = u'username'
    pw = u'newpw'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
                return u'没有修改用户信息的权限...'

            modifU = web.input()
            # print 'modfU->', modifU

            ''' 获得用户实例 '''
            u = User.obj(modifU.username)
            if u is None:
                raise ValueError(u'指定的用户%s不存在...' % modifU.username)

            ''' 修改密码 '''
            u.password = u'%s' % modifU.newpw

            if u.errors:
                raise ValueError(u.errStr)

            ''' 修改后存库 '''
            u.save()

            return u'修改用户%s的密码成功' % u.username

        except:
            return self.errInfo()



class AddUG(base_handler.BaseHandler):
    """
    给用户添加用户组
    """
    URL = u'/modif_user_add_ug'
    url = r'/modif_user_add_ug.*'

    uname = u'uname'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
                return u'没有修改用户信息的权限...'

            modifU = web.input()
            # print 'modfU->', modifU

            ''' 获得待修改的用户实例 '''
            u = User.obj(modifU.uname)
            if u is None:
                raise ValueError(u'指定的用户%s不存在...' % modifU.uname)

            ''' 添加用户组 '''
            joinUGNames = u.getUGNames()
            for ug in UserGroup.all():
                if modifU.get(ug.name) != u'on':
                    continue
                if u.isInUg(ug):
                    ''' 已经加入的组忽略 '''
                    continue
                ''' 符合条件则添加 '''
                u.addUserGroup(ug)

            ''' 没有错误则可以存库 '''
            if u.errors:
                raise ValueError(u.errStr)

            ''' 修改后存库 '''
            u.save()

            return u'为用户%s添加用户组成功' % u.username

        except:
            return self.errInfo()


class RemoveUG(base_handler.BaseHandler):
    """
    移除用户的用户组
    """
    URL = u'/modif_user_remove_ug'
    url = r'/modif_user_remove_ug.*'

    uname = u'uname'

    def POST(self):
        try:
            if not app.session.login and not settings.DEBUG:
                return render.login(u'登录超时，请重新登录')

            ''' 检查权限 '''
            user = User.obj(app.session.username)
            if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
                return u'没有修改用户信息的权限...'

            modifU = web.input()
            # print 'modfU->', modifU

            ''' 获得用户实例 '''
            u = User.obj(modifU.uname)
            if u is None:
                raise ValueError(u'指定的用户%s不存在...' % modifU.uname)

            ''' 移除用户组 '''
            for ug in UserGroup.all():
                if modifU.get(ug.name) != u'on':
                    continue
                if not u.isInUg(ug):
                    ''' 不在用户组中的忽略 '''
                    continue
                ''' 符合条件的移除 '''
                u.removeUserGroup(ug)

            ''' 没有错误则可以存库 '''
            if u.errors:
                raise ValueError(u.errStr)

            ''' 修改后存库 '''
            u.save()

            return u'为用户%s移除用户组成功' % u.username

        except:
            return self.errInfo()