#coding=utf-8
'''
Created on 2015-07-24

@author: Shawn
'''

import json
import datetime

from gevent import Greenlet, sleep
from redisco import models

import orm



class BaseTask(Greenlet):
    '''
    用于添加到主循环中的任务的父类
    '''
    #
    # TYPE_BACKUP_GAME_MYSQL = '0'
    #
    # _type = models.Attribute(required=True)
    #
    # _execute_time = models.DateTimeField()
    #
    # _valid = models.BooleanField(default=False)

    # @property
    # def type(self):
    #     return self._type



    # def validate(self):
    #     '''
    #     :return:
    #     '''
    #     errss = ''
    #     for errs in self._errors:
    #         err = " ".join(errs)
    #         print err
    #         errss += err
    #     if self._errors:
    #         print 'are the reasons to '
    #     return errss


    def _run(self):
        """

        :return:
        """
        self.running = True
        print u'添加测试任务成功'
        interval = datetime.timedelta(seconds=1)

        pre = datetime.datetime.now()
        while self.running:
            now = datetime.datetime.now()
            delta = now - pre
            if delta > interval:
                # print 'time', now
                pre = now
            sleep(0.5)


