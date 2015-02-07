# -*- coding: utf-8 -*-

"""URL definitions of the application. Regex based URLs are mapped to their
class handlers.
"""

from controllers.login_handler import Login
from controllers.index_handler import Index
from controllers.main_handler import Main
from controllers.manage_handler import (ManageUser, CreateUserGroup, CreateUser, ModifUser, ModifUserN, ModifUserPW, AddUG, RemoveUG, ModifUserGroup)
from controllers.sim_terminal_handler import (SimTerminalPage, SimTermLocalServer)


URLS = (
    Index.url,                  Index.__name__,
    Login.url,                  Login.__name__,
    Main.url,                   Main.__name__,
    ManageUser.url,             ManageUser.__name__,
    CreateUserGroup.url,        CreateUserGroup.__name__,
    CreateUser.url,             CreateUser.__name__,
    ModifUser.url,              ModifUser.__name__,
    ModifUserN.url,             ModifUserN.__name__,
    ModifUserPW.url,            ModifUserPW.__name__,
    AddUG.url,                  AddUG.__name__,
    RemoveUG.url,               RemoveUG.__name__,
    ModifUserGroup.url,         ModifUserGroup.__name__,
    SimTerminalPage.url,        SimTerminalPage.__name__,
    SimTermLocalServer.url,     SimTermLocalServer.__name__,
)
# for i,u in enumerate(URLS):
#     print u, '\t',
#     if (i+1) % 2 == 0:
#         print


HANDLER = {}

for i, name in enumerate(URLS):
    if (i+1) % 2 == 0:
        cls = eval(name)
        HANDLER[name] = cls
