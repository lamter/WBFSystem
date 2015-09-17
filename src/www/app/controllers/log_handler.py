# coding:utf-8
"""
Created on 2015/9/10

描述

@author: Cordial
"""

import random
import json

import web

from . import (render, session)
from .. import settings
from ..models.views import Views
from ..models.usergroup import UserGroup
from base_handler import BaseHandler


class TestRefreshLog(BaseHandler):
    """
    log刷新
    """
    URL = BaseHandler.URL + '/test_refresh_log'
    url = BaseHandler.url + r'/test_refresh_log.*'

    def GET(self):

        import requests
        url = 'http://localhost:23001/bpm_http_request'

        dic = {
            'type': 20004,
            'tag': web.input().get('tag'),
            'num': 100,
        }
        data = json.dumps(dic)
        response = requests.get(url, data=data)
        # print 161616
        # for k, v in json.loads(response.text).items():
        #     print k,':', v

        return response.text

        # return json.dumps({'log': ['log--->%s' % random.randint(10, 1000), 'log--->%s' % random.randint(10, 1000)]})


class TestShowLog(BaseHandler):
    """
    显示log
    """
    URL = BaseHandler.URL + '/test_show_log'
    url = BaseHandler.url + r'/test_show_log.*'

    def GET(self):

        user = session().user

        views = Views(user)

        ''' 渲染管理用户选项 '''
        # url = TestRefreshLog.URL
        url = QueryLocalLogCache.URL
        views.render_refresh_log(url)

        return views.log_show


class QueryLocalLogCache(BaseHandler):
    """
    查询日志缓存
    """
    URL = BaseHandler.URL + '/query_loacl_log_cache'
    url = BaseHandler.url + r'/query_loacl_log_cache.*'

    def GET(self):
        """
        直接使用最新的一行日志来作为标签
        :return:
        """
        user = session().user
        if not user.isHavePms(UserGroup.PERMISSION_SIM_TERM_LOCAL_SERVER):
            return '没有 查看 本地伪终端 的权限...'

        tag, num = self.getWebInput()

        log, lastLine = self.getLog(tag)

        ''' 截取需要的长度 '''
        log = log[-num:]

        ''' 标签 '''
        if log:
            newTag = log[-1]
        else:
            newTag = lastLine

        response = {
            'tag': newTag,
            'log': log,

        }

        return json.dumps(response)


    def getWebInput(self):
        """

        :return:
        """

        dic = web.input()
        tag = dic.get('tag')
        num = dic.get('num')

        if not tag:
            tag = None
        if num:
            num = int(num)
        else:
            num = 108
        return tag, num


    def getLog(self, tag):
        log = []
        lastLine = None
        try:
            with open(settings.LOG, 'rb') as f:
                for t in f:
                    if tag and tag in t:
                        ''' 符合标签, 重新开始记录 '''
                        log = []
                        lastLine = t
                        continue
                    ''' 去掉末尾换行符 '''
                    t = t.strip('\n')
                    log.append(t)
                    lastLine = t
        except IOError:
            pass
        finally:
            return log, lastLine