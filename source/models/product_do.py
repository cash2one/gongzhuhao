#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date,TIMESTAMP,Text,Enum,Float
from sqlalchemy.sql.functions import now

class ProductType(Base):
    """
        产品分类   案例  XX
    """
    __tablename__ = 'product_type'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(String(16))                  #代码
    Fname = Column(String(128))                  #名称

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class WeddingPhotoProduct(Base):
    '''
        商家作品/
    '''
    __tablename__ = 't_wedding_photo_product'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer)               #:商家ID 装修公司
    Fuser_id = Column(Integer)                  #子用户id
    Fproduct_type = Column(String(64))                      #产品类型   自定义  不写数据库
    Fname = Column(String(256),doc='名称')

    Fshot_space = Column(String(64),doc='拍摄地点')
    Fshot_space_name = Column(String(128),doc='拍摄地点')
    Fstyle_code = Column(String(64),doc='风格code')
    Fstyle_name = Column(String(64),doc='风格名称')
    Fshot_scene_code = Column(String(64),doc='拍摄场景code')
    Fshot_scene_name = Column(String(64),doc='拍摄场景名称')
    Fmode_style_code = Column(String(64),doc='造型特色code')   #逗号区分
    Fmode_style_name = Column(String(64),doc='造型特色名称')

    Fsale_price = Column(Integer,doc='起拍价')

    Ftitle = Column(String(256),doc='标题')
    Fdescription = Column(String(1024),doc='描述')
    Fcover_img = Column(String(512),doc='封面图')
    Ffavorite_count = Column(Integer,default=0,doc='收藏数')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class WeddingPhotoProductImages(Base):
    '''
    产品图片
    '''
    __tablename__ = 't_wedding_photo_product_images'

    Fid = Column(Integer, primary_key=True)
    Fwedding_photo_product_id = Column(Integer,doc='产品 楼上表ID')

    Fimg_id = Column(Integer,doc='图片ID')
    Furl = Column(String(512),doc='图片请求地址')
    Fsort = Column(Integer,doc='图片显示排序')
    Fdescription = Column(String(512),doc="图片描述")

    Fassist_count = Column(Integer,default=0)                #赞的次数
    Fcomments_count = Column(Integer,default=0)              #评论次数
    Fcollection = Column(Integer,default=0)                  #收藏次数

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

# class ShotPakageStyleConf(Base):
#     '''
#     服装造型
#     '''
#     __tablename__='t_shot_pakage_style'
#     pass
#
#
# class ShotPakageSpaceConf(Base):
#
#     __tablename__='t_shot_pakage_photos_conf'
#     pass


class ShotPackage(Base):
    '''
    套系
    '''
    __tablename__='t_shot_package'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer)               #:商家ID 装修公司
    Fuser_id = Column(Integer)               #:子用户ID
    Fpackage_name = Column(String(64),doc='套系名称')     #

    Fprice = Column(Integer,doc='原价')
    Fsale_price = Column(Integer,doc='现价')


    '''服装造型'''
    Fbride_style_count = Column(String(256),doc='新娘造型X套 单位是套')
    Fgroom_style_count = Column(String(256),doc='新郎造型X套 单位是套')
    Fcloth_select_type = Column(SmallInteger,doc='服装选择区域')  #服装选择类型  1.指定区域 2.全场任选
    Fcloth_remark = Column(String(512),doc='补充说明')

    '''拍摄地点说明'''
    Foutdoor_space = Column(String(512),doc='外景地')
    Finner_space = Column(String(512),doc='内景地')
    Fspace_remark = Column(String(512),doc='补充说明')

    '''团队服务、提供那些服务'''
    Fshot_desc = Column(String(512),doc='套系特色')
    Fphotographer_level = Column(String(256),doc='摄影师级别')
    Frecommend_photographer = Column(String(512),doc='推荐摄影师')       #多个用空格隔开
    Farter_level = Column(String(256),doc='化妆师级别')
    Frecommend_arter = Column(String(512),doc='推荐化妆师')              #多个用空格隔开

    '''附赠产品'''
    Fphoto_album_desc = Column(String(512),doc='相册')
    Fphoto_frame_desc = Column(String(512),doc='相框')
    Fmv_desc = Column(String(512),doc='相框')
    Fother_desc = Column(String(512),doc='其他描述')


    Fdescription = Column(Text,doc='套系补充说明')#
    Fother_pay_desc = Column(String(512),doc='其他补充说明')
    Fcover_img = Column(String(512),doc='封面图')
    Ffavorite_count = Column(Integer,default=0,doc='收藏数')
    Fis_activity = Column(Boolean,default=0)        #参加活动

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class ShotPackageImages(Base):
    '''
    套系图片
    '''
    __tablename__ = 't_shot_package_images'

    Fid = Column(Integer, primary_key=True)
    Fshot_package_id = Column(Integer,doc='产品 楼上表ID')

    Fimg_id = Column(Integer,doc='图片ID')
    Furl = Column(String(512),doc='图片请求地址',nullable=True)
    Fsort = Column(Integer,doc='图片显示排序',default=0)
    Fdescription = Column(String(512),doc="图片描述")

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class ShotPackagePreferential(Base):
    """
        套系优惠
    """
    __tablename__ = 't_shot_package_preferential'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)                                           #商户ID
    Fstart_time = Column(DateTime, default=now())   #起始时间
    Fend_time = Column(DateTime, default=now())                                        #截至时间

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class WeddingDressShotPackage(Base):
    """婚纱礼服套系
    """
    __tablename__ = 't_weddingdress_shot_package'

    Fid = Column(Integer, primary_key=True)
    Fpackage_name = Column(String(64), default='', doc='套系名称')

    Fmerchant_id = Column(Integer, nullable=False, doc='商家id')
    Fuser_id = Column(Integer, doc='子用户id')

    Fprice = Column(Float, default=0.0, doc='原价')
    Fsale_price = Column(Float, default=0.0, doc='现价')

    Ftype = Column(Enum('rent', 'sale'), default='rent', doc='租赁或购买')
    Ffreetrial = Column(Boolean, default=0, doc='0不可免费试纱, 1可免费试纱')

    Fcount = Column(Integer, default=0, doc='礼服数量')
    Fdescription = Column(String(512), default='', doc='礼服类别描述')
    Fextra = Column(Text(), default='', doc='补充说明')

    Fcover_img = Column(String(512), default='', doc='封面图')
    Ffavorite_count = Column(Integer, default=0, doc='收藏数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建时间')
    Fmodify_time = Column(DateTime, default=now(), doc='修改时间')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingDressShotPackage(id={0}, name={1})>'.format(self.Fid, self.Fpackage_name)


class WeddingDressShotPackageImage(Base):
    '''婚纱礼服套系里的图片
    '''
    __tablename__ = 't_weddingdress_shot_package_image'

    Fid = Column(Integer, primary_key=True)
    Fimg_id = Column(Integer, nullable=False, doc='图片ID')
    Fshot_package_id = Column(Integer, nullable=False, doc='表WeddingDressShotPackage的id')

    Furl = Column(String(512), nullable=False, doc='图片请求地址')
    Fsort = Column(Integer, default=0, doc='图片显示排序')
    Fdescription = Column(String(512), default='', doc="图片描述")

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingDressShotPackageImage(img_id={0}, url={1})>'.format(self.Fimg_id, self.Furl)


class WeddingDressPhotoProduct(Base):
    '''婚纱礼服的作品
    '''
    __tablename__ = 't_weddingdress_photo_product'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer, nullable=False, doc='商家ID')
    Fuser_id = Column(Integer, doc='子用户id')
    Fname = Column(String(256), default='', doc='名称')

    Fcategory = Column(String(64), default='', doc='分类')
    Fcolor = Column(String(64), default='', doc='颜色')
    Fstyle = Column(String(64), default='', doc='款式')

    Fsale_price = Column(Integer, default=0, doc='起拍价')

    Ftitle = Column(String(256), default='', doc='标题')
    Fdescription = Column(String(1024), default='', doc='描述')
    Fcover_img = Column(String(512), default='', doc='封面图')
    Ffavorite_count = Column(Integer, default=0, doc='收藏数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingDressPhotoProduct(id={0}, name={1})>'.format(self.Fid, self.Fname)


class WeddingDressPhotoProductImages(Base):
    '''婚纱礼服作品图片
    '''
    __tablename__ = 't_weddingdress_photo_product_images'

    Fid = Column(Integer, primary_key=True)
    Fphoto_product_id = Column(Integer, nullable=False, doc='WeddingDressPhotoProduct表ID')

    Fimg_id = Column(Integer,doc='图片ID')
    Furl = Column(String(512), default='', doc='图片请求地址')
    Fsort = Column(Integer, default=0, doc='图片显示排序')
    Fdescription = Column(String(512), default='', doc="图片描述")

    Fassist_count = Column(Integer, default=0, doc='赞的次数')
    Fcomments_count = Column(Integer, default=0, doc='评论次数')
    Fcollection = Column(Integer, default=0, doc='收藏次数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingDressPhotoProductImages(img_id={0}, url={1})>'.format(self.Fimg_id, self.Furl)

class WeddingCompanyShotPackage(Base):
    """婚庆公司套系
    """
    __tablename__ = 't_weddingcompany_shot_package'

    Fid = Column(Integer, primary_key=True)
    Fpackage_name = Column(String(64), default='', doc='套系名称')

    Fmerchant_id = Column(Integer, nullable=False, doc='商家id')
    Fuser_id = Column(Integer, doc='子用户id')

    Fprice = Column(Float, default=0.0, doc='原价')
    Fsale_price = Column(Float, default=0.0, doc='现价')

    #婚礼布置
    Fwelcome_area = Column(Text(), default='', doc='迎宾区')
    Fceremony_area = Column(Text(), default='', doc='仪式区')
    Freception_area = Column(Text(), default='', doc='婚宴区')
    Fequipment = Column(Text(), default='', doc='设备及灯光')
    Farrangement_extra = Column(Text(), default='', doc='婚礼布置补充说明')

    #鲜花装饰
    Fmeetingplace = Column(Text(), default='', doc='会场')
    Fbridegroom = Column(Text(), default='', doc='新郎')
    Fbride = Column(Text(), default='', doc='新娘')
    Fvip = Column(Text(), default='', doc='贵宾')
    Fflower_extra = Column(Text(), default='', doc='鲜花装饰补充说明')

    #仪式
    Fwedding_ceremony = Column(Text(), default='', doc='证婚仪式')
    Fbanquet_ceremony = Column(Text(), default='', doc='宴会仪式')
    Fceremony_extra = Column(Text(), default='', doc='仪式补充说明')

    #服务团队
    Fmaster = Column(Text(), default='', doc='司仪')
    Fmakeup = Column(Text(), default='', doc='化妆')
    Fphotography = Column(Text(), default='', doc='摄影')
    Fcamera = Column(Text(), default='', doc='摄像')
    Fservice_extra = Column(Text(), default='', doc='其他人员')

    Fextra = Column(Text(), default='', doc='补充说明')

    Fcover_img = Column(String(512), default='', doc='封面图')
    Ffavorite_count = Column(Integer, default=0, doc='收藏数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建时间')
    Fmodify_time = Column(DateTime, default=now(), doc='修改时间')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingCompanyShotPackage(id={0}, name={1})>'.format(self.Fid, self.Fpackage_name)


class WeddingCompanyShotPackageImage(Base):
    '''婚庆公司套系里的图片
    '''
    __tablename__ = 't_weddingcompany_shot_package_image'

    Fid = Column(Integer, primary_key=True)
    Fimg_id = Column(Integer, nullable=False, doc='图片ID')
    Fshot_package_id = Column(Integer, nullable=False, doc='表WeddingCompanyShotPackage的id')

    Furl = Column(String(512), nullable=False, doc='图片请求地址')
    Fsort = Column(Integer, default=0, doc='图片显示排序')
    Fdescription = Column(String(512), default='', doc="图片描述")

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingCompanyShotPackageImage(img_id={0}, url={1})>'.format(self.Fimg_id, self.Furl)


class WeddingCompanyPhotoProduct(Base):
    '''婚纱公司的作品
    '''
    __tablename__ = 't_weddingcompany_photo_product'

    Fid = Column(Integer, primary_key=True)
    Fmerchant_id = Column(Integer, nullable=False, doc='商家ID')
    Fuser_id = Column(Integer, doc='子用户id')
    Fname = Column(String(256), default='', doc='名称')

    Fcategory = Column(String(64), default='', doc='分类')
    Fcolor = Column(String(64), default='', doc='颜色')
    Fstyle = Column(String(64), default='', doc='款式')

    Fsale_price = Column(Integer, default=0, doc='起拍价')

    Ftitle = Column(String(256), default='', doc='标题')
    Fdescription = Column(String(1024), default='', doc='描述')
    Fcover_img = Column(String(512), default='', doc='封面图')
    Ffavorite_count = Column(Integer, default=0, doc='收藏数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingCompanyPhotoProduct(id={0}, name={1})>'.format(self.Fid, self.Fname)


class WeddingCompanyPhotoProductImages(Base):
    '''婚庆公司作品图片
    '''
    __tablename__ = 't_weddingcompany_photo_product_images'

    Fid = Column(Integer, primary_key=True)
    Fphoto_product_id = Column(Integer, nullable=False, doc='WeddingCompanyPhotoProduct表ID')

    Fimg_id = Column(Integer,doc='图片ID')
    Furl = Column(String(512), default='', doc='图片请求地址')
    Fsort = Column(Integer, default=0, doc='图片显示排序')
    Fdescription = Column(String(512), default='', doc="图片描述")

    Fassist_count = Column(Integer, default=0, doc='赞的次数')
    Fcomments_count = Column(Integer, default=0, doc='评论次数')
    Fcollection = Column(Integer, default=0, doc='收藏次数')

    Fcreate_time = Column(DateTime, default=now(), doc='创建日期')
    Fmodify_time = Column(DateTime, default=now(), doc='修改日期')
    Fdeleted = Column(Boolean, default=0)

    def __repr__(self):
        return '<WeddingCompanyPhotoProductImages(img_id={0}, url={1})>'.format(self.Fimg_id, self.Furl)