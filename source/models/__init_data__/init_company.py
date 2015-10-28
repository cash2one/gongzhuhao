#encoding:utf-8
__author__ = 'frank'

from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey
import sys
sys.path.append('../')
sys.path.append('../../')
from models.company_do import *

mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8',encoding='utf-8', echo=True)
#mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao?charset=utf8',encoding='utf-8', echo=True)

Session = sessionmaker(bind=mysql_engine)
session = Session()
def create_company():
    data = [(3,'only','shanghai','maobo')]
    data2 = [(2,'jack&jones','shanghai','zhangjinjin')]
    data3 = [(1,'唯一视觉','shanghai','qiuyan')]
    data4 = [(4,'幸福来敲门','shanghai','jinkuan')]
    session.execute(
        Company.__table__.insert(),[{'Fuser_id':Fuser_id,'Fcompany_name':Fcompany_name,'Fcompany_address':Fcompany_address,
                                   'Fcontact':Fcontact} for Fuser_id,Fcompany_name,Fcompany_address,Fcontact in data]
    )
    session.commit()

    session.execute(
        Company.__table__.insert(),[{'Fuser_id':Fuser_id,'Fcompany_name':Fcompany_name,'Fcompany_address':Fcompany_address,
                                   'Fcontact':Fcontact} for Fuser_id,Fcompany_name,Fcompany_address,Fcontact in data2]
    )
    session.commit()
    session.execute(
        Company.__table__.insert(),[{'Fuser_id':Fuser_id,'Fcompany_name':Fcompany_name,'Fcompany_address':Fcompany_address,
                                   'Fcontact':Fcontact} for Fuser_id,Fcompany_name,Fcompany_address,Fcontact in data3]
    )
    session.commit()
    session.execute(
        Company.__table__.insert(),[{'Fuser_id':Fuser_id,'Fcompany_name':Fcompany_name,'Fcompany_address':Fcompany_address,
                                   'Fcontact':Fcontact} for Fuser_id,Fcompany_name,Fcompany_address,Fcontact in data4]
    )
    session.commit()

create_company()
