#encoding:utf-8
__author__ = 'wangjinkuan'

from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, Date, TIMESTAMP
from sqlalchemy.sql.functions import now
from sqlalchemy import event

class Activity(Base):

    __tablename__ = 't_activities'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer)
    Fproduct_id = Column(Integer)
    Fproduct_name = Column(String(256),doc='产品名称')
    Fcover_img = Column(String(512),doc='封面图')
    Fproduct_type = Column(Integer)     #套系 1 其他类型再定
    Fcompany_name = Column(String(256),doc='公司名')
    Fprice = Column(Integer,doc='原价')
    Fsale_price = Column(Integer,doc='现价')
    Forder_gift = Column(String(512),doc='优惠')
    Fcompany_gift = Column(String(512))
    Fend_date = Column(DateTime)
    Flink_url = Column(String(1024),doc='链接')
    Fsort = Column(Integer,doc='排序')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=False)