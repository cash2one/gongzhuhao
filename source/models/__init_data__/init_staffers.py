#encoding:utf-8
__author__ = 'frank'
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey
from models.staffer_do import *

mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
        encoding='utf-8', echo=True)

Session = sessionmaker(bind=mysql_engine)
session = Session()
def create_staffers():
    data = [('2','1','技术部','obama','13890099000')]
    session.execute(
        Staffers.__table__.insert(),[{'Fuid_mct':Fuid_mct,'Fdepartment_id':Fdepartment_id,'Fdepartment_name':Fdepartment_name,
                                    'Fname':Fname,'Fmobi':Fmobi}
                                   for Fuid_mct,Fdepartment_id,Fdepartment_name,Fname,Fmobi in data]
    )
    session.commit()

create_staffers()

