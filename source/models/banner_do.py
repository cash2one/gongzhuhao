#encoding:utf-8
__author__ = 'wangjinkuan'

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,TIMESTAMP,Float,Text,Date
from sqlalchemy.sql.functions import now

class BannerType(Base):
    '''
    todo:banner类型
    '''
    __tablename__ = 't_banner_type'

    Fid=Column(Integer,primary_key=True)   #banner type
    Fbanner_name=Column(String(100))     #ing称
    Fbanner_code = Column(String(20))   # banner_code
    Fbanner_desc = Column(String(1024))  #描述   banner的位置，banner图片尺寸，大小

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class Banner(Base):
    """
        Banner 配置
    """
    __tablename__ = 't_banners'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(128))              #banner name
    Fbanner_code = Column(String(20))        #对应的banner code
    Fimage_url = Column(String(256))          #banner图片
    Fdescription = Column(String(1024))       #banner 图片说明
    Flink = Column(String(1024))              #banner的链接
    Fvalue_type=Column(Integer)
    Fstart_time = Column(DateTime)             #展示时间
    Fexpire_time = Column(DateTime)            #展示结束时间

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)