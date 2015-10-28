#encoding:utf-8
import sys
sys.path.append('../')

from models.album_do import *
from models.app_do import *
from models.company_do import *
from models.location_do import *
from models.order_do import *
from models.product_do import *
from models.schedule_do import *
from models.share_do import *
from models.staffer_do import *
from models.user_do import *
from models.topic_do import *
from models.message_do import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy import create_engine

mysql_engine = create_engine('mysql://root:1qazxsw2@121.41.100.80:3306/db_gongzhuhao?charset=utf8', encoding='utf-8', echo=True)
# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',encoding='utf-8',echo=True)
# Base.metadata.drop_all(mysql_engine)
#
#mysql_engine = create_engine('mysql://root:111111@192.168.88.132:3306/db_gongzhuhao?charset=utf8', encoding='utf-8', echo=True)
# #mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao?charset=utf8',encoding='utf-8',echo=True)
# Base.metadata.drop_all(mysql_engine)
# Base.metadata.create_all(mysql_engine)
# exit(0)
Session = sessionmaker(bind=mysql_engine)
session = Session()
users = session.query(Users).filter(Users.Fdeleted==0).first()
print users.metadata
print dir(Users)
print dir(users)
# for u in users:
#     print 'hello start'
#     print dir(u)
#     print u.metadata
#     print 'endstart start'

exit(0)
session.close()
#
#
# # dic={'user_name':'qiuyan.zwp'}
# # Users.set_attrs(session,1,dic)
# # Users.set_attrs(session,1,user_name='qiuyan')
# #
# # exit
# from sqlalchemy import or_
# from utils.date_util import datetime_format
# import datetime
# # orders = session.query(OrdersSchedule).filter(OrdersSchedule.Fshot_date==datetime_format('%Y-%m-%d',datetime.datetime.now()+ datetime.timedelta(days=2)))
# # for o in orders:
# #     print '-------------------'
# #     print o.Fshot_date
# search_context='18'
# order_ids = session.query(Orders.Fid).filter(Orders.Fdeleted==0).filter(or_(Orders.Fuser_mobi.like('%{0}%'.format(search_context)),Orders.Forder_id_user.like('%{0}%'.format(search_context))))
# print order_ids
# id_list = [int(d[0]) for d in order_ids]
# print id_list
# print 'dd'
# session.close()