#encoding:utf-8

from models.base_do import Base
from sqlalchemy import Column,Integer,Float,String,DateTime,Boolean,SmallInteger,Date,TIMESTAMP
from sqlalchemy.sql.functions import now

class Orders(Base):
    """订单表"""

    __tablename__ = 't_orders'

    Fid = Column(Integer, primary_key=True)
    Forder_id = Column(String(32))          #订单号(对内) 21位
    Forder_id_user = Column(String(64), nullable=False)       #用户输入的订单号(对外)
    Fuid = Column(String(16), default='', server_default='')       #订单对应的用户ID
    Fuid_mct = Column(String(16), nullable=False)       #订单对应的商户ID
    Foperation_id = Column(Integer, nullable=True)                          #操作人ID
    Forder_from = Column(String(10), doc='订单录入来源', default='apps_crm')             #apps_crm mobile  录入订单
    Forder_type = Column(SmallInteger, default=0, server_default='0') #订单类型
    Forder_pic = Column(String(64), doc='订单照片', default='')             #订单合同照片id
    Fuser_name = Column(String(64), default='', server_default='')  #用户姓名
    Fuser_name_ex = Column(String(64), default='', server_default='')  #客户第二姓名（如新郎）
    Fuser_mobi = Column(String(64), default='', server_default='')  #客户手机号
    Fuser_mobi_ex = Column(String(64), default='', server_default='')  #客户第二手机号
    Fuser_birth = Column(Date, default='1980-12-12', server_default='1980-12-12')   #出生年月
    Fuser_birth_ex = Column(Date, default='1980-12-12', server_default='1980-12-12')#出生年月
    Fuid_stf = Column(String(64), default='', server_default='',doc='接单人')    #商户员工ID 接单人
    Famount = Column(Integer, default=0, server_default='0')      #订单金额
    Fdeposit = Column(Integer, default=0, server_default='0')      #订单金额
    Fstatus = Column(SmallInteger, default=0, server_default='0')     #订单状态 conf.order_conf._ORDERS_STATUS
    Fcomment = Column(String(1024), default='', server_default='')  #备注信息

    Ffitting_time = Column(DateTime,nullable=True,default=None,doc='试衣时间')
    Fshot_time = Column(DateTime,nullable=True,default=None,doc='拍摄时间')
    Fselect_time = Column(DateTime,nullable=True,default=None,doc='选片时间')
    Fcertain_time = Column(DateTime,nullable=True,default=None,doc='定稿时间')
    Fabtain_time = Column(DateTime,nullable=True,default=None,doc='取件时间')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(TIMESTAMP,default=now())
    Fdeleted = Column(SmallInteger, default=0, server_default='0')

class OfflinePayOrder(Base):

    __tablename__ = 't_offline_pay_order'

    Fid = Column(Integer, primary_key=True)
    Forder_id = Column(String(32))
    Famount = Column(Integer,doc='金额')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(TIMESTAMP,default=now())
    Fdeleted = Column(SmallInteger, default=0, server_default='0')


class OrderSignUser(Base):

    __tablename__ = 't_order_sign_user'

    Fid = Column(Integer, primary_key=True)
    Forder_id = Column(String(32))

    Fstaff_id = Column(Integer,doc='员工ID')
    Fstaff_name = Column(String(64),doc='员工ID')
    Ffull_departent_name = Column(String(128),default='',doc='部门全路径')
    Ffull_departmnt_id = Column(String(128),default='',doc='部门全路径ID')
    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(TIMESTAMP,default=now())
    Fdeleted = Column(Boolean, default=0)

class OrdersFrom(Base):

    __tablename__ = 't_order_from'

    Fid = Column(Integer, primary_key=True)
    Forder_id = Column(Integer)                 #订单名称
    Fmerchant_id = Column(Integer,nullable=True)
    Forder_from_id = Column(Integer)            #来源ID
    Ffrom_name = Column(String(256),doc='来源名称')
    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class EvaluationCategory(Base):
    '''评价分类'''

    __tablename__ = 't_evaluation_category'

    Fid = Column(Integer, primary_key=True)
    Fschedule_type_id = Column(SmallInteger,doc='排期类型ID')
    Fname = Column(String(62),doc='评价名称')
    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class OrderEvaluation(Base):
    '''
        订单(用户)评价
    '''
    __tablename__ = 't_orders_evaluation'

    Fid = Column(Integer, primary_key=True)
    Forder_id = Column(Integer,doc='订单ID')
    Fmerchant_id = Column(Integer,doc='商户ID')
    Fuser_id = Column(Integer,doc='用户ID')
    Fschedule_type_code = Column(Integer,doc='排期类型code')
    Fcategory_name = Column(String(64),doc='类型名称')
    Fstaffer_name = Column(String(256),doc='服务人员姓名')
    Fscore = Column(String(64),doc='评分')
    Fcontent = Column(String(1024),nullable=True,default=0,doc='评论内容')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class EvaluationImages(Base):
    '''
        评价图片
    '''
    __tablename__ = 't_evaluation_images'

    Fid = Column(Integer, primary_key=True)
    Forder_evaluation_id = Column(Integer,doc='评价ID')
    Fimg_id = Column(Integer,doc='图片ID')
    Fimg_url = Column(String(256),doc='推案地址')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)


class OrderFromConf(Base):

    __tablename__ = 't_order_from_conf'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer,doc='商户ID')
    Fname = Column(String(256),doc='订单来源')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class OrderDataBackup(Base):

    __tablename__= 't_merchant_data_backup'
    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer,doc='商户ID')
    Fback_url = Column(String(256),doc='备份数据地址')
    Fsave_name = Column(String(128),doc='保存名称')
    Fstart_date = Column(Date,doc='统计开始时间')
    Fend_date = Column(Date, doc='统计结束时间')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class BespeakOrders(Base):

    ORDER_STATUS=[
        (0,'下单待处理'),
        (1,'已处理,预定成功'),
        (2,'已处理,不预定'),
        (3,'已完结')
    ]

    ORDER_TYPE=[
        (1,'商户订单'),
        (2,'套系订单'),
        (3,'作品订单')
    ]
    __tablename__= 't_bespeak_orders'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer,doc='用户ID',nullable=True)
    Fmerchant_id = Column(Integer,doc='商户ID')
    Forder_type = Column(SmallInteger,doc='订单类型')       #1.商户订单,2.套系订单 3.作品订单
    Frefer_id = Column(Integer,doc='引用ID')
    Fcontact = Column(String(128),doc='联系人')
    Fmobile = Column(String(32),doc='联系电话')

    Fstatus = Column(SmallInteger,doc='状态')                 #订单状态
    Fintention = Column(SmallInteger,nullable=True,default=0)          #意向 0.待定 1.没意向  2.有意向

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0)

class BespeakOrdersVisit(Base):

    __tablename__ = 't_bespeak_orders_visit'

    Fid = Column(Integer, primary_key=True)
    Fbespeak_order_id = Column(Integer,nullable=True)                       #潜在客服纪录ID
    Fmerchant_id = Column(Integer,nullable=True)                            #商户

    Forder_user = Column(String(32),doc='回访用户') #
    Fdesc = Column(String(512),doc='回访描述')
    Fvistor = Column(String(256),doc='回访用户')    #回访员工姓名

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)