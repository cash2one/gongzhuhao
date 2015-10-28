#encoding:utf-8
__author__ = 'wangjinkuan'


from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date,Text
from sqlalchemy.sql.functions import now
from sqlalchemy import event

class UsersFavorites(Base):
    '''
        用户收藏
    '''
    __tablename__='t_favorites'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)   #收藏用户ID
    Ffavorites_type = Column(SmallInteger,doc='收藏类型') #1:商户  2:套系 3:作品
    Ffavorites_id = Column(Integer,doc='收藏产品ID')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)