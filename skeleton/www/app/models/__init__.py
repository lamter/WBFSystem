#coding=utf-8
'''
Created on 2014-10-27

@author: Shawn
'''


from user import User


class Init(object):


    def __call__(self, *args, **kwargs):
        '''
        :param args:
        :param kwargs:
        :return:
        '''

        ''' 初始化root用户 '''
        self.root()


    def root(self):
        '''
        如果初始化出用户后没有超级用户，那么使用默认配置初始化出超级用户
        :return:
        '''

        root = User.obj(User.rootAccount)

        if root is None:
            ''' 如果还没有root用户 '''
            ''' 不存在root用户，重新生成 '''
            root = User.createRoot()

        else:
            ''' 如果已经有root用户了, 初始化root用户组 '''
            root.initRootUg()

        root.save()


init = Init()


