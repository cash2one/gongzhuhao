#encoding:utf-8

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date,TIMESTAMP
from sqlalchemy.sql.functions import now


class Roles(Base):

    __tablename__ = 't_roles'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(String(128), default='',doc='代码')
    Fname = Column(String(128), default='',doc='名称')
    Fcreate_time = Column(DateTime,default=now())    #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())   #修改日期
    Fdeleted = Column(Boolean, default=0, server_default='0')        #默认存在


class Users(Base):
    """用户信息表"""
    __tablename__ = 't_users'

    STATUS={
        'normal':'正常',
        'inactive':'未激活',
        'delete':'删除',
        'reeze':'冻结'
    }

    Fid = Column(Integer, primary_key=True)
    Fuid = Column(String(64))       #用户ID 内部使用
    Fuser_mobi = Column(String(32), nullable=False)         #手机号码 注册/登陆用
    Fuser_name = Column(String(128), default='', server_default='')     #用户姓名
    Fuser_pwd = Column(String(128), nullable=False)                     #用户密码
    Fnick_name = Column(String(128), default='', server_default='')     #显示名称
    Frealname = Column(String(128), default='', server_default='')     #真实名称
    Femail = Column(String(128), default='', server_default='')         #email地址
    Fsex = Column(String(32),nullable=True)                             #性别
    Frole_codes = Column(String(256),default='')                        #角色
    Fpermission = Column(String(512),default='')                        #权限
    is_employee = Column(Boolean,doc='是否是员工')                       #是否是员工
    Fstatus = Column(String(128),default='inactive')                     #状态
    Fweibo = Column(String(128), default='', server_default='')          #微博号
    Fweixin = Column(String(128), default='', server_default='')         #微信号
    Fqq = Column(String(16), default='', server_default='')             #QQ号
    Fphoto_url = Column(String(128),server_default='')     #用户头像url
    Fbirthday = Column(Date, default='1980-12-12', server_default='1980-12-12')   #出生年月


    Fprovince = Column(Integer)          #省
    Fcity = Column(Integer)              #市
    Farea = Column(Integer)              #区
    Fdetail_address = Column(String(256)) #街道详细地址
    Faddress=Column(String(256))
    Fsign_text = Column(String(256),default='')                         #个性签名
    Flast_visit = Column(DateTime,default=now())             #暴露
    Flast_visit_ip = Column(String(16),default='')
    Fvisit_times = Column(Integer,default=0)                           #暴露 访问次数
    Fcoin = Column(Integer,default=0)
    Femail_check_url = Column(String(256),default='')                   #邮件激活链接

    Fcreate_time = Column(DateTime,default=now())    #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())   #修改日期
    Fdeleted = Column(Boolean, default=0, server_default='0')        #默认存在

class UserRoles(Base):

    __tablename__ = 't_user_roles'

    Fid = Column(Integer, primary_key=True)

    Fuser_id = Column(Integer,doc='用户ID')
    Frole_id = Column(Integer,doc='角色ID')

    Fcreate_time = Column(DateTime,default=now())     #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())                #修改日期
    Fdeleted = Column(Boolean, default=0)               #默认存在



class Permission(Base):

    __tablename__ = 't_permission'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(String(128), default='',doc='权限代码')
    Fname = Column(String(128), default='',doc='权限名称')
    Fdesc = Column(String(512),default='权限描述')

    Fcreate_time = Column(DateTime,default=now())    #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())   #修改日期
    Fdeleted = Column(Boolean, default=0, server_default='0')        #默认存在


class UserPermission(Base):

    __tablename__ = 't_user_permission'

    Fid = Column(Integer, primary_key=True)

    Fuser_id = Column(Integer,doc='用户ID')
    Fpermission_id = Column(Integer,doc='权限ID')

    Fcreate_time = Column(DateTime,default=now())     #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())                #修改日期
    Fdeleted = Column(Boolean, default=0)               #默认存在


class UserSignDays(Base):
    """
        用户签到
    """
    __tablename__="user_sign"
    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)           #用户
    Fsign_type = Column(String(50))      #签到类型  web_site  ios  android

    Fcreate_time = Column(DateTime,default=now())     #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())                #修改日期
    Fdeleted = Column(Boolean, default=0)               #默认存在

class UserFocus(Base):

    """关注和被关注"""
    __tablename__="t_user_focus"
    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)                          #用户
    Ffocus_user_id = Column(Integer)                    #关注用户
    Fis_fans = Column(Boolean)                          #是否已经关注    相互关注
    Fcreate_time = Column(DateTime,default=now())       #创建日期
    Fmodify_time = Column(DateTime,default=now())                #修改日期
    Fdeleted = Column(Boolean, default=0)               #默认存在
