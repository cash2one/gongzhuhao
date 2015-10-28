#encoding:utf-8
__author__ = 'binpo'

from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from models.schedule_do import SchedulePlan

t = [330, 331]# 12 4
mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao?charset=utf8',encoding='utf-8',echo=True)
Session = sessionmaker(bind=mysql_engine)
session = Session()
session.query(SchedulePlan).filter(SchedulePlan.Fuser_id==4,SchedulePlan.Fid.in_(t)).update({'Ftotal_per_day':int(12)},synchronize_session=False)
session.commit()