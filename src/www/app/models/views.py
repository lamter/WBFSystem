#coding=utf-8
'''
Created on 2014-10-28

@author: Shawn
'''

from .. import settings
from ..controllers import (render)
from usergroup import UserGroup
from user import User


class Views(object):
    """
    用于传递页面上各个模块的内容
    """
    def __init__(self, user=None):
        self.user = user
        if self.user == None:
            raise ValueError('模板需要一个用户对象self.user')

    def isHasAttr(self, attr):
        return hasattr(self, attr)


    def html(self, attr):
        '''
        将制定的html生成html文件保存到www.tmp下
        :param attr:
        :return:
        '''
        print '查看生成的文件: %s ' % settings.absolute('../test/test.html')
        if self.isHasAttr(attr):
            with open(settings.absolute('../test/test.html'), 'wb') as h:
                a = '%s' % getattr(self, attr)
                h.write(a)
        else:
            with open(settings.absolute('../test/test.html'), 'wb') as h:
                h.write(attr)


    def render_test(self, StaticCSSHandler):
        """
        :return:
        """

        self.test = render.test(StaticCSSHandler)



    def render_manage_user_option(self, manage_handler):
        '''
        管理用户选项
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_CREATE_USER | UserGroup.PERMISSION_CREATE_USER_GROUP | UserGroup.PERMISSION_USER_GROUP_LIST | UserGroup.PERMISSION_USER_LIST

        if not self.user.isHavePms(pms):
            ''' 拥有权限才能渲染模板 '''
            return

        self.manage_user_option = render.manage_user_option(self.user, UserGroup, manage_handler)



    def render_manage_user(self):
        '''
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_MANAGER_USER

        ''' 拥有权限才能渲染模板 '''
        if not self.user.isHavePms(pms):
            print '没有权限!!!'
            return

        ''' 管理用户选项 '''
        # self.render_manage_user_option()

        self.manage_user = render.manage_user(self.user, UserGroup, self)


    def render_modif_user(self, modifUser, ModifUserN, ModifUserPW, AddUG, RemoveUG):
        '''
        渲染修改用户信息界面
        :return:
        '''
        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_MODIF_USER

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.modif_user = render.modif_user(self.user, UserGroup, modifUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)



    def render_user_list(self, ModifUser):
        '''
        渲染 用户信息列表
        :param args:
        :return:
        '''
        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_USER_LIST

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.user_list = render.user_list(self.user, UserGroup, ModifUser, User)


    def render_user_group_list(self):
        '''
        渲染 用户组信息 列表
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_USER_GROUP_LIST

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.user_group_list = render.user_group_list(self.user, UserGroup)



    def render_create_user_group(self, CreateUserGroup):
        '''
        渲染 创建用户组界面
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_CREATE_USER_GROUP

        if not self.user.isHavePms(pms):
            return

        ''' 渲染 '''
        self.create_user_group = render.create_user_group(self.user, UserGroup, CreateUserGroup)


    def render_create_user(self, CreateUser):
        '''
        渲染 创建用户 界面
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_CREATE_USER

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.create_user = render.create_user(self.user, UserGroup, CreateUser)


    def render_modif_user_group(self, ModifUserGroup):
        '''
        渲染 修改用户组信息 界面
        :return:
        '''

        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_MODIF_USER_GROUP

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户组信息 '''
        self.modif_user_group = render.modif_user_group(self.user, UserGroup, ModifUserGroup)


    def render_refresh_log(self, queryUrl):
        """
        刷新log
        :return:
        """

        self.log_show = render.log_show(self.user, UserGroup, queryUrl)


    def render_sim_terminal_page(self, SimTermLocalServer):
        """
        渲染 伪终端的页面
        :return:
        """
        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_MODIF_USER_GROUP

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.sim_terminal_page = render.sim_terminal_page(self.user, UserGroup, SimTermLocalServer)


    def render_sim_term_local_server(self, querUrl, simTermTag, LocalExecPython):
    # def render_sim_term_local_server(self):
        """
        渲染 本地进程的终端页面
        :return:
        """
        ''' 设置这个模块相关的权限 '''
        pms = UserGroup.PERMISSION_SIM_TERM_LOCAL_SERVER

        if not self.user.isHavePms(pms):
            return

        ''' 渲染用户信息 '''
        self.sim_term_local_server = render.sim_term_local_server(self.user, UserGroup, self, querUrl, simTermTag, LocalExecPython)
        # self.sim_term_local_server = render.sim_term_local_server(self.user, UserGroup, self)


    def render_terminal_output(self, queryUrl, term_title):
        """
        虚拟终端的输出界面
        :param term_output: [server, ...]
        >>> server = object # server 需要以下的属性
        >>> server.term_title
        >>> server.term_output
        :return:
        """

        ''' 渲染用户信息 '''
        self.terminal_output = render.terminal_output(self.user, UserGroup, queryUrl, term_title)



    def render_terminal_input(self, LocalExecPython):
        """
        虚拟终端 输入界面
        :return:
        """

        ''' 渲染用户信息 '''
        self.terminal_input = render.terminal_input(self.user, UserGroup, LocalExecPython)


    def render_real_time_term(self, term_name):
        """
        实时终端
        :return:
        """
        self.real_time_term = render.real_time_term(term_name)
