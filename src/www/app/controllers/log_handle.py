# -*- coding: utf-8 -*-

"""
Created on 2015-09-11

@author: Shawn


"""

import json
import traceback

import web

from . import (render, session)
from .. import settings
from base_handler import BaseHandler
from ..models.usergroup import UserGroup


class QueryLogCache(BaseHandler):
    """
    查询日志缓存
    """
    URL = BaseHandler.URL + '/query_log_cache'
    url = BaseHandler.url + r'/query_log_cache'

    def GET(self):
        """
        直接使用最新的一行日志来作为标签
        :return:
        """
        user = session().user

        if not user.isHavePms(UserGroup.PERMISSION_SIM_TERM_LOCAL_SERVER):
            return '没有 查看 本地伪终端 的权限...'

        dic = web.input()
        tag = dic.get('logTag')
        num = dic.get('num')
        if not tag:
            tag = None
        if num:
            num = int(num)
        else:
            num = 100

        log = []
        with open(settings.LOG, 'rb') as f:
            for t in f:
                if tag and tag in t:
                    ''' 符合标签, 重新开始记录 '''
                    log = []
                ''' 去掉末尾换行符 '''
                log.append(t.strip('\n'))

        ''' 截取需要的长度 '''
        log = log[-num:]

        ''' 标签 '''
        if log:
            newTag = log[-1]
        else:
            newTag = None

        response = {
            'tag': newTag,
            'log': log,

        }

        return json.dumps(response)






