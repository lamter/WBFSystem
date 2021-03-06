#coding=utf-8
'''
Created on 2014-09-21

@author: Shawn
'''

import json

from redisco import models

from counter import Counter
from usergroup import UserGroup
import orm



Encoder = json.JSONEncoder()
Decoder = json.JSONDecoder()



''' 账号长度限制 '''
ACCOUNT_MAX_SIZE = 50
ACCOUNT_MIN_SIZE = 3

''' 密码长度限制 '''
PW_MAX_SIZE = 50
PW_MIN_SIZE = 6

NEW_ACCOUNT_ERR_NOT_UNIQUE = 'not unique'


def validateAccount(field_name, value):
    '''
    :return:
    '''
    if len(value) > ACCOUNT_MAX_SIZE:
        return ((field_name, '不能超过%d个字符!!!' % ACCOUNT_MAX_SIZE),)
    if len(value) < ACCOUNT_MIN_SIZE:
        return ((field_name, '用户名不能少于%d个字符!!!' % ACCOUNT_MIN_SIZE),)



def validatePassword(field_name, value):
    '''
    密码规范
    :param field_name:
    :param value:
    :return:
    '''
    if len(value) > ACCOUNT_MAX_SIZE:
        return ((field_name, '不能超过%d个字符!!!' % PW_MAX_SIZE),)
    if len(value) < ACCOUNT_MIN_SIZE:
        return ((field_name, '用户名不能少于%d个字符!!!' %PW_MIN_SIZE),)



class User(orm.RediscoModle):
    '''
    要存库的数据类型
    '''
    # uid = models.IntegerField(required=True, unique=True)
    username = models.Attribute(required=True, unique=True, validator=validateAccount)
    password = models.Attribute(required=True, validator=validatePassword)

    ''' 注册时间 '''
    register_time = models.DateTimeField(auto_now_add=True)

    ''' 最后登录时间 '''
    last_login_time = models.DateTimeField(auto_now=True)

    ''' 所属的用户组 '''
    _userGroups = models.ListField(target_type=str)

    ''' 是否注销 '''
    is_cancel = models.BooleanField(default=True)

    ''' root用户的账号和密码 '''
    rootAccount = 'root'
    import p
    rootPassword = p.pw


    def validate(self):
        '''
        :return:
        '''
        errss = ''
        for errs in self._errors:
            err = " ".join(errs)
            print err
            errss += err
        if self._errors:
            print 'are the reasons to '
        return errss


    # @classmethod
    # def obj(cls, ):
    #     '''
    #     根据用户名获取玩家
    #     :param args: [username]
    #     :return:
    #     '''
    #     username = args[0]
    #     return cls.objects.filter(username=username).first()


    @classmethod
    def all(cls):
        '''
        获得所有用户的实例
        :return:
        '''
        return cls.objects.filter().all().exclude(username=cls.rootAccount)



    @classmethod
    def createNewUser(cls, username, password):
        '''
        创建新的用户
        :param username:
        :param password:
        :return:
        '''
        # TODO 密码明文加密, 暂时不做加密，直接保存明文

        # user = User(uid=userUid, username=username, password=password)
        user = User(username=username, password=password)

        ''' 检查账号是否生成成功 '''
        if not user.is_valid():
            ''' 生成失败，直接报错退出 '''
            raise ValueError(user.errStr)
            # if NEW_ACCOUNT_ERR_NOT_UNIQUE in user.validate():
            #     raise ValueError('用户名重复!!!')

        ''' 生成新的用户的id '''
        counter = Counter.obj()
        counter.incr(Counter.user)
        user.id = counter.uid

        ''' 生成成功，账号存库 '''
        user.save()

        return user

    @property
    def userGroups(self):
        '''
        根据 userGroup.id索引回用户组实例
        :return:
        '''
        ugs = []
        for ugid in [ugid for ugid in self._userGroups]:
            ug = UserGroup.obj(id=ugid)
            ''' 如果该id已经作废，则移除 '''
            self._userGroups.remove(ugid) if ug is None else ugs.append(ug)

        return ugs


    @property
    def lastLoginTime(self):
        '''
        最后登录时间
        :return:
        '''
        return self.last_login_time



    @property
    def registerTime(self):
        '''
        注册时间
        :return:
        '''
        return self.register_time




    @property
    def isCancel(self):
        '''
        真个账号是否已经注销
        :return:
        '''
        return self.is_cancel


    def addUserGroup(self, userGroup):
        '''
        加入指定的用户组
        :param userGroup:
        :return:
        '''
        if not isinstance(userGroup, UserGroup):
            errInfo = '分配用户组失败!!!\nclass:%s不是指定的用户组类型%s!!!' % type(userGroup), UserGroup.__name__
            raise TypeError(errInfo)

        if userGroup in self.userGroups:
            errInfo = '用户已经在用户组 uid:%d %s 中了' % (userGroup.id, userGroup.name)
            raise ValueError(errInfo)

        self._userGroups.append(userGroup.id)
        self.save()


    def removeUserGroup(self, userGroup):
        '''
        移除用户组
        :param ug:
        :return:
        '''
        if not isinstance(userGroup, UserGroup):
            errInfo = '分配用户组失败!!!\nclass:%s不是指定的用户组类型%s!!!' % type(userGroup), UserGroup.__name__
            raise TypeError(errInfo)

        if userGroup not in self.userGroups:
            errInfo = '用户不在用户组 id:%d %s 中了' % (userGroup.id, userGroup.name)
            raise ValueError(errInfo)

        self._userGroups.remove(userGroup.id)


    @classmethod
    def createRoot(cls):
        '''
        生成root用户
        :return:
        '''
        ''' 生成root用户实例 '''
        root = User.createNewUser(User.rootAccount, User.rootPassword)

        root.initRootUg()

        root.save()

        return root


    def initRootUg(self):
        '''
        初始化root用户的root用户组权限
        :return:
        '''
        if self.username != self.__class__.rootAccount:
            raise ValueError('该用户不是root用户!!!')

        ''' 检查用户组 '''
        rootUg = UserGroup.obj(name=UserGroup.rootGroup)

        if rootUg:
            ''' 如果用户组存在，删除掉 '''
            rootUg.delete(User)

        rootUg = UserGroup.createRootGroup()
        rootUg.save()

        ''' 清空root的用户组 '''
        while len(self.userGroups) > 0:
            self._userGroups.pop(0)
        ''' 添加root用户组 '''
        self._userGroups.append(rootUg.id)


    def getPms(self):
        '''
        从所有用户组获得权限
        :return:
        '''
        p = set()
        for userGroup in self.userGroups:
            p |= userGroup.pms

        return p


    def isHavePms(self, permissions):
        '''
        用户是否拥有某几种权限
        :param permission: 只能传递 UserGroup.PERMISSION_*进来
        :return:
        '''
        return permissions & self.getPms()


    def isInUg(self, ug):
        '''
        是否在这个用户组中
        :param ug: UserGroup()
        :return:
        '''
        if not isinstance(ug, UserGroup):
            raise ValueError('错误的用户组类型: %s' % ug.__class__.__name__)
        return ug in self.userGroups


    def getUserGroupByName(self, name):
        '''
        根据 userGroup.name 获得 UserGroup()
        :param name:
        :return: UserGroup()  or None
        '''
        for ug in self.userGroups:
            if ug.name == name:
                return ug

        return None


    def isPW(self, pw):
        return self.password == pw


    def getUGNames(self):
        '''
        获得所有组名的数组
        :return:
        '''
        ns = []
        for ug in self.userGroups:
            ns.append(ug.name)
        return ns


    def getUnjoinGroups(self):
        '''
        获得未加入的用户组
        :return:
        '''
        ugs = UserGroup.all()
        unj = []
        j = self.getUGNames()
        for ug in ugs:
            if ug.name not in j:
                unj.append(ug)
        return unj
