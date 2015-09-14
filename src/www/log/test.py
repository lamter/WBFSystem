# -*- coding: utf-8 -*-

"""
Created on 2015-09-14

@author: Shawn


"""


import time

with open('wbfs.log', 'rb') as f:
    # a = []
    # for i in f:
    #     print i
    # b = f.xreadlines()
    # print type(b)
    print f.readlines()


a = 'adf\nasdf\n'
print [a.strip('\n')]


