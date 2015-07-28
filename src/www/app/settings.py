# -*- coding: utf-8 -*-

"""Default options for the application.
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import traceback
import platform
import logging

import web
import redis.exceptions
import redisco

''' 日志 '''
log = './log/wsgi.log'
loglevel = logging.ERROR
IS_LOG_TO_FILE = True

DEBUG = False
# DEBUG = True

IS_UNITTEST = False
# IS_UNITTEST = True


# global session

''' 并发数 '''
ASYNC = 1000

WEB_LISTEN_PORT = 8080

SESSION_TIMEOUT = 3600  # 1 Hour

HASH_KEY = ''
VALIDATE_KEY = ''
ENCRYPT_KEY = ''
SECRET_KEY = ''

REDIS_HOST = 'localhost'
REDIS_PW = ''
REDIS_PORT = 8911
REDIS_DB = 1

try:
    redisco.connection_setup(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    if not redisco.connection.ping():
        raise redis.exceptions.ConnectionError('redisco 链接失败!!\n请检查 redis 服务是否启动')
except redis.exceptions.ConnectionError:
    raise redis.exceptions.ConnectionError('redisco 链接失败!!\n请检查 redis 服务是否启动')



def absolute(path):
  """Get the absolute path of the given file/folder.

  ``path``: File or folder.
  """
  import os
  PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
  return os.path.normpath(os.path.join(PROJECT_DIR, path))


# import os
''' 将skeleton/www/app加入import 路径 '''
# print absolute('app')
if absolute('app') not in sys.path:
    sys.path.insert(0, absolute('app'))

def logfile():
    appPath = os.path.split(__file__)[0]
    wwwPath = os.path.split(appPath)[0]
    logfile = os.path.join(wwwPath, 'log/wbfs.log')
    return logfile


def setSessionParameters(session_parameters):
    """
    设置 web.config.session_parameters 的参数
    :param session_parameters:
    :return:
    """
    session_parameters['cookie_name'] = 'webpy_session_id'
    session_parameters['cookie_domain'] = None
    session_parameters['timeout'] = SESSION_TIMEOUT
    session_parameters['ignore_expiry'] = True
    session_parameters['ignore_change_ip'] = False
    session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
    session_parameters['expired_message'] = 'Session expired'


def isMac():
    return platform.system() == 'Darwin'