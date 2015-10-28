#encoding:utf-8
__author__ = 'binpo'


from models.base_do import Base
from sqlalchemy import Column,Integer,Float,String,DateTime,Boolean,SmallInteger,Date,TIMESTAMP
from sqlalchemy.sql.functions import now

class ShareConf(Base):

    __tablename__ = 't_share_conf'

    Fid = Column(Integer, primary_key=True)
    Fmusic_style = Column(String(128),doc='音乐风格')
    Fmusic_name = Column(String(128),doc='音乐名称')                   #:音乐名称
    Fmusic_url = Column(String(256),doc='音乐路径')
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class ShareCategory(Base):

    '''分享分类'''

    __tablename__ = 't_share_category'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(128),doc='名称')
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class UserPhotosShare(Base):
    '''用户分享'''
    __tablename__ = 't_user_photos_share'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer,doc='分享用户ID')
    Forder_id = Column(Integer,doc='订单ID')
    Falbum_id = Column(Integer,doc='相册ID')
    Fmerchant_id = Column(Integer,doc='商户ID')
    Ftitle = Column(String(256),doc='分享标题')
    Fdescription = Column(String(1024),doc='分享描述')
    Fbg_color = Column(String(10),doc='背景颜色',nullable=True)
    Fslide_type = Column(SmallInteger,doc='滑动方向')                   #1.上下滑动  2.左右滑动
    Fmusic_style = Column(String(128),doc='音乐风格',default='')
    Fmusic_name = Column(String(128),doc='音乐名称',default='')                   #:音乐名称
    Fmusic_url = Column(String(256),doc='音乐路径',default='')
    Fmusic_id = Column(Integer,doc='音乐ID',nullable=True)
    Fcover_img = Column(String(512),doc='封面图',default='')

    Fforward_times = Column(Integer,default=0)               #转发次数
    Fpage_view = Column(Integer,default=0)                  #PV
    Fuser_view = Column(Integer,default=0)                  #UV
    Fassist_count = Column(Integer,default=0)                #赞的次数

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class ShareUserViews(Base):
    '''
    user_views
    '''
    __tablename__ = 't_share_user_views'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer,doc='分享用户ID')
    Fuser_photos_share_id = Column(Integer,doc='分享ID')
    Fweixin_id = Column(String(128),doc='微信ID') #微信ID
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class ShareImages(Base):
    '''
    分享的图片
    '''
    __tablename__='t_share_images'

    Fid = Column(Integer, primary_key=True)
    Fuser_photos_share_id = Column(Integer,doc='分享ID')

    Fimg_url = Column(String(256),doc='图片路径')
    Fimg_id = Column(Integer,doc='图片ID')

    Fimg_size = Column(Integer,doc='图片大小')

    Fsort = Column(Integer,default=0,doc='排序')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class ShareMusic(Base):
    '''分享背景音乐'''
    __tablename__='t_share_music'

    Fid = Column(Integer, primary_key=True)
    Fmusic_url = Column(String(256),doc='音乐路径')
    Fmusic_name = Column(String(64),doc='音乐名称')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

'''用户祝福可以用潜客合并一张表'''

class ShareWishes(Base):

    '''
        用户祝福
    '''
    __tablename__ = 't_share_wishes'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer,doc='分享用户ID')
    Fuser_photos_share_id = Column(Integer,doc='分享ID')
    Fweixin_id = Column(String(128),doc='微信ID') #
    Fsend_user = Column(String(256),doc='微信名称')
    Fweixin_photos = Column(String(128),doc='微信用户头像')
    Fwish_content = Column(String(1024),doc='祝福语')
    Fremote_ip = Column(String(32),doc='访问IP',nullable=True)

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class PotentialCustomer(Base):
    '''
    潜在客户信息纪录
    '''
    __tablename__ = 't_potential_customer'

    Fid = Column(Integer, primary_key=True)
    Fuser_photos_share_id = Column(Integer,nullable=True)                       #分享资源ID
    Fshare_user_id = Column(Integer,doc='分享人的ID')
    Fshare_name = Column(String(32),doc='潜客名称')                              #相册名称 or 来源名称  拍摄人的姓名
    Fmerchant_id = Column(Integer,nullable=True)                                #商户
    Fcompany_id = Column(Integer,nullable=True)                                 #公司ID
    Fpotential_customer_name = Column(String(64),nullable=True)                     #潜在联系人姓名
    Fpotential_customer_phone = Column(String(15),nullable=True)                    #潜客电话
    Fintention = Column(String(16),nullable=True,doc='意向')                     #意向

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class PotentialCustomerVisit(Base):

    __tablename__ = 't_potential_customer_visit'

    Fid = Column(Integer, primary_key=True)
    Fpotential_customer_id = Column(Integer,nullable=True)                       #潜在客服纪录ID
    Fintention = Column(String(16),doc='意向')
    Fshare_name = Column(String(32),doc='名称')                                    #相册名称 or 来源名称  拍摄人的姓名
    Fmerchant_id = Column(Integer,nullable=True)                                    #商户
    Fdesc = Column(String(512),doc='回访描述')
    Fvistor = Column(String(256),doc='回访用户')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)

class MerchantShareWishes(Base):
    '''
    商户祝福
    '''
    __tablename__ = 't_merchant_share_wishes'

    Fid = Column(Integer,primary_key=True)
    Fmerchant_id = Column(Integer,doc='商户ID')
    Foperation_id = Column(Integer,doc='商户操作人ID')
    Fwishes_type = Column(SmallInteger,doc='祝福类型')
    Fwishes_content = Column(String(512),doc="分享内容",default='')

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)





