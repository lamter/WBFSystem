# -*- coding: utf-8 -*-

"""Default options for the application.
"""

import sys
import traceback

import web
import redis.exceptions
import redisco

reload(sys)
sys.setdefaultencoding('utf-8')

DEBUG = True


# global session


SESSION_TIMEOUT = 3600  # 1 Hour

HASH_KEY = ''
VALIDATE_KEY = ''
ENCRYPT_KEY = ''
SECRET_KEY = ''

REDIS_HOST = 'localhost'
REDIS_PW = ''
REDIS_PORT = 8911
REDIS_DB = 1

redisco.connection_setup(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
try:
    if not redisco.connection.ping():
        raise redis.exceptions.ConnectionError(u'redisco 链接失败!!!')
except redis.exceptions:
    raise redis.exceptions.ConnectionError(u'redisco 链接失败!!!')



def absolute(path):
  """Get the absolute path of the given file/folder.

  ``path``: File or folder.
  """
  import os
  PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
  return os.path.normpath(os.path.join(PROJECT_DIR, path))
