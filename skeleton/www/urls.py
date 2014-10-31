# -*- coding: utf-8 -*-

"""URL definitions of the application. Regex based URLs are mapped to their
class handlers.
"""

from app.controllers.login_handler import Login
from app.controllers.index_handler import Index

URLS = (
    r'^/',                  Index.__name__,
    r'/login',              Login.__name__,
)


HANDLER = {}

for i, name in enumerate(URLS):
    if (i+1) % 2  == 0:
        cls = eval(name)
        HANDLER[name] = cls
