#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''

import json
from redisco import models
import orm

Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()




class UserGroup(orm.RediscoModle):
    '''
    要存库的数据类型
    '''
    ''' 用户权限枚举=> '''

    ''' 登录 '''
    PERMISSION_LOG_IN = 1 << 0
    PERMISSION_CREATE_USER_GROUP = 1 << 1
    PERMISSION_CREATE_USER = 1 << 2
    PERMISSION_USER_LIST = 1 << 3
    PERMISSION_USER_GROUP_LIST = 1 << 4

    ''' <=用户权限枚举 '''

    ''' 超级用户组 '''
    rootGroup = 'root'

    uid = models.IntegerField(required=True, unique=True)
    name =models.Attribute(required=True, unique=True)
    permissions = models.IntegerField(default=0)
    # users = models.ListField(target_type=baseuser.User)


    @property
    def pms(self):
        return self.permissions


    @classmethod
    def getAllPms(cls):
        '''
        获得全权限
        :return:
        '''
        allPms = 0
        for pm in cls.getPermissionDic().values():
            allPms |= pm
        return allPms



    def validate(self):
        '''
        :return:
        '''
        errss = u''
        for errs in self._errors:
            err = u" ".join(errs)
            print err
            errss += err
        if self._errors:
            print u'are the reasons to '
        return errss



    @classmethod
    def createNewUserGroup(cls, name=None, permissions=None):
        '''
        创建新的用户组
        :return:
        '''
        serverdata.globa.counter.incr("userGroup")
        uid = serverdata.globa.counter.userGroupUid

        if name is None:
            name = u'用户组%d' % uid

        userGroup = UserGroup(uid=uid, name=name)

        ''' 配置用户组权限 '''
        if permissions is None:
            userGroup.permissions = cls.PERMISSION_LOG_IN
        else:
            userGroup.permissions = permissions


        if userGroup.is_valid() is not True:
            raise ValueError(u'创建用户组失败!!')

        # ''' 创建有效 '''
        # serverdata.globa.userGroupDic[uid] = userGroup

        ''' 存库 '''
        userGroup.save()

        # ''' 添加到用户组列表 '''
        # serverdata.globa.userGroupDic[userGroup.uid] = userGroup

        return userGroup



    @classmethod
    def getPermissionDic(cls):
        '''
        获得权限的字典{属性名: 权限}
        :return:
        '''
        dic = {}
        for PM in dir(cls):
            if "PERMISSION_" == PM[:len("PERMISSION_")]:
                dic[PM] = getattr(cls, PM)

        return dic


    def addPermissions(self, permissions):
        '''
        给用户组添加权限
        :param permission: 必须以 UserGroup.PERMISSION_* 来传递
        :return:
        '''
        # for pm in self.__class__.getPermissionDic().values():
        #     if not permissions & pm:
        #         effInfo = u'用户组: %s设定权限失败!!非法的权限 %d !!!' % (self.name, permissions)
        #         raise ValueError(effInfo)
        self.permissions |= permissions


    def setPermissions(self, permissions):
        '''
        直接将用户组的权限置为指定的权限
        :param permissions:
        :return:
        '''
        self.permissions = permissions




    def removePermissions(self, permissions):
        '''
        给用户组减少权限
        :param permission:
        :return:
        '''
        # if permissions not in self.__class__.getPermissionDic().values():
        #     effInfo = u'用户组: %s设定权限失败!!非法的权限 %d !!!' % (self.name, permissions)
        #     raise ValueError(effInfo)

        ''' 先授权，在卸权。因为计算算法的原因，所以这么做 '''
        self.addPermissions(permissions)
        self.permissions -= permissions
        self.save()


    def isHavePms(self, permissions):
        '''
        该用户组是否有某种权限
        :param permission:
        :return: bool
        '''
        return permissions & self.pms



    @classmethod
    def createRootGroup(cls):
        '''
        生成root用户组
        :return:
        '''

        ''' root 用户组拥有全部权限 '''
        ug = UserGroup.createNewUserGroup(UserGroup.rootGroup, cls.getAllPms())
        serverdata.globa.userGroupDic.pop(ug.uid)

        return ug



