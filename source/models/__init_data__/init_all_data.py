#encoding:utf-8
__author__ = 'wangjinkuan'

from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy.sql.functions import now

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

from models.__init_data__.init_roles import create_roles
from models.__init_data__.init_users import insert_users
from models.__init_data__.init_permission import insert_permission
from models.__init_data__.cities.cities import parse
from models.__init_data__.init_topic_img import insert_topic_img
from models.__init_data__.init_topics import insert_topic

# mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
#        encoding='utf-8', echo=True)

mysql_engine = create_engine('mysql://root:1qazxsw2@121.41.100.80:3306/db_gongzhuhao?charset=utf8', encoding='utf-8', echo=True)


Session = sessionmaker(bind=mysql_engine)
session = Session()

from lxml import etree
import os
ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
file_path = ROOT_PATH + "/" + "cities"+"/"
# print ROOT_PATH
def insert_data(sess,etree,file_path,mysql_engine):
    Base.metadata.drop_all(mysql_engine)
    Base.metadata.create_all(mysql_engine)
    create_roles(sess)
    insert_users(sess)
    insert_permission(sess)
    insert_topic_img(sess)
    insert_topic(sess)
    parse(sess,etree,file_path)

insert_data(session,etree,file_path,mysql_engine)