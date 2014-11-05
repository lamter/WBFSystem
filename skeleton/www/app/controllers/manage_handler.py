# -*- coding: utf-8 -*-

"""
Created on 2014-10-28

@author: Shawn



This module contains the main handler of the application.
"""

import traceback

import web

import skeleton.www.app as app
from base_handler import *
from skeleton.www.app.models.views import Views
from skeleton.www.app.models.user import User
from skeleton.www.app.models.usergroup import UserGroup


