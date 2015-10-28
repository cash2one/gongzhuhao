#encoding:utf-8
__author__ = 'wangjinkuan'

import sys
sys.path.append('../')
sys.path.append('../../')

from models.order_do import *
from services.orders.order_services import OrderServices
from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy.sql.functions import now

mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',encoding='utf-8', echo=True)
Session = sessionmaker(bind=mysql_engine)
session = Session()


def insert_users(session):
    '''
    :param session:
    0:试衣 1:摄影 2:选样 3:定稿 4:取件
    :return:
    '''
    service = OrderServices(session)
    evaluation_categorys = [
        {'schedule_type_id':'0','name':'试衣评价'},
        {'schedule_type_id':'1','name':'摄影评价'},
        {'schedule_type_id':'1','name':'化妆评价'},
        {'schedule_type_id':'2','name':'选样评价'},
        {'schedule_type_id':'3','name':'定稿评价'},
        {'schedule_type_id':'4','name':'取件评价'}
    ]
    for evaluation_category in evaluation_categorys:
        service.create_evaluation_category(**evaluation_category)

insert_users(session)
