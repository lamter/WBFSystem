# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

    伪终端，用于直接直接使用代码同服务进程交互

"""


from . import session
from base_handler import *
from ..models.views import Views


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

    def GET(self):
        """
        打开本地进程的伪终端页面
        :return:
        """

        user = session().user

        ''' 获得日志内容 '''

        return '未完成'






