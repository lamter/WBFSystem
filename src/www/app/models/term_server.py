#coding=utf-8
'''
Created on 2015-02-05

@author: Shawn

用于伪终端的 module
'''


class TerminalServer(object):
    """
    用于伪终端的server
    """
    def __init__(self, host='localhost', title='未配置终端标签'):
        self.host = host
        self.term_title = title
        self.term_output = ''

