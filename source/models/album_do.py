# encoding:utf-8
from models.base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger, Date, TIMESTAMP
from sqlalchemy.sql.functions import now
from sqlalchemy import event



'''
拍摄风格
时尚 清新 特色 韩式 复古
拍摄场景
花海 外景 特色 实景基地
婚纱礼服
婚纱 便装 礼服 裙子 情侣装 特色
'''


class PhotoStyles(Base):

    __tablename__ = 't_photo_styles'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(128))
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=False)


class PhotoPlaces(Base):

    __tablename__ = 't_photo_places'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(128))
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=False)


class PhotoClothStyle(Base):

    __tablename__ = 't_photo_cloth_style'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(128))
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=False)


class Albums(Base):
    """相册信息表"""
    __tablename__ = 't_albums'

    Fid = Column(Integer, primary_key=True)       # 主键
    Forder_id = Column(String(32),nullable=True)    # 订单ID(内部)
    Fuid_mct = Column(String(16), nullable=False)       # 商户ID
    Fuser_id = Column(Integer)                                      # 用户ID
    Foperation_id = Column(Integer, nullable=True)                          #操作人ID

    Fablum_name = Column(String(128), doc='相册名称')
    Falbum_type = Column(String(32),doc='相册类型',nullable=True)   #订单类型
    Fpic_type = Column(SmallInteger, default=0)    # 图片类型
    Fclass = Column(SmallInteger, default=0)       # 拍摄类型
    Fstyle = Column(SmallInteger, default=0)       # 拍摄风格
    Fsite = Column(String(128), default='', server_default='')         # 拍摄场地
    Ftotal = Column(Integer,default=0)
    Furl_pic_cover = Column(String(512), default='', server_default='')  # 封面图片地址
    Fstatus = Column(SmallInteger, doc='状态',default=0)          #   #静修图状态  0:未发送，1:已发送
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(DateTime, default=now())
    Fdeleted = Column(Boolean, default=0)


class Photos(Base):
    """原图信息"""
    __tablename__ = 't_photoes'

    Fid = Column(Integer, primary_key=True)
    Falbum_id = Column(Integer, default=0)  #所属相册ID
    Fuid_mct = Column(Integer)                                  #商户ID
    Foperation_id = Column(Integer, nullable=True)                          #操作人ID
    Fuser_id = Column(Integer)                                              #用户ID
    Fimage_name = Column(String(128), default='', doc='名称')
    Ffull_name = Column(String(256), default='', server_default='')  # 图片存储地址
    Fimage_size = Column(String(128), default='', doc='图片大小')
    Fimage_url = Column(String(256), default='', server_default='')  # 图片请求URL
    Fis_selected = Column(Boolean, default=0, doc='是否选择')  # 用户选择图片
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class AdornPhotos(Base):
    """修饰后图片信息"""
    __tablename__ = 't_adorn_photos'

    Fid = Column(Integer, primary_key=True)
    Falbum_id = Column(Integer, default=0)  #所属相册ID
    Fuid_mct = Column(Integer)      #商户ID
    Fuser_id = Column(Integer)                  #用户ID
    Foperation_id = Column(Integer, nullable=True)                          #操作人ID

    Fimage_name = Column(String(128), default='', doc='名称')
    Ffull_name = Column(String(256), default='')  #图片存储地址
    Fimage_size = Column(String(128), default='', doc='图片大小')
    Fimage_url = Column(String(256), default='')  #图片请求URL
    Fstatus = Column(SmallInteger,default=0)        #静修图状态  0:未发送，1:已发送
    Fphoto_style_tags = Column(String(256), default='')  #风格名称  可以是多个标签
    Fphoto_place_tags = Column(String(256), default='')  #拍摄地点   可以是多个标签
    Fphoto_cloth_style_tags = Column(String(256), default='', server_default='')  #服饰风格  可以是多个标签

    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


class OrderPic(Base):
    """订单照片信息"""
    __tablename__ = 't_order_pic'

    Fid = Column(Integer, primary_key=True)
    Falbum_id = Column(Integer, default=0)  # 所属相册ID
    Forder_id = Column(String(32), nullable=True)       # 订单ID(内部)
    Fuid_mct = Column(Integer)              # 商户ID
    Foperation_id = Column(Integer, nullable=True)      # 操作人ID
    Fuser_id = Column(Integer)                          # 用户ID
    Fimage_type = Column(String(128), default='', doc='类型')  # 图片类型
    Fimage_name = Column(String(128), default='', doc='名称')
    Ffull_name = Column(String(256), default='', server_default='')  # 图片存储地址
    Fimage_size = Column(String(128), default='', doc='图片大小')
    Fimage_url = Column(String(256), default='', server_default='')  # 图片请求URL
    Fis_selected = Column(Boolean, default=0, doc='是否选择')  # 用户选择图片
    Fcreate_time = Column(DateTime, default=now())
    Fmodify_time = Column(TIMESTAMP, default=now())
    Fdeleted = Column(Boolean, default=0)


@event.listens_for(AdornPhotos, "after_insert", propagate=True)
def img_add_listener(mapper,conn,object):

    # object.Fuid_mct
    sql = "update t_albums set Ftotal=(select count(Fid) from t_adorn_photos where Fdeleted!=1 and Falbum_id=%s ) where Fid=%s"
    connection=conn.connect()
    sql = sql%(str(object.Falbum_id),str(object.Falbum_id))
    connection.execute(sql)
    connection.close()

@event.listens_for(AdornPhotos, 'after_update',propagate=True)
def after_update_img_listener(mapper, conn, target):
    sql = "update t_albums set Ftotal=(select count(Fid) from t_adorn_photos where Fdeleted!=1 and Falbum_id=%s ) where Fid=%s"
    connection=conn.connect()
    sql = sql%(str(target.Falbum_id),str(target.Falbum_id))
    connection.execute(sql)
    if target.Fdeleted==1:
        album = connection.execute('select Furl_pic_cover from t_albums where Fid=%s'%(target.Falbum_id)).fetchall()#.filter(Albums.Fid==target.Falbum_id).scalar()
        if album[0][0]==target.Fimage_url:
            photos = connection.execute('select Fimage_url from  t_adorn_photos where Fdeleted=0 and Falbum_id=%s'%(target.Falbum_id)).fetchall()
                #.filter(AdornPhotos.Fdeleted==0,AdornPhotos.Falbum_id==target.Falbum_id)
            if photos:
                update_cover_sql = 'update t_albums set Furl_pic_cover=(select Fimage_url from t_adorn_photos where Fdeleted=0 and Falbum_id=%s limit 1) where Fid=%s'%(target.Falbum_id,target.Falbum_id)
                connection.execute(update_cover_sql)
            else:
                update_cover_sql = 'update t_albums set Furl_pic_cover="" where Fid=%s'%(target.Falbum_id)

    connection.close()
#
# @event.listens_for(TopicImages, 'after_insert')
# def after_insert_listener(mapper, conn, target):
#     connection=conn.connect()
#     sql = 'update t_topics set Ftotal_img=Ftotal_img+1 where Fid='+str(target.Ftopic_id)
#     connection.execute(sql)
#     connection.close()
