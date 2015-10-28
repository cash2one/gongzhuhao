#encoding:utf-8
__author__ = 'wangjinkuan'

import sys
sys.path.append('../')
sys.path.append('../../')

from models.topic_do import *
from models.base_do import Base
from services.topics.topic_services import TopicServices

from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.functions import now


mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
       encoding='utf-8', echo=True)

Session = sessionmaker(bind=mysql_engine)
session = Session()


def insert_topic(session):

    service = TopicServices(session)
    sns = [
        {'user_id':5,'topic_id':4,'sns_type':1,'topic_type':2},
        {'user_id':5,'topic_id':6,'sns_type':1,'topic_type':2},
]
    for u in sns:
        service.create_topic_sns(u.get('topic_id'),u.get('user_id'),u.get('sns_type'),u.get('topic_type'))
# insert_users(session)
insert_topic(session)