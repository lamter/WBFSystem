# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

    伪终端，用于直接直接使用代码同服务进程交互

"""
import os

import web

from . import session
from base_handler import *
from ..models.views import Views
from ..models.term_server import TerminalServer
from ..models.pm import PM



class SimTerminalPage(BaseHandler):
    """
    伪终端
    """
    URL = BaseHandler.URL + '/sim_terminal_page'
    url = BaseHandler.url + r'/sim_terminal_page.*'

    def GET(self):
        """
        主页面
        :return:
        """

        user = session().user

        views = Views(user)

        ''' 渲染管理用户选项 '''
        views.render_sim_terminal_page(SimTermLocalServer)

        return views.sim_terminal_page



class SimTermLocalServer(BaseHandler):
    """
    本地服务进程的终端
    """
    URL = BaseHandler.URL + '/sim_term_local_server'
    url = BaseHandler.url + r'/sim_term_local_server.*'

    python_code = 'python_code'

    def GET(self):
        """
        打开本地进程的伪终端页面
        :return:
        """
        if not session().user.isHavePms(PM.PERMISSION_SIM_TERM_LOCAL_SERVER):
            return '没有 使用 游戏服务器进程终端 的权限...'

        ''' 终端 '''
        termLocalServer = TerminalServer()
        termLocalServer.term_title = '本地服务进程'
        termLocalServer.logfile = settings.logfile()

        ''' 获得日志内容 '''
        # termLocalServer.getLogText()

        ''' 生成用于显示的界面 '''
        term_output = [termLocalServer]
        views = Views(session().user)
        views.render_terminal_output(term_output)
        views.render_terminal_input()
        views.render_sim_term_local_server(SimTermLocalServer)
        return views.sim_term_local_server


    def POST(self):
        """
        提交 python 代码到本地进程执行，并放回Log结果
        :return:
        """
        if not session().user.isHavePms(PM.PERMISSION_SIM_TERM_LOCAL_SERVER):
            return '没有 使用 游戏服务器进程终端 的权限...'

        exe = web.input(_unicode=True)

        ''' 终端 '''
        termLocalServer = TerminalServer()
        termLocalServer.term_title = '本地服务进程'
        termLocalServer.logfile = settings.logfile()

        ''' 执行 python 代码 '''
        termLocalServer.execPythonCode(exe.python_code)

        # ''' 获得日志内容 '''
        # termLocalServer.getLogText()

        ''' 生成用于显示的界面 '''
        term_output = [termLocalServer]
        views = Views(session().user)
        views.render_terminal_output(term_output)
        views.render_terminal_input()
        views.render_sim_term_local_server(SimTermLocalServer)
        return views.sim_term_local_server