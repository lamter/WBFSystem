#coding=utf-8
'''
Created on 2015-02-05

@author: Shawn
'''

import unittest
import random

import web
import redis
import redisco

from src.www.app.controllers import session
from src.www.app.tools.web_session import Initializer
from src.www.app import (models, controllers, settings)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror, verify_session)
from src.www.app.urls import (URLS, HANDLER)
from src.www.app.tools.app_processor import (header_html, notfound, internalerror)
from src.www.app.models.user import User
from src.www.app.models.usergroup import UserGroup
from src.www.app.models.views import Views
from src.www.app.models.term_server import TerminalServer
from src.www.app.controllers.manage_handler import (ManageUser, ModifUserN, ModifUserPW, AddUG, RemoveUG)
from src.www.app.controllers.login_handler import Login
from src.www.app.controllers.sim_terminal_handler import (SimTermLocalServer)

def suite():
    testSuite1 = unittest.makeSuite(TestSimTerminal, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestSimTerminal(unittest.TestCase):
    '''
    测试伪终端
    '''
    def setUp(self):
        '''
        :return:
        '''

        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        settings.REDIS_PORT = 8911
        # settings.REDIS_DB = 0

        ''' redisco连接 '''
        settings.rd = redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        # ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 启动服务 '''
        web.config.debug = settings.DEBUG

        self.appM = web.application(URLS, HANDLER, autoreload=False)
        application = self.appM.wsgifunc()

        self.appM.notfound = notfound
        self.appM.internalerror = internalerror
        self.appM.add_processor(web.loadhook(header_html))

        session.init(web.session.Session(self.appM, web.session.DiskStore('sessions'), initializer=Initializer(
                                                                                                              User=models.user.User,
                                                                                                              UserGroup=models.usergroup.UserGroup,
                                                                                                              BanLogin=controllers.login_handler.BanLogin,
                                                                                                              settings=settings,
                                                                                                              session=session,
                                                                                                              ))
        )

        ''' 校验session, 添加到app的 processor 流程中，顺序需要在 session初始化之后 '''
        self.appM.add_processor(web.loadhook(verify_session))
        ''' 初始化 html 头, 添加到app的 processor 流程中 '''
        self.appM.add_processor(web.loadhook(header_html))

        web.config.session_parameters['cookie_name'] = 'webpy_session_id'
        web.config.session_parameters['cookie_domain'] = None
        web.config.session_parameters['timeout'] = 10
        web.config.session_parameters['ignore_expiry'] = True
        web.config.session_parameters['ignore_change_ip'] = False
        web.config.session_parameters['secret_key'] = 'akdnA0FJsdJFLSlvno92'
        web.config.session_parameters['expired_message'] = 'Session expired'


    def test_render_sim_terminal_page(self):
        '''
        测试 修改用户信息界面
        :return:
        '''
        user = User.obj(username=User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(username=User.rootAccount)

        views = Views(user)
        views.render_sim_terminal_page(SimTermLocalServer)
        views.html('sim_terminal_page')


    def test_render_termial_output(self):
        """
        :return:
        """
        term_server = TerminalServer()
        term_server.term_title = '测试终端输出用'
        term_server.term_output = '测试终端输出的内容'

        term_output = [term_server, term_server]

        user = User.obj(username=User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(username=User.rootAccount)

        views = Views(user)
        views.render_terminal_output(term_output)
        views.html('terminal_output')

    def test_render_sim_term_local_server(self):
        """
        :return:
        """
        term_server = TerminalServer()
        term_server.term_title = '本地服务进程'
        term_server.term_output = '测试终端输出的内容'

        term_output = [term_server, term_server]

        user = User.obj(username=User.rootAccount)
        if not user:
            User.createRoot()
            user = User.obj(username=User.rootAccount)

        views = Views(user)
        views.render_terminal_output(term_output)
        views.render_terminal_input()

        views.render_sim_term_local_server(SimTermLocalServer, term_server)
        views.html('sim_term_local_server')


    def test_SimTermLocalServer_GET(self):
        """
        测试 打开本地服务交互终端
        :return:
        """

        user = User.obj(username=User.rootAccount)
        if not user:
            User.createRoot()

        settings.debug_user = user

        ''' 渲染 '''
        v = Views(user)
        v.html(self.appM.request(localpart=SimTermLocalServer.URL, method='GET').data)


    def test_SimTermLocalServer_POST(self):
        """
        测试 打开本地服务交互终端
        :return:
        """

        user = User.obj(username=User.rootAccount)
        if not user:
            User.createRoot()

        settings.debug_user = user
        data = {
            SimTermLocalServer.python_code: "非unicode中文: 逗比，unicode中文：u'这是unicode'",
        }

        ''' 渲染 '''
        v = Views(user)
        v.html(self.appM.request(localpart=SimTermLocalServer.URL, data=data, method='POST').data)



    def execuPython(self):
        """

        :return:
        """