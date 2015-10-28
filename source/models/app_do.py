# -*- coding: utf-8 -*-

__author__ = 'zhaowenpeng'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, Float
from sqlalchemy.sql.functions import now

class AppVersion(Base):
    """
    app 版本控制
    """
    __tablename__ = 'app_version'

    id = Column(Integer, primary_key=True)
    app_type = Column(SmallInteger,doc='app类型')             # 3:ios app. 1:andrido app. 2: pc client.
   # ttid = Column(Integer)                      #:标示
    app_version = Column(String(128),doc='版本')           #app版本
    md5string = Column(String(128),doc="md5验证")             #md5验证
    app_url = Column(String(128),doc="下载地址")               #下载地址
    file_name = Column(String(128),doc='文件名称')              #文件名称
    app_size = Column(Integer,doc="大小")                  #大小
#    app_tile = Column(String(128),doc="title")              #title
    app_desc = Column(String(1024),doc="描述")             #描述
    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=0)


class ClientToken(Base):
    """
    app token
    """
    __tablename__ = 'app_token'
    id = Column(Integer, primary_key=True)
    app_type = Column(SmallInteger)
    user_id = Column(Integer)
    app_version = Column(String(128))
    client_token = Column(String(128))
    lat = Column(Float)             #经度
    lng = Column(Float)             #纬度
    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=0)

class WeixinMenu(Base):
    """
    微信菜单
    """
    __tablename__ = 'wx_menu'
    id = Column(Integer, primary_key=True)

    code = Column(String(128))   #菜单编码
    name = Column(String(128))   #菜单名称
    type = Column(String(128))   #菜单类型
    is_common = Column(Boolean,default=0)   #是否公共，0：否认，需结合用户id访问；1：是
    is_sub = Column(Boolean,default=0)   #是否子菜单，0：否；1：是
    parent_name = Column(String(128))   #子菜单的父name
    url = Column(String(128))   #访问地址,type为view时有用
    key = Column(String(128))   #key,type为click时有用

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=0)