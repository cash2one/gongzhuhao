#encoding:utf-8
__author__ = 'wangjinkuan'

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,TIMESTAMP,Float,Text,Date
from sqlalchemy.sql.functions import now

class HomeRecommend(Base):
    '''
    todo:首页分享
    '''
    __tablename__ = 't_home_recommend'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)
    Frecommend_type = Column(Integer) #1:套系 2:产品 3:商家
    Fproduct_id = Column(Integer) #套系ID，产品ID，商家ID
    Fmerchant_id = Column(Integer) #推荐产品所属商家
    Fproduct_name = Column(String(512),default='')
    Frecommend_url = Column(String(512),default='',doc='首页展示图片url')
    Fposition = Column(String(512),default='',doc='首页展示位置')
    Fis_on_share = Column(Boolean,default=0,doc='是否已在首页展示')
    Fis_recommend = Column(Boolean,default=0,doc='是否推荐')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class AppsHomeRecommend(Base):
    '''
    todo:首页分享
    '''
    __tablename__ = 't_home_recommend_apps'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)
    Frecommend_type = Column(Integer)  #1:套系 2:产品 3:商家
    Fproduct_id = Column(Integer)      #套系ID，产品ID，商家ID
    Fmerchant_id = Column(Integer)     #推荐产品所属商家
    Fproduct_name = Column(String(512),default='')
    Frecommend_url = Column(String(512),default='',doc='首页展示图片url')
    Fposition = Column(String(512),default='',doc='首页展示位置')
    Fis_on_share = Column(Boolean,default=0,doc='是否已在首页展示')
    Fis_recommend = Column(Boolean,default=0,doc='是否推荐')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)


