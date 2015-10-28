#encoding:utf-8
__author__ = 'frank'
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy import create_engine, MetaData,ForeignKey
from models.order_do import *

mysql_engine = create_engine('mysql://root:111111@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
        encoding='utf-8', echo=True)

Session = sessionmaker(bind=mysql_engine)
session = Session()
def create_orders():
    data = [('22015020241734106','20112222','2','1','linda','13817777663','1','1000','1','备注信息')]
    data1 = [('22015020241734107','20112223','2','1','peter','13817777665','1','1000','2','备注信息')]
    data2 = [('22015020241734108','20112224','7','2','john','13817777608','1','1000','1','备注信息')]
    data3 = [('22015020241734109','20112225','7','1','tom','138177776134','1','1000','1','备注信息')]
    data4 = [('22015020241734110','20112226','2','0','viona','13817776790','1','1000','1','备注信息')]
    data5 = [('22015020241734111','20112227','2','1','allen','13817777013','1','1000','0','备注信息')]
    data6 = [('22015020241734112','20112228','7','3','mathiue','13817777482','1','1000','1','备注信息')]
    data7 = [('22015020241734113','20112229','2','1','ruby','13817777011','1','1000','2','备注信息')]
    data8 = [('22015020241734114','20112210','7','2','frank','13817777294','1','1000','1','备注信息')]
    data9 = [('22015020241734115','20112211','2','1','cathilen','13817777739','1','1000','1','备注信息')]

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data1]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data2]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data3]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data4]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data5]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data6]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data7]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data8]

    )
    session.commit()

    session.execute(
        Orders.__table__.insert(),[{'Forder_id':Forder_id,'Forder_id_user':Forder_id_user,'Fuid_mct':Fuid_mct,
                                    'Forder_type':Forder_type,'Fuser_name':Fuser_name,'Fuser_mobi':Fuser_mobi,
                                    'Fuid_stf':Fuid_stf,'Famount':Famount,'Fstatus':Fstatus,'Fcomment':Fcomment}
                                   for Forder_id,Forder_id_user,Fuid_mct,Forder_type,Fuser_name,Fuser_mobi,Fuid_stf,
                                   Famount,Fstatus,Fcomment in data9]

    )
    session.commit()

create_orders()
