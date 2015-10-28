#encoding:utf-8
__author__ = 'morichounami'
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey
from models.user_do import *

# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',
#          encoding='utf-8', echo=True)
# mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
#        encoding='utf-8', echo=True)
# mysql_engine = create_engine('mysql://root:1qazxsw2@121.41.100.80:3306/db_gongzhuhao?charset=utf8',
#        encoding='utf-8', echo=True)


# Session = sessionmaker(bind=mysql_engine)
# session = Session()

def create_roles(session):
    data = [('admin','管理员'),('merchant','商户')]
    session.execute(
        Roles.__table__.insert(),[{'Fcode':code,'Fname':name} for code,name in data]
    )
    session.commit()

# create_roles()