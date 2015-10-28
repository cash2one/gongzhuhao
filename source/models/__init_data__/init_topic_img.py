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


mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',encoding='utf-8',echo=True)

# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',encoding='utf-8', echo=True)



Session = sessionmaker(bind=mysql_engine)
session = Session()

def insert_topic_img(session):
    service = TopicServices(session)
    users = [
        {'topic_id':1,'user_id':5,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':1,'user_id':5,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':1,'user_id':5,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':2,'user_id':6,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':2,'user_id':6,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':2,'user_id':6,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
        {'topic_id':1,'user_id':5,'url':'http://img.gongzhuhao.com/album/users/8/exquisite/1047457x379158000d493a9d737bd34385ab3e26.jp@80q_0r.jpg'},
    ]
    for u in users:
        service.create_topic_img_2(**u)

insert_topic_img(session)
