#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,TIMESTAMP,Float,Text
from sqlalchemy.sql.functions import now

class Company(Base):
    '''
        商户公司信息
    '''
    __tablename__ = 't_company'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)                   #:商家ID

    Fcompany_name = Column(String(128))                  #公司名称
    Fprovince = Column(Integer)          #省
    Fcity = Column(Integer)              #市
    Farea = Column(Integer)              #区
    Fdetail_address = Column(String(200),default='') #街道详细地址
    Faddress = Column(String(256),default='')               #从省开始的 整个地址
    Fcontact = Column(String(64),default='')                #联系人
    Fphone = Column(String(256),default='')                  #联系人电话
    Fqq = Column(String(20),default='')                  #联系人qq
    Fmail = Column(String(50),default='')                  #联系人邮箱
    Fphoto_url = Column(String(512),default='')             #logo 图片地址
    Fbackground_url = Column(String(512),default='')             #背景图片地址
    level = Column(Integer,default=6)               #商户星级1-10 代表0-5 颗星
    Fdescription = Column(Text,default='')          #商家描述
    Fis_activity = Column(Boolean,default=0)        #参加活动
    Flat = Column(Float,nullable=True)              #经度
    Flng = Column(Float,nullable=True)              #纬度
    Fapp_url = Column(String(256),default='')       #微信app地址
    Fapp_token = Column(String(256),default='')     #微信token
    Fapp_id = Column(String(256),default='')        #微信app id
    Fapp_secret = Column(String(256),default='')    #微信secret
    Fmenu_codes = Column(String(256),default='')    #微信菜单编码,aaa,bb,cc，最多三个

    Fstyle_tags = Column(String(256),default='',doc='风格标签')

    Fcheapest = Column(Integer,default=0)
    Fmost_expensive = Column(Integer,default=0)
    Ffavorite_count = Column(Integer,default=0,doc='收藏数')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)


class CompanyContact(Base):
    '''公司联系人'''
    __tablename__ = 't_company_contact'

    Fid = Column(Integer, primary_key=True)
    Fcompany_id = Column(Integer,doc='公司ID')
    Fuser_name = Column(String(128),doc='商户联系人信息')        #商户联系人用户名
    Fmobile = Column(String(128),doc='商户联系人信息')        #商户联系人电话

    Fcreate_time = Column(DateTime,default=now())    #创建日期
    Fmodify_time = Column(TIMESTAMP,default=now())               #修改日期
    Fdeleted = Column(Boolean, default=0)              #默认存在


class BranchCompany(Base):

    '''公司分店信息'''
    __tablename__ = 't_branch_company'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)                   #:商家ID 装修公司
    Fname = Column(String(128))                  #分店名称
    Fprovince = Column(Integer)          #省
    Fcity = Column(Integer)              #市
    Farea = Column(Integer)              #区
    Fdetail_address = Column(String(200)) #街道详细地址
    Faddress = Column(String(256))               #从省开始的 整个地址
    Fphone = Column(String(128))      #联系电话

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class CompanyUsers(Base):
    '''
        公司用户信息
        可登陆后台关系操作
    '''

    __tablename__ = 't_company_users'

    Fid = Column(Integer, primary_key=True)
    Fuid_mct = Column(String(16), nullable=False)  # 商户ID
    Fuser_id = Column(Integer)  # 登陆人员ID
    Fcompany_id = Column(Integer)  # 公司信息ID

    Fpermission = Column(String(256), default='')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class CompanyAdditionInfo(Base):
    """
    商户的附加配置信息
        如：分享推广语 分享奖励语 的配置信息
    """

    __tablename__ = 't_company_addition_info'
    Fid = Column(Integer, primary_key=True)
    Fuid_mct = Column(Integer, nullable=False)      # 商家ID
    Finfo_key = Column(String(64), nullable=False)  # 附加信息key（区分不同类型信息）
    Finfo = Column(String(1024), default='')        # 附加信息值
    Fstatus = Column(String(16), default='')        # 状态

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class CompanyGift(Base):
    """
    商户的到店礼,订单礼
    """
    __tablename__ = 't_company_gift'

    Fid = Column(Integer, primary_key=True)
    Fuid_mct = Column(Integer,nullable=False)      # 商家ID
    Fgift_type = Column(Integer,nullable=False)  # 到店里还是订单礼(1,2)
    Fcontent = Column(String(1024), default='')        # 附加信息
    Fstatus = Column(String(16), default='')        # 状态

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

