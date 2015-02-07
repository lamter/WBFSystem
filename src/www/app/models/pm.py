#coding=utf-8
'''
Created on 2015-1-3

@author: Shawn
'''

# import orm

class PM(object):
    """
    权限管理
    """
    ''' 用户权限枚举=> '''

    PM_MAP = {}
    ''' 用户权限枚举=> '''

    ''' 登录权限比较特殊 '''
    PERMISSION_BAN_LOGIN = set(['PERMISSION_BAN_LOGIN'])
    PM_MAP['PERMISSION_BAN_LOGIN'] = PERMISSION_BAN_LOGIN

    ''' 其他权限 '''

    ''' 创建用户组 '''
    PERMISSION_CREATE_USER_GROUP = set(['PERMISSION_CREATE_USER_GROUP'])
    PM_MAP['PERMISSION_CREATE_USER_GROUP'] = PERMISSION_CREATE_USER_GROUP

    ''' 创建用户 '''
    PERMISSION_CREATE_USER = set(['PERMISSION_CREATE_USER'])
    PM_MAP['PERMISSION_CREATE_USER'] = PERMISSION_CREATE_USER

    ''' 查看用户列表 '''
    PERMISSION_USER_LIST = set(['PERMISSION_USER_LIST'])
    PM_MAP['PERMISSION_USER_LIST'] = PERMISSION_USER_LIST

    ''' 创建用户组 '''
    PERMISSION_USER_GROUP_LIST = set(['PERMISSION_USER_GROUP_LIST'])
    PM_MAP['PERMISSION_USER_GROUP_LIST'] = PERMISSION_USER_GROUP_LIST

    ''' 修改用户信息 '''
    PERMISSION_MODIF_USER = set(['PERMISSION_MODIF_USER'])
    PM_MAP['PERMISSION_MODIF_USER'] = PERMISSION_MODIF_USER

    ''' 修改 用户组 信息 '''
    PERMISSION_MODIF_USER_GROUP = set(['PERMISSION_MODIF_USER_GROUP'])
    PM_MAP['PERMISSION_MODIF_USER_GROUP'] = PERMISSION_MODIF_USER_GROUP

    ''' 管理用户信息页面 '''
    PERMISSION_MANAGER_USER = set(['PERMISSION_MANAGER_USER'])
    PM_MAP['PERMISSION_MANAGER_USER'] = PERMISSION_MANAGER_USER

    ''' 本地服务的伪终端 '''
    PERMISSION_SIM_TERM_LOCAL_SERVER = set(['PERMISSION_SIM_TERM_LOCAL_SERVER'])
    PM_MAP['PERMISSION_SIM_TERM_LOCAL_SERVER'] = PERMISSION_SIM_TERM_LOCAL_SERVER

    ''' 以 PERMISSION_* 的形式来命名变量 '''

    ''' <=用户权限枚举 '''
    ''' 以 PERMISSION_* 的形式来命名变量 '''



    @classmethod
    def getPermissionDic(cls):
        '''
        获得权限的字典{属性名: 权限}
        :return:
        '''
        return cls.PM_MAP.copy()


    @classmethod
    def defaultPms(cls):
        """
        默认权限
        :return:
        """
        return set()
