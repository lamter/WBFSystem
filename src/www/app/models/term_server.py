#coding=utf-8
'''
Created on 2015-02-05

@author: Shawn

用于伪终端的 module
'''


import sys
import os
import StringIO
import contextlib


class TerminalServer(object):
    """
    用于伪终端的server
    """
    def __init__(self):
        self.host = 'localhost'
        self.term_title = '未设置终端标签'
        self.term_output = ''
        self.logfile = ''
        # self.loglines = 50      # 读取多少行日志


    def getLogText(self):
        """
        根据 self.logfile 获取输出内容
        :return:
        """
        if not os.path.exists(self.logfile):
            self.term_output = '指定路径没有logfile文件'
            return

        logText = ''
        with open(self.logfile, 'rb') as lf:
            ''' 获得最新的 self.loglines 行 '''
            for i in lf.readlines()[-self.loglines:]:
                logText += i

        ''' 替换换行符 '''
        self.term_output = logText.replace('\n', "<br/>")


    def execPythonCode(self, pythonCode):
        """
        执行 python 代码，并获得输出结果
        :param pythonCode:
        :return:
        """
        with stdoutIO() as s:
            exec pythonCode

        self.term_output = s.getvalue()


@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO.StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old