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

# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',encoding='utf-8', echo=True)



Session = sessionmaker(bind=mysql_engine)
session = Session()

# insert into t_topics (Fuser_id,Fcotegory_id,Ftitle,Fcontent,Ftotal_img,Fis_top,Fis_essence,Ftotal_assess) values
# (2,1,'title2','content_2',2,0,0,6),
# (1,1,'title3','content3',3,0,1,5),
# (3,1,'title4','content4',2,1,1,6),
# (4,1,'title5','content5',8,1,0,6),
# (1,1,'title6','content6',2,0,1,6);

def insert_topic(session):

    service = TopicServices(session)
    users = [
        # {'user_id':8,'topic_id':1,'reply_index':6,'parent_id':1,'content':'两情相悦的最高境界'},
        # {'user_id':9,'topic_id':1,'reply_index':7,'parent_id':1,'content':'金屋笙歌偕彩凤洞房花'},
        # {'user_id':10,'topic_id':1,'reply_index':8,'parent_id':2,'content':'祝你俩幸福美满'},
        # {'user_id':4,'topic_id':1,'reply_index':9,'parent_id':3,'content':'携手共渡美丽人生'},
        # {'user_id':9,'topic_id':1,'reply_index':10,'parent_id':4,'content':'恭喜你们步入爱的殿堂'},

        # {'user_id':9,'topic_id':1,'reply_index':11,'parent_id':6,'content':'彩凤洞房花烛喜乘龙 '},
        # {'user_id':2,'topic_id':1,'reply_index':12,'parent_id':7,'content':'同德同心幸福长'},
        # {'user_id':5,'topic_id':1,'reply_index':13,'parent_id':8,'content':'祝福一对新人真心相爱'},
        # {'user_id':1,'topic_id':1,'reply_index':14,'parent_id':9,'content':'敬祝百年好合永'},

        {'user_id':11,'topic_id':1,'parent_id':9,'content':'同德同心幸福长'},


]
    for u in users:
        service.create_topic_reply(**u)

# insert_users(session)
insert_topic(session)