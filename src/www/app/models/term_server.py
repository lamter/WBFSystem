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
    def __init__(self):
        self.host = ''
        self.term_title = ''
        self.term_output = ''

