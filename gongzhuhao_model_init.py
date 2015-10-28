#encoding: utf-8
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, Date, TIMESTAMP, Float, Enum, Text
from sqlalchemy import create_engine
from sqlalchemy.sql.functions import now
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
import datetime

#from services.weddingdress.weddingdress_service import WeddingDressService
#from services.company.company_services import CompanyServices


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

class MySQLPingListener(object):

    def checkout(self, dbapi_con, con_record, con_proxy):
        from sqlalchemy.exc import DisconnectionError
        from _mysql_exceptions import OperationalError
        try:
            dbapi_con.ping()
        except OperationalError:
            raise DisconnectionError("Database server went away")

if __name__ == '__main__':


    engine = create_engine("mysql://root:123456@127.0.0.1:3306/db_gongzhuhao?charset=utf8",echo=False,
                           pool_size=25,
                           max_overflow=140,
                           pool_recycle=40,
                           pool_timeout=5,
                           listeners=[MySQLPingListener()])

    # 创建表
    Base.metadata.create_all(engine)


    # 表添加内容
    # session_factory = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
    # t = WeddingDressShotPackage()
    # t.Fpackage_name = '童话'
    # t.Fmerchant_id = 1
    # t.Fuser_id = 1
    # t.Fprice = 10000
    # t.Fsale_price = 5000
    # t.Ftype = 'rent'
    # t.Ffreetrial = 0
    # t.Fcount = 5
    # t.Fdescription = '主纱、出门纱、晚礼服、小礼服、伴娘服'
    # t.Fextra = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean euismod bibendum laoreet. Proin gravida dolor sit amet lacus accumsan et viverra justo commodo. Proin sodales pulvinar tempor. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Nam fermentum, nulla luctus pharetra vulputate, felis tellus mollis orci, sed rhoncus sapien nunc eget odio.'
    # t.Fcover_img = 'http://img.gongzhuhao.com/album/merchant/1040/183045hN5FdtIMGL1873.JPG'
    # t.Ffavorite_count = 0
    #
    # session_factory.add(t)
    # session_factory.commit()


    # 测试service
    # session_factory = scoped_session(sessionmaker(bind=engine, autoflush=True, autocommit=False))
    # service = WeddingDressService(session_factory())
    # print service.min_and_max_price(25)
    # service = CompanyServices(session_factory())
    # service.update_range_price(25, 300, 500)