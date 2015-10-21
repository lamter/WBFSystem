# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: lamter

This module contains the main handler of the application.
"""

import web

from . import (render, session)
from .. import settings
from base_handler import BaseHandler
from ..models.views import Views
from ..models.user import User
from ..models.usergroup import UserGroup


class ManageUser(BaseHandler):

    URL = BaseHandler.URL + '/manage_user'
    url = BaseHandler.url + r'/manage_user.*'

    def GET(self):

        user = session().user

        if not user.isHavePms(UserGroup.PERMISSION_MANAGER_USER):
            return '没有 打开 用户管理页面 的权限...'

        views = Views(user)

        ''' 渲染管理用户选项 '''
        # views.render_manage_user_option()

        ''' 渲染 用户信息列表 '''
        views.render_user_list(ModifUser)

        ''' 渲染 用户组信息列表 '''
        views.render_user_group_list()

        ''' 渲染 创建用户组界面 '''
        views.render_create_user_group(CreateUserGroup)

        ''' 渲染 创建用户 界面 '''
        views.render_create_user(CreateUser)

        ''' 渲染 修改用户组 界面 '''
        views.render_modif_user_group(ModifUserGroup)

        ''' 渲染用户管理界面列表 '''
        views.render_manage_user()

        ''' 用户管理选择 '''
        return views.manage_user



class CreateUserGroup(BaseHandler):
    """
    创建用户组
    """
    URL = BaseHandler.URL +  '/create_user_group'
    url = BaseHandler.url + r'/create_user_group.*'

    ugname = 'ugname'

    def POST(self):

        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_CREATE_USER_GROUP):
            return '没有创建用户组的权限...'

        # print '创建用户中...'
        newUg = web.input()
        # print 'newUg->', newUg

        ''' 获取设定的权限 '''
        pms = set([])
        for pmn, pm in UserGroup.getPermissionDic().items():
            if newUg.get(pmn) == 'on':
                pms |= pm
        # print 'pms->', pms

        ''' 创建用户组 '''
        UserGroup.createNewUserGroup(newUg.ugname, pms)

        return '创建用户组%s成功' % newUg.ugname


class CreateUser(BaseHandler):
    """
    创建用户
    """
    URL = BaseHandler.URL +  '/create_user'
    url = BaseHandler.url + r'/create_user.*'

    name = 'username'
    passwd = 'userpasswd'

    ugsign = 'ugid_'            # 返回的用户组的值为 ugid_1

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_CREATE_USER):
            return '没有创建用户的权限...'

        # print '创建用户中...'
        newU = web.input()

        # print 'newU->', newU
        # for k,v in newU.items():
        #     print type(k), k,':',v

        ''' 创建用户 '''
        u = User.createNewUser(newU.username, newU.userpasswd)

        ''' 设定用户组 '''
        try:
            for k,v in newU.items():
                if v != 'on':
                    ''' on 才是属于被勾选的 '''
                    continue
                ugid = k.split(self.ugsign)[1]
                ug = UserGroup.obj(id=ugid)
                if ug:
                    u.addUserGroup(ug)
        except:
            raise ValueError('创建用户成功, 但是添加用户组失败')

        return '创建用户%s成功' % u.username



class ModifUser(BaseHandler):
    """
    修改用户信息界面
    """
    URL = BaseHandler.URL +  '/modif_user_info'
    url = BaseHandler.url + r'/modif_user_info.*'

    uname = 'username'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
            return '没有修改用户信息的权限...'

        views = Views(user)

        modifU = web.input()

        ''' 获得待修改的用户实例 '''
        modfUser = User.obj(username=modifU.username)
        if modfUser is None:
            raise ValueError('指定的用户%s不存在...' % modifU.username)

        views.render_modif_user(modfUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)

        return views.modif_user



class ModifUserN(BaseHandler):
    """
    修改用户名
    """
    URL = BaseHandler.URL + '/modif_user_name'
    url = BaseHandler.url + r'/modif_user_name.*'

    uname = 'uname'
    newN = 'newN'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
            return '没有修改用户信息的权限...'

        modifU = web.input()
        print 'modifU->', modifU
        ''' 获得用户实例 '''
        u = User.obj(username=modifU.uname)
        if u is None:
            raise ValueError('指定的用户%s不存在...' % modifU.uname)

        ''' 修改密码 '''
        u.username = '%s' % modifU.newN
        if u.errors:
            raise ValueError(u.errStr)

        ''' 修改后存库 '''
        u.save()
        return '修改用户%s的用户名%s为成功' % (modifU.uname, modifU.newN)



class ModifUserPW(BaseHandler):
    """
    修改用户密码
    """
    URL = BaseHandler.URL +  '/modif_user_pw'
    url = BaseHandler.url + r'/modif_user_pw.*'

    name = 'username'
    pw = 'newpw'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
            return '没有修改用户信息的权限...'

        modifU = web.input()
        # print 'modfU->', modifU

        ''' 获得用户实例 '''
        u = User.obj(username=modifU.username)
        if u is None:
            raise ValueError('指定的用户%s不存在...' % modifU.username)

        ''' 修改密码 '''
        u.password = '%s' % modifU.newpw

        if u.errors:
            raise ValueError(u.errStr)

        ''' 修改后存库 '''
        u.save()

        return '修改用户%s的密码成功' % u.username



class AddUG(BaseHandler):
    """
    给用户添加用户组
    """
    URL = BaseHandler.URL +  '/modif_user_add_ug'
    url = BaseHandler.url + r'/modif_user_add_ug.*'

    uname = 'uname'

    ugsign = 'ugid_'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
            return '没有修改用户信息的权限...'

        modifU = web.input()
        # print 'modfU->', modifU

        ''' 获得待修改的用户实例 '''
        u = User.obj(username=modifU.uname)
        if u is None:
            raise ValueError('指定的用户%s不存在...' % modifU.uname)

        ''' 添加用户组 '''
        for k,v in modifU.items():
            if v != 'on':
                continue
            try:
                ugid = k.split(self.ugsign)[1]
            except:
                continue
            ug = UserGroup.obj(id=ugid)
            if ug and not u.isInUg(ug):
                ''' 没有加入的用户才添加 '''
                u.addUserGroup(ug)

        ''' 没有错误则可以存库 '''
        if u.errors:
            raise ValueError(u.errStr)

        ''' 修改后存库 '''
        u.save()

        return '为用户%s添加用户组成功' % u.username



class RemoveUG(BaseHandler):
    """
    移除用户的用户组
    """
    URL = BaseHandler.URL +  '/modif_user_remove_ug'
    url = BaseHandler.url + r'/modif_user_remove_ug.*'

    uname = 'uname'

    ugsign = 'ugid_'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER):
            return '没有修改用户信息的权限...'

        modifU = web.input()
        # print 'modfU->', modifU

        ''' 获得用户实例 '''
        u = User.obj(username=modifU.uname)
        if u is None:
            raise ValueError('指定的用户%s不存在...' % modifU.uname)

        ''' 添加用户组 '''
        for k,v in modifU.items():
            if v != 'on':
                continue
            ugid = k.split(self.ugsign)[1]
            ug = UserGroup.obj(id=ugid)
            if ug and u.isInUg(ug):
                ''' 没有加入的用户才添加 '''
                u.removeUserGroup(ug)

        ''' 没有错误则可以存库 '''
        if u.errors:
            raise ValueError(u.errStr)

        ''' 修改后存库 '''
        u.save()

        return '为用户%s移除用户组成功' % u.username



class ModifUserGroup(BaseHandler):
    """
    修改用户组信息
    """
    URL = BaseHandler.URL + '/modif_user_group'
    url = BaseHandler.url + r'/modif_user_group.*'

    oname = 'oname'
    name = 'name'

    def POST(self):
        user = session().user

        ''' 检查权限 '''
        if not user.isHavePms(UserGroup.PERMISSION_MODIF_USER_GROUP):
            return '没有 修改 用户组 信息的权限...'

        ''' 新用户组信息 '''
        newUg = web.input()

        ''' 实例化 '''
        ug = UserGroup.obj(name=newUg.oname)
        if ug is None:
            raise ValueError('用户组%s' % newUg.oname)

        ''' 改名 '''
        if newUg.name:
            ug.name = newUg.name

        ''' 获取设定的权限 '''
        pms = set([])
        for pmn, pm in UserGroup.getPermissionDic().items():
            if newUg.get(pmn) == 'on':
                pms |= pm

        ''' 重设权限 '''
        ug.setPms(pms)

        ''' 保存 '''
        ug.save()

        ''' 是否有错误 '''
        if ug.errStr:
            raise ValueError(ug.errStr)

        return '修改用户组成功'
