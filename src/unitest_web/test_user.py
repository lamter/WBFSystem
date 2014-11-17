#coding=utf-8
'''
Created on 2014-10-27

@author: Shawn
'''

import unittest
import traceback

import redis
import redisco

from src.www import settings
from src.www.app.models.user import User
from src.www.app.models import user
from src.www.app.models import init

from src.www.app.models.usergroup import UserGroup


def suite():
    testSuite1 = unittest.makeSuite(TestUser, "test")
    alltestCase = unittest.TestSuite([testSuite1, ])
    return alltestCase


class TestUser(unittest.TestCase):
    '''
    '''
    def setUp(self):
        '''
        :return:
        '''

        ''' 配置测试用的redis配置信息  '''
        settings.REDIS_HOST = "localhost"
        settings.REDIS_PORT = 8911
        settings.REDIS_DB_NUM = 0

        ''' redisco连接 '''
        settings.rd = redisco.connection_setup(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)

        ''' 额外的redis连接 '''
        self.redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


    def tearDown(self):
        # return
        print u'清空了数据库%s' % settings.REDIS_DB
        self.redis.flushdb()


    def test_createUser(self):
        '''
        :return:
        '''
        self.redis.flushdb()

        username, password = 'shawn', '123456'
        u = User.createNewUser(username, password)

        print u'生成用户完毕...'
        u = User.obj(username)
        if not u.is_valid:
            raise ValueError(u'生成玩家失败!!!')
        print u'生成用户成功...'


    def test_objNoUser(self):
        '''
        获取一个不存在的用户
        :return:
        '''
        self.redis.flushdb()

        username = 'adfgagdsdfadsg'
        u = User.obj(username)
        if u is not None:
            raise ValueError(u'不存在的用户不是None')



    def test_createSameNameUer(self):
        '''
        尝试生成同名用户
        :return:
        '''
        self.redis.flushdb()
        username, password = 'aaa111', 'bbb222'
        u = User.createNewUser(username, password)
        try:
            u = User.createNewUser(username, password)
        except:
            errInfo = traceback.format_exc()
            if user.NEW_ACCOUNT_ERR_NOT_UNIQUE in errInfo:
                print u'不能创建重名账户...'
            else:
                raise errInfo



    def test_nonstandardPW(self):
        '''
        非标注密码
        :return:
        '''
        self.redis.flushdb()

        ''' 密码过长 '''
        un = 'Shawn'
        pw = ''.join(['1' for i in range(user.ACCOUNT_MAX_SIZE+1)])
        try:
            err = u'能够生成过 长 的密码!!'
            u = User.createNewUser(un, pw)
            raise ValueError(err)
        except :
            errInfo = traceback.format_exc()
            if err in errInfo:
                raise ValueError(errInfo)


        un = 'Shawn'
        pw = ''.join(['1' for i in range(user.ACCOUNT_MIN_SIZE-1)])
        try:
            err = u'能够生成过 短 的密码!!'
            u = User.createNewUser(un, pw)
            raise ValueError(err)
        except:
            errInfo = traceback.format_exc()
            if err in errInfo:
                raise ValueError(errInfo)




    def test_creatRoot(self):
        '''
        创建root用户
        :return:
        '''
        self.redis.flushdb()

        root = User.createRoot()
        print 'root name ->', root.username
        rootUg = root.getUserGroupByName(User.rootAccount)

        print rootUg.pms
        print root.userGroups

        root.save()

        root = User.obj(User.rootAccount)
        rootUg = root.getUserGroupByName(UserGroup.rootGroup)

        print rootUg.pms
        print root.userGroups



    def test_userAll(self):
        '''
        实例化所有角色
        :return:
        '''
        init()
        users = User.all()
        print len(users)
        for u in users:
            print u.username


    def test_addUserGroup(self):
        '''
        测试 给用户添加用户组
        :return:
        '''

        ''' 清空数据库 '''
        self.redis.flushdb()

        ''' 生成测试用户 '''
        un = u'test01'
        pw = u'123456'
        user = User.createNewUser(un, pw)

        ''' 生成测试用户组 '''
        ugn = u'testUG01'
        ug = UserGroup.createNewUserGroup(ugn)
        print u'ug->', id(ug), ug

        ''' 添加用户组 '''
        user.addUserGroup(ug)
        ug = UserGroup.obj(ugn)
        print 'ug->', id(ug), ug

        ''' 添加用户组 '''
        if ug not in user.userGroups:
            raise ValueError(u'添加  用户组失败')

        ''' 移除用户组 '''
        user.removeUserGroup(ug)
        if ug in user.userGroups:
            raise ValueError(u'移除 用户组失败')