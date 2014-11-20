#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''

import json

from redisco import models

from counter import Counter
import orm


Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()


class UserGroup(orm.RediscoModle):
    '''
    要存库的数据类型
    '''
    ''' 用户权限枚举=> '''

    ''' 登录权限比较特殊 '''
    PERMISSION_BAN_LOGIN = 1 << 0

    ''' 其他权限 '''

    ''' 创建用户组 '''
    PERMISSION_CREATE_USER_GROUP = 1 << 1

    ''' 创建用户 '''
    PERMISSION_CREATE_USER = 1 << 2

    ''' 查看用户列表 '''
    PERMISSION_USER_LIST = 1 << 3

    ''' 创建用户组 '''
    PERMISSION_USER_GROUP_LIST = 1 << 4

    ''' 修改用户信息 '''
    PERMISSION_MODIF_USER = 1 << 5

    ''' 修改 用户组 信息 '''
    PERMISSION_MODIF_USER_GROUP = 1 << 6

    ''' 管理用户信息页面 '''
    PERMISSION_MANAGER_USER = 1 << 7


    ''' 以 PERMISSION_* 的形式来命名变量 '''

    ''' <=用户权限枚举 '''

    ''' 超级用户组 '''
    rootGroup = u'root'

    # uid = models.IntegerField(required=True, unique=True)
    name =models.Attribute(required=True, unique=True)
    permissions = models.IntegerField(default=0)
    # users = models.ListField(target_type=baseuser.User)


    @classmethod
    def all(cls):
        '''
        获取所有用户组
        :return:
        '''
        return cls.objects.filter().all().exclude(name=cls.rootGroup)


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


    def getPmsName(self):
        '''
        获得所持有的权限名
        :return:
        '''
        pmsName = []
        for pmn, pm in self.getPermissionDic().items():
            if self.isHavePms(pm):
                pmsName.append(pmn)
        return pmsName


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
    def createNewUserGroup(cls, name, permissions=None):
        '''
        创建新的用户组
        :return:
        '''
        userGroup = UserGroup(name=name)

        ''' 配置用户组权限 '''
        if permissions is None:
            # userGroup.permissions = cls.PERMISSION_LOG_IN
            userGroup.permissions = 0
        else:
            userGroup.permissions = permissions

        if not userGroup.is_valid():
            raise ValueError(userGroup.errors)

        ''' 设置用户组id和用户组名 '''
        counter = Counter.obj()
        counter.incr(Counter.userGroup)
        userGroup.id = counter.ugid

        ''' 存库 '''
        userGroup.save()

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


    def addPms(self, pms):
        '''
        给用户组添加权限
        :param permission: 必须以 UserGroup.PERMISSION_* 来传递
        :return:
        '''
        # for pm in self.__class__.getPermissionDic().values():
        #     if not permissions & pm:
        #         effInfo = u'用户组: %s设定权限失败!!非法的权限 %d !!!' % (self.name, permissions)
        #         raise ValueError(effInfo)
        self.permissions |= pms


    def setPms(self, pms):
        '''
        直接将用户组的权限置为指定的权限
        :param permissions:
        :return:
        '''
        self.permissions = pms


    def removePms(self, pms):
        '''
        给用户组减少权限
        :param permission:
        :return:
        '''
        # if permissions not in self.__class__.getPermissionDic().values():
        #     effInfo = u'用户组: %s设定权限失败!!非法的权限 %d !!!' % (self.name, permissions)
        #     raise ValueError(effInfo)

        ''' 先授权，在卸权。因为计算算法的原因，所以这么做 '''
        self.addPms(pms)
        self.permissions -= pms
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
        pms = cls.getAllPms() - cls.PERMISSION_BAN_LOGIN
        ug = UserGroup.createNewUserGroup(UserGroup.rootGroup, pms)

        return ug


    @classmethod
    def getPmNames(cls):
        '''
        所有权限的名字数组
        :return:
        '''
        names = []
        for n in cls.getPermissionDic().keys():
            ls = n.split('_')
            n = '_'.join(ls[0:])
            names.append(n)
        return names


    def removeAllPms(self):
        '''
        移除 该用户组 所有权限
        :return:
        '''

        self.removePms(self.pms)



    def delete(self, User):
        '''
        重写 delete 方法，删除用户组需要同时将从用户身上删除用户组
        :return:
        '''
        for u in User.all():
            if self in u.userGroups:
                u.removeUserGroup(self)
                u.save()

        ''' 从redis中删除实例 '''
        orm.RediscoModle.delete(self)
