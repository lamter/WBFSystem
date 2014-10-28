# -*- coding: utf-8 -*-

"""Default options for the application.
"""

import web
import redisco
DEBUG = False

session = None

SESSION_TIMEOUT = 3600  # 1 Hour

HASH_KEY = ''
VALIDATE_KEY = ''
ENCRYPT_KEY = ''
SECRET_KEY = ''

REDIS_HOST = 'localhost'
REDIS_PW = ''
REDIS_PORT = 8911
REDIS_DB = 1

rd = redisco.connection_setup(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def absolute(path):
  """Get the absolute path of the given file/folder.

  ``path``: File or folder.
  """
  import os
  PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
  return os.path.normpath(os.path.join(PROJECT_DIR, path))
