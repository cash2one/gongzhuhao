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
    users = [
        {'user_id':6,'category_id':1,'title':'因为在今天，我的内心也跟你一样的欢腾','content':'快乐！祝你们，百年好合'},
        {'user_id':7,'category_id':1,'title':'让流云奉上真挚的情意','content':'空气里都充满了醉人的甜蜜'},
        {'user_id':8,'category_id':1,'title':'空气里都充满了醉人的甜蜜','content':'白首齐眉鸳鸯比翼'},
        {'user_id':9,'category_id':1,'title':'花烛笑迎比翼鸟，洞房','content':'正所谓天生一对'},
        {'user_id':1,'category_id':1,'title':'青阳启瑞桃李同心','content':'人们常说的神仙眷侣就是你们了'},
        {'user_id':2,'category_id':1,'title':'白首齐眉鸳鸯比翼','content':'青阳启瑞桃李同心'},
        {'user_id':3,'category_id':1,'title':'红梅吐芳喜成连理','content':'绿柳含笑永结同心'},
        {'user_id':4,'category_id':1,'title':'对联是中国的传统文化的精华','content':'许订终身贺新婚'},
        {'user_id':5,'category_id':1,'title':'前生注定，喜结良缘','content':'许订终身贺新婚'},
        {'user_id':1,'category_id':1,'title':'新婚大喜！百年好合！','content':'新郎新娘的祝福语'},
]
    for u in users:
        service.create_topic(**u)

insert_topic(session)