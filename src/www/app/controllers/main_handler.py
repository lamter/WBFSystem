# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn

This module contains the main handler of the application.
"""

import traceback

import web

from . import session
from base_handler import *
from manage_handler import (ManageUser)
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

        print 333333333333
        print 'id(session())->', id(session())

        user = session().user


        views = Views(user)

        ''' 渲染管理用户选项 '''
        views.render_manage_user_option(ManageUser)

        ''' 用户管理选择 '''
        return render.main(user, UserGroup, views, ManageUser)


