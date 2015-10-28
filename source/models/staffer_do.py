#encoding:utf-8

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date
from sqlalchemy.sql.functions import now


class Staffers(Base):
    """员工信息表"""
    __tablename__ = 't_staffers'
    Fid = Column(Integer, primary_key=True)
    Fuid_mct = Column(String(16))   #商户ID
    Fdepartment_id = Column(String(8), nullable=False)   #所属部门ID
    Fdepartment_name = Column(String(64), nullable=False)   #所属部门名称
    Fname = Column(String(64), nullable=False)            #员工姓名
    Fmobi = Column(String(32), default='', server_default='')  #手机号码 注册/登陆用
    Fpwd = Column(String(128), default='', server_default='')  #用户密码
    Femail = Column(String(128), default='', server_default='')         #email地址
    Ftitle = Column(String(128), default=0, server_default='0')          #员工职称
    Fphoto_url = Column(String(128), default='', server_default='')     #员工头像url
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class Department(Base):
    """商户部门信息表（支持两级部门）"""
    __tablename__ = 't_department'

    Fid = Column(Integer, primary_key=True)

    Fuid_mct = Column(String(16))   # 商户ID
    Fname = Column(String(64), nullable=False)  # 部门名称
    Fdepartment_level = Column(Integer, default=1, server_default='1')    #部门级别 1/2
    Fdepartment_father = Column(Integer)   #上一级部门ID
    Ffull_departm_id = Column(String(128), default='', server_default='',nullable=True)   #部门全路径ID
    Ffull_department_name = Column(String(128), nullable=True)                               #部门全路径名称
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0, server_default='0')




