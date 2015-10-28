#encoding:utf-8
import sys
sys.path.append('../')
sys.path.append('../../')

#CREATE DATABASE IF NOT EXISTS db_gongzhuhao DEFAULT CHARSET utf8;
from models.user_do import *
# from models.schedule_do import *
# from models.order_do import *
# from models.staffer_do import *
# from models.album_do import *

from sqlalchemy import create_engine
from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy.sql.functions import now


mysql_engine = create_engine('mysql://root:sunwang@127.0.0.1:3306/db_gongzhuhao?charset=utf8',
       encoding='utf-8', echo=True)

# mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/db_gongzhuhao_publish?charset=utf8',encoding='utf-8', echo=True)



Session = sessionmaker(bind=mysql_engine)
session = Session()


from services.users.user_services import UserServices

def insert_users(session):

    service = UserServices(session)
    users = [
        {'user_name':'jinkuan','user_pwd':'111111','phone':'13817959607','email':'','is_employee':1,'nick':'锦宽','roles':[1,2],'merchant_name':'锦宽婚纱摄影','merchant_addr':'毕升路299弄'},
        {'user_name':'qiuyan','user_pwd':'111111','phone':'15882136829','email':'','is_employee':1,'nick':'丘岩','roles':[1,2],'merchant_name':'丘岩婚纱摄影','merchant_addr':'毕升路299弄'},
        {'user_name':'jinjin','user_pwd':'111111','phone':'18521099629','email':'','is_employee':1,'nick':'锦锦','roles':[1,2],'merchant_name':'锦锦婚纱摄影','merchant_addr':'毕升路299弄'},
        {'user_name':'jinxin','user_pwd':'111111','phone':'13917507064','email':'','is_employee':1,'nick':'金鑫','roles':[1,2],'merchant_name':'金鑫婚纱摄影','merchant_addr':'毕升路299弄'},
        {'user_name':'mingming','user_pwd':'111111','phone':'13808483343','email':'','is_employee':1,'nick':'明明','roles':[1,2],'merchant_name':'明明婚纱摄影','merchant_addr':'毕升路299弄'},
        {'user_name':'zhanguo','user_pwd':'111111','phone':'18105713808','email':'','is_employee':1,'nick':'战国','roles':[1,2],'merchant_name':'战国婚纱摄影','merchant_addr':'毕升路299弄'},
]
    for u in users:
        service.create_user(**u)

    # data = [('admin','管理员','qiu@taobao.com','qiuyan','123445'),('businessman','商户','zhan@taobao.com','hello','hello1234'),('user','普通用户','guo@alibaba-inc.com','hello','hellowerr')]
    # t = session.execute(
    #     Users.__table__.insert(),[{'uuid':code,'nick':name,'email':email,'user_name':username,'user_pwd':password} for code,name,email,username,password in data]
    # )
    # print t

    #session.commit()

# def create_roles():
#     data = [('admin','管理员','整个站点管理'),('merchant','商户','商家用户')]
#     session.execute(
#         Roles.__table__.insert(),[{'Fcode':code,'Fname':name} for code,name,description in data]
#     )
#     session.commit()
#
# create_roles()
# insert_users()


# d = now()
# print d
# t = '''INSERT INTO t_users (`Fuid`, `Fuser_mobi`, `Fuser_name`, `Fuser_pwd`, `Femail`, `Frole_codes`, is_employee, `Fweibo`, `Fweixin`, `Fqq`, `Fphoto_url`, `Fbirthday`, `Fdeleted`)
# VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)'''%('508d4265-4e71-3170-b247-2369ea589ba6', '13438291032', 'qiuyan', '0e17a4750ba8f30313cc830c99a4e2d1', 'wenpeng.zhap@zenmez.com', '',
#                                                                               1, '', '', '', '', '1980-12-12', 0)
#
# print t

#INSERT INTO t_users (`Fuid`, `Fuser_mobi`, `Fuser_name`, `Fuser_pwd`, `Femail`, `Frole_codes`, is_employee, `Fweibo`, `Fweixin`, `Fqq`, `Fphoto_url`, `Fbirthday`, `Fdeleted`)VALUES ('508d4265-4e71-3170-b247-2369ea589ba6', '13438291032', 'qiuyan', '0e17a4750ba8f30313cc830c99a4e2d1', 'wenpeng.zhap@zenmez.com', '', 1, '', '', '', '','1980-12-12',0)
#print session.query(Users).count()