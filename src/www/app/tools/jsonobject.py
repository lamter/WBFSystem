# -*- coding: utf-8 -*-

"""
Created on 2015-10-21

@author: Shawn

"""

import json

class JsonObject(object):
    """
    一个模仿 js 的 json object
    """
    def __init__(self):

        self.dic = {}

        self.__setattr__ = self._setattr


    def _setattr(self, name, value):
        """

        :param name:
        :param value:
        :return:
        """
        json.dumps({name, value})

        self.dic[name] = value

        object.__setattr__(self, name, value)