# -*- coding: utf-8 -*-

"""URL definitions of the application. Regex based URLs are mapped to their
class handlers.
"""

from controllers.base_handler import BaseHandler
from controllers.main_handler import (Main, Top, Left, Right, DataTable, JsCharts, Ajax, JqueryAjax)
from controllers.login_handler import Login
from controllers.logout_handler import Logout
from controllers.index_handler import Index
from controllers.manage_handler import (ManageUser, CreateUserGroup, CreateUser, ModifUser, ModifUserN, ModifUserPW, AddUG, RemoveUG, ModifUserGroup)
from controllers.sim_terminal_handler import (SimTerminalPage, SimTermLocalServer)
from controllers.static_handler import (JavaScripteHandler, CssHandler, ImageHandler)
from controllers.test_handler import Test


URLS = (
    Index.url,                                                  Index.__name__,
    Login.url,                                                  Login.__name__,
    Main.url,                                                   Main.__name__,
    Top.url,                                                    Top.__name__,
    Left.url,                                                   Left.__name__,
    Right.url,                                                  Right.__name__,
    ManageUser.url,                                             ManageUser.__name__,
    DataTable.url,                                              DataTable.__name__,
    JsCharts.url,                                               JsCharts.__name__,
    ManageUser.url,                                             ManageUser.__name__,
    CreateUserGroup.url,                                        CreateUserGroup.__name__,
    CreateUser.url,                                             CreateUser.__name__,
    ModifUser.url,                                              ModifUser.__name__,
    ModifUserN.url,                                             ModifUserN.__name__,
    ModifUserPW.url,                                            ModifUserPW.__name__,
    AddUG.url,                                                  AddUG.__name__,
    RemoveUG.url,                                               RemoveUG.__name__,
    ModifUserGroup.url,                                         ModifUserGroup.__name__,
    SimTerminalPage.url,                                        SimTerminalPage.__name__,
    SimTermLocalServer.url,                                     SimTermLocalServer.__name__,
    Logout.url,                                                 Logout.__name__,
    JavaScripteHandler.url,                                     JavaScripteHandler.__name__,
    Test.url,                                                   Test.__name__,
    CssHandler.url,                                             CssHandler.__name__,
    ImageHandler.url,                                           ImageHandler.__name__,
    Ajax.url,                                                   Ajax.__name__,
    JqueryAjax.url,                                             JqueryAjax.__name__,
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
