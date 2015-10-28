# encoding:utf-8

from models.base_do import Base
from sqlalchemy import Column, String, DateTime, Boolean, SmallInteger, TIMESTAMP,Integer,Date,Text
from sqlalchemy.sql.functions import now

class ShotScheduleCategory(Base):

    '''拍摄档期分类'''

    __tablename__ = 't_schedule_category'

    Fid = Column(Integer, primary_key=True, autoincrement=True)
    Fmerchant_id = Column(Integer,doc='商户ID')
    Fname = Column(String(128),doc='名称/地点')
    Fdefault = Column(Boolean,default=0,doc='是否默认')
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)


class SchedulePlan(Base):

    """档期管理"""

    __tablename__ = 't_schedule_plan'
    Fid = Column(Integer, primary_key=True, autoincrement=True)
    Fuser_id = Column(Integer,doc='商户ID')
    Fschedule_category_id = Column(Integer,doc='排期分类',nullable=True)
    Fschedule_type = Column(String(64),doc='排期类型')#SCHEDULE_TYPE     ['试衣', '摄影', '选样', '定稿', '取件']
    Fschedule_order_type = Column(String(64),doc='订单排期类型')#SCHEDULE_ORDER_TYPE
    Ftotal_per_day = Column(Integer,doc='每天拍摄数量')
    Fschedule_day = Column(Date,default=now())

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class OrdersSchedule(Base):

    """订单排期表"""
    __tablename__ = 't_orders_schedule'

    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键
    Fid = Column(SmallInteger)  # 排期ID [_Type index]
    Forder_id = Column(String(32))

    Fmerchant_id = Column(Integer,nullable=True)                                #商户ID
    Fcustomer_id = Column(Integer,nullable=True)                                #用户ID
    Foperation_id = Column(Integer, nullable=True)                              #操作人ID
    Fnotified_num = Column(SmallInteger, default=0)                             # 此排期已通知用户次数0未通知
    Fschedule_category_id = Column(Integer,doc='排期分类',nullable=True)         #档期分类id
    Fschedule_category_name = Column(String(128),default='',doc='排期分类名称')   #档期分类name

    Fdatetime = Column(DateTime)                                                # 此排期时间
    Fshot_date = Column(Date)                                                   # 此排期时间  精确到某一天

    Fsite = Column(String(128), default='')                             # 服务地点
    Fuid_stf = Column(String(256), default='')                          # 排期中参与的员工ID
    Fname_stf = Column(String(256), default='')                         # 排期中参与的员工姓名
    Ftitle_stf = Column(String(256), default='')                        # 排期中员工职称
    Freminder = Column(String(512), default='')                         # 温馨提示

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class ScheduleEvaluation(Base):

    '''
        排期 评论&拍照
    '''
    __tablename__ = 't_schedule_evaluation'

    Fid = Column(Integer, primary_key=True)
    Fschedule_id =Column(Integer, primary_key=True)
    Forder_id = Column(Integer,doc='订单ID')
    Fmerchant_id = Column(Integer,doc='商户ID')
    Fuser_id = Column(Integer,doc='用户ID')
    Fcontent = Column(String(1024),nullable=True,default=0,doc='评论内容')
    Fimage_ids = Column(String(1024),doc='图片id列表',default='')

    Fcreate_time = Column(DateTime,default=now())
    Fmodify_time = Column(DateTime,default=now())
    Fdeleted = Column(Boolean, default=0, server_default='0')


class ScheduleAttentionTemplate(Base):
    '''默认提醒模版'''

    __tablename__ = 't_schedule_attention'
    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer, doc='商户ID')
    Fschedule_type_id = Column(SmallInteger, doc='排期类型ID')
    Fschedule_type_name = Column(String(64), doc='名称')
    Fdescription = Column(String(1024), doc='描述')  # 提醒内容
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class ScheduleSiteTemplate(Base):
    '''排期信息中的服务地址模版'''

    __tablename__ = 't_schedule_site'
    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer, doc='商户ID')
    Fschedule_type_id = Column(SmallInteger, doc='排期类型ID')
    Fschedule_type_name = Column(String(64), doc='名称')
    Fsite = Column(String(1024), doc='服务地点')
    Fisdefault = Column(Boolean, default=0, doc='设置为默认地点')
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)

