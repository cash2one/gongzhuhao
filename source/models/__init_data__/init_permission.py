#encoding:utf-8
import sys
sys.path.append('../')
sys.path.append('../../')

#CREATE DATABASE IF NOT EXISTS db_gongzhuhao DEFAULT CHARSET utf8;
from models.user_do import *
from models.schedule_do import *
from models.order_do import *
from models.staffer_do import *
from models.album_do import *

from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base

__author__ = 'binpo'


# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',encoding='utf-8', echo=True)
# mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
#        encoding='utf-8', echo=True)

#mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao?charset=utf8',encoding='utf-8', echo=True)
# mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8', encoding='utf-8', echo=True)

# Session = sessionmaker(bind=mysql_engine)
# session = Session()


def insert_permission(session):
    for d in permission_list:
        permission = Permission()
        permission.Fcode = d[0]
        permission.Fname = d[1]
        permission.Fdesc = d[2]
        session.add(permission)
        session.commit()

permission_list = [
    ['orders_view', '服务查看', '查看订单信息'],
    ['orders_edit', '增删改', '订单增删改'],
    ['schedule_view_edit','排期','排期操作 '],
    ['photos_view', '查看', '查看图片'],
    ['photos_edit', '上传照片', '上传照片,删除照片'],
    ['send_photoes','发送照片','照片发送至手机端'],
    ['plans_view', '查看', '档期查看'],
    ['plans_edit', '设置', '档期设置'],
    ['share_view', '查看', '分享统计查看'],
    ['potential_view', '查看', '潜客信息查看'],
    ['potential_return','回访','潜客回访'],
    ['merchant_information_view','查看','商户信息查看'],
    ['merchant_information_edit','编辑','商户信息编辑'],
    ['work_view', '查看', '作品查看'],
    ['work_edit', '编辑', '作品管理'],
    ['series_view', '查看', '套系查看'],
    ['series_edit', '编辑', '套系编辑'],
]


# print '初始化权限管理系统'
# init_permission(permission_list)
# print 'download'
