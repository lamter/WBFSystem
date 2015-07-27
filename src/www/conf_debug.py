# -*- coding: utf-8 -*-
"""
Created on 2015-07-27

@author: Shawn

"""

import sys
import logging

import log
from app import settings

settings.DEBUG = True

''' 在调试中不需要输出到日志，直接指向 '''
settings.loglevel = logging.INFO
# settings.log.close()
# settings.log = 'default'
