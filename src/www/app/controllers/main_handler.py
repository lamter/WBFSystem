# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import (render, session)
from base_handler import *
from logout_handler import Logout
from manage_handler import (ManageUser)
from sim_terminal_handler import SimTerminalPage
from ..models.views import Views
from ..models.usergroup import UserGroup


class Main(BaseHandler):

    URL = BaseHandler.URL + '/main'
    url = BaseHandler.url + r'/main'

    def GET(self):
        """
        主页面
        :return:
        """
        try:
            user = session().user
        except:
            ''' 报错就弹到登录界面, 表示没有登录, 进行重新登录 '''
            from login_handler import Login
            return render.login('未登录', Login)
        # import time
        # b = time.time()
        # time.sleep(5)
        # e = time.time()
        # return u'%s to %s' % (str(b), str(e))

        # views = Views(user)
        #
        # ''' 用户管理选择 '''
        # views.render_manage_user_option(ManageUser)
        #
        # ''' 用户管理选择 '''
        # return render.main(user,
        #                    UserGroup,
        #                    views,
        #                    ManageUser,
        #                    ServerPage,
        #                    TableDataPage,
        #                    SimTerminalPage,
        #                    Logout,
        #                    OperatorPage,
        #                    )

        return render.main(user, Top, Left, Right)


class Top(BaseHandler):

    URL = BaseHandler.URL + '/top'
    url = BaseHandler.url + r'/top'

    def GET(self):
        """
        top页面
        :return:
        """

        user = session().user

        ''' top页面的数 '''
        return render.top(user, Logout)


class Left(BaseHandler):

    URL = BaseHandler.URL + '/left'
    url = BaseHandler.url + r'/left'

    def GET(self):
        """
        left页面
        :return:
        """

        user = session().user

        views = Views(user)

        ''' 用户管理选择 '''
        views.render_manage_user_option(ManageUser)

        ''' left页面的数 '''
        return render.left(user,
                           UserGroup,
                           views,
                           ManageUser,
                           DataTable,
                           JsCharts
                           )


class Right(BaseHandler):

    URL = BaseHandler.URL + '/right'
    url = BaseHandler.url + r'/right'

    def GET(self):
        """
        右边主页面
        :return:
        """

        user = session().user

        ''' right页面的数 '''
        return render.right(user)


class DataTable(BaseHandler):

    URL = BaseHandler.URL + '/dataTable'
    url = BaseHandler.url + r'/dataTable'

    def GET(self):
        """
        数据列表页面
        :return:
        """
        user = session().user

        ''' datatable页面的数 '''
        return render.dataTable(user)


class JsCharts(BaseHandler):

    URL = BaseHandler.URL + '/jsCharts'
    url = BaseHandler.url + r'/jsCharts'


    def GET(self):
        """
        数据列表页面
        :return:
        """
        user = session().user

        ''' jsChart页面的数 '''
        return render.js_charts(user)
