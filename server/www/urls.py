# -*- coding: utf-8 -*-

"""URL definitions of the application. Regex based URLs are mapped to their
class handlers.
"""

from app.controllers.login_handler import Login
from app.controllers.index_handler import Index
from app.controllers.main_handler import Main
from app.controllers.manage_handler import (ManageUser)


URLS = (
    Index.url,                  Index.__name__,
    Login.url,                  Login.__name__,
    Main.url,                   Main.__name__,
    ManageUser.url,             ManageUser.__name__,
)

HANDLER = {}

for i, name in enumerate(URLS):
    if (i+1) % 2 == 0:
        cls = eval(name)
        HANDLER[name] = cls
