# encoding:utf-8
__author__ = 'binpo'

from ..base_services import BaseService
from models.album_do import Albums, Photos, AdornPhotos, OrderPic
from models.order_do import Orders
from sqlalchemy import or_

class PhotosServices(BaseService):

    def add_photos_by_ablum_id(self, ablum_id, user_id,**kargs):
        return self.db.query(Photos).filter(Photos.Fdeleted==0,Photos.Falbum_id==ablum_id,Photos.Fuid_mct==ablum_id).order_by('Fcreate_time desc')

    def check_album_permission(self, uid_mct, ablum_id):
        '''
        :param uid_mct:
        :param ablum_id:
        :return:
        '''
        """ 检查相册权限"""
        return self.db.query(Albums.Fid).filter(
            Albums.Fuid_mct == uid_mct,
            Albums.Fid == ablum_id,
            Albums.Fdeleted == 0).scalar()

    def get_ablum_ablum_id(self,ablum_id,user_id=None):
        if user_id:
            return self.db.query(Albums).filter(
                Albums.Fdeleted == 0,
                Albums.Fid == ablum_id,Albums.Fuser_id==user_id).scalar()
        else:
            return self.db.query(Albums).filter(Albums.Fid == ablum_id,Albums.Fdeleted == 0).scalar()

    def get_ablum_name_by_ablum_id(self, ablum_id):
        return self.db.query(Albums.Fablum_name).filter(
            Albums.Fdeleted == 0,
            Albums.Fid == ablum_id).scalar()

    def album_add_photos(
            self, ablum_id, merchant_id, user_id, files,
            order_user_id=None,
            is_exquisite=False,
            is_order_pic=False,
            is_user_tweet=False,
            order_id=''):
        '''
        :todo 创建相册
        :param ablum_id:
        :param merchant_id:
        :param user_id:
        :param files:
        :param order_user_id:
        :param is_exquisite:
        :param is_order_pic: 是否是手机上传的订单图片
        :param is_user_tweet: 是否是用户上传的分享心情图片
        :return:
        '''
        album = self.db.query(Albums).filter(Albums.Fid==ablum_id).first()

        file_ids = []
        for f in files:
            if is_exquisite:
                img = AdornPhotos()
            else:
                img = Photos()

            if is_order_pic:  # 商户手机端建订单
                img = OrderPic()
                img.Forder_id = order_id
                img.Fimage_type = 'order_pic'

            if is_user_tweet:  # 用户在每个阶段发表的心情
                img = OrderPic()
                img.Forder_id = order_id
                img.Fimage_type = 'user_tweet'

            img.Falbum_id = ablum_id
            img.Fuid_mct = merchant_id          # 商户ID
            img.Fuser_id = album.Fuser_id       # 用户ID
            img.Foperation_id = user_id
            img.Fimage_name = f.get('name')
            img.Ffull_name = f.get('full_name')  # 图片存储地址
            img.Fimage_size = f.get('size')
            img.Fimage_url = f.get('url')  # 图片请求URL
            self.db.add(img)
            self.db.commit()
            if not album.Furl_pic_cover:
                album.Furl_pic_cover = f.get('url')
            file_ids.append(str(img.Fid))
        self.db.commit()

        return file_ids

    def query_photos_by_ablum_id(self,ablum_id, user_id,is_exquisite):
        '''
        获取相册图片
        :param ablum_id:
        :param user_id: 商户ID
        :return:
        '''
        # print user_id
        # print is_exquisite
        if is_exquisite:
            return self.db.query(AdornPhotos).filter(AdornPhotos.Fdeleted==0,AdornPhotos.Falbum_id==ablum_id,AdornPhotos.Fuid_mct==user_id).order_by('Fcreate_time desc')
        return self.db.query(Photos).filter(Photos.Fdeleted==0,Photos.Falbum_id==ablum_id,Photos.Fuid_mct==user_id).order_by('Fcreate_time desc')

    def query_photos_by_ablum_id2(self,user_id,album_id):
        '''
        todo:根据相册id获取照片数量
        :param ablum_id:相册id
        :return:
        '''
        query = self.db.query(AdornPhotos).filter(AdornPhotos.Fdeleted==0,AdornPhotos.Falbum_id == album_id,AdornPhotos.Fuser_id == user_id)
        return query


    def get_order_by_album_id(self,merchant_id,album_id):
        '''
        根据相册ID获取订单信息
        :param album_id:
        :return:
        '''
        order_id = self.db.query(Albums.Forder_id).filter(Albums.Fdeleted==0,Albums.Fuid_mct==merchant_id,Albums.Fid==album_id).scalar()
        return self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fid==order_id).scalar()


    def get_album_by_order(self, merchant_id, order_id):
        '''
        根据订单信息获取相册ID
        :param order_id:
        :return:
        '''
        return self.db.query(Albums).filter(
            Albums.Fdeleted == 0,
            Albums.Fuid_mct == merchant_id,
            Albums.Forder_id == order_id).scalar()

    def get_album_by_order_id(self, order_id):
        '''
        根据订单信息获取相册ID
        :param order_id:
        :return:
        '''
        return self.db.query(Albums).filter(
            Albums.Fdeleted == 0,
            Albums.Forder_id == order_id).scalar()

    def query_photos_by_ablum_user_id(self,ablum_id, user_id):
        '''
        :获取用户相册图片
        :param ablum_id:
        :param user_id:
        :return:
        '''
        return self.db.query(AdornPhotos).\
            filter(AdornPhotos.Fdeleted==0,AdornPhotos.Falbum_id==ablum_id,AdornPhotos.Fuser_id==user_id)

    def query_album_list_by_merchant_id(self,merchant_id,search_context=None):
        '''
        :todo根据商户获取相册
        :param merchant_id:
        :return:
        '''
        query = self.db.query(Albums).filter(Albums.Fdeleted==0,Albums.Forder_id!=None,Albums.Fuid_mct==merchant_id)
        #Fuser_mobi,Forder_id_user

        if search_context and search_context.strip():
            order_ids = self.db.query(Orders.Fid).filter(Orders.Fdeleted==0).filter(or_(Orders.Fuser_mobi.like('%{0}%'.format(search_context)),Orders.Forder_id_user.like('%{0}%'.format(search_context))))
            #query(Orders.Fid).filter(Orders.Fdeleted==0).filter(or_(Orders.Fuser_mobi.like('%{0}%').format(search_context),Orders.Forder_id_user.like('%{0}%').format(search_context)))
            id_list = [int(d[0]) for d in order_ids ]
            if id_list:
                query = query.filter(or_(Albums.Fablum_name.like('%{0}%'.format(search_context)),Albums.Forder_id.in_(id_list)))
            else:
                query = query.filter(Albums.Fablum_name.like('%{0}%'.format(search_context)))
        return query.order_by('Fcreate_time desc')

    def query_album_by_user_id(self, user_id):
        '''
        :todo根据用户获取用户的相册列表
        :param user_id:
        :return:
        '''
        query = self.db.query(Albums).\
            filter(Albums.Fdeleted == 0,Albums.Fuser_id == user_id).order_by('Fcreate_time desc').all()
        return query

    def query_user_album_by_status(self,user_id,status):
        '''
        :todo根据用户和相册状态查询相册
        :param user_id:
        :param status:
        :return:
        '''
        return self.db.query(Albums).filter(Albums.Fdeleted==0,Albums.Fuser_id==user_id,Albums.Fstatus==status)

    def query_album_by_id(self,merchant_id,album_id):
        '''
        :根据相册ID获取相册
        :param user_id:
        :param status:
        :return:
        '''
        return self.db.query(Albums).filter(Albums.Fdeleted==0,Albums.Fuid_mct==merchant_id,Albums.Fid==album_id).scalar()#.order_by('Fcreate_time desc')

    def query_album_by_user_id(self,user_id,album_id):
        '''
        :根据 用户ID 相册ID获取相册
        :param user_id:
        :param status:
        :return:
        '''
        return self.db.query(Albums).filter(Albums.Fdeleted==0,Albums.Fuser_id==user_id,Albums.Fid==album_id).scalar()#.order_by('Fcreate_time desc')


    def delete_photo_by_photo_id(self,merchant_id,photo_id):
        '''
        :todo删除单张图片
        :param merchant_id:
        :param photo_id:
        :return:
        '''
        img = self.db.query(AdornPhotos).filter(AdornPhotos.Fid==photo_id,AdornPhotos.Fuid_mct==merchant_id).scalar()
        img.Fdeleted=1#,synchronize_session=False)
        self.db.commit()

        # if photo:
        #     photo.Fdeleted=1
        #     self.db.add(photo)#.save()
        #     # albums = self.db.query(Albums).filter(Albums.Fid==photo.Falbum_id,Albums.Fuid_mct==merchant_id).scalar()
        #     # if albums.Ftotal==0:
        #     #     pass
        #     # else:albums.Ftotal = albums.Ftotal-1
        #     # self.db.add(albums)#.save()


    def get_album_by_album_name(self,album_name,merchant_id):
        '''
        :todo根据相册名称查询相册
        :param album_name:
        :param merchant_id:
        :return:
        '''
        album = self.db.query(Albums).filter(Albums.Fuid_mct==merchant_id,Albums.Fablum_name==album_name).first()
        if not album:
            album = Albums()
            album.Fuid_mct = merchant_id
            album.Fablum_name = album_name
            self.db.add(album)
            self.db.commit()
        return album
    def query_albums(self,merchant_id,**kwargs):
        '''
        todo:获取相册
        :param kwargs:
        :return:
        '''
        query = self.db.query(Albums).filter(Albums.Fdeleted == 0,Albums.Fuid_mct == merchant_id)
        if kwargs.get('start_date',''):
            query = query.filter(Albums.Fcreate_time > kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(Albums.Fcreate_time < kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('albums_status',''):
            query = query.filter(Albums.Fstatus == kwargs.get('albums_status'))
        if kwargs.get('album_name',''):
            content = kwargs.get('album_name')
            query = query.filter(Albums.Fablum_name.like('%'+content+'%'))
        return query

    def query_photos(self,album_id,merchant_id):
        query = self.db.query(AdornPhotos).\
            filter(AdornPhotos.Falbum_id == album_id,AdornPhotos.Fuid_mct == merchant_id,AdornPhotos.Fdeleted == 0)
        return query

    def create_albums(self,order_id,merchant_id,album_name,album_type):
        album = Albums()
        album.Forder_id = order_id
        album.Fuid_mct = merchant_id
        album.Fablum_name = album_name
        album.Falbum_type = album_type
        self.db.add(album)
        self.db.commit()

    def get_album_type_by_album_id(self,album_id):
        '''
        :todo 根据ID查询相册类型
        :param album_id:
        :return:
        '''
        return self.db.query(Albums.Falbum_type).filter(Albums.Fdeleted==0,Albums.Fid==album_id).scalar()

    def get_album_by_name(self,user_id,name='默认相册'):
        '''
        :根据相册名称查找相册
        :param user_id:
        :param name:
        :return:
        '''
        query = self.db.query(Albums).filter(Albums.Fdeleted==0,Albums.Fablum_name==name)
        if query.count()>0:
            return query.first()
        else:
            album = Albums()
            album.Fuser_id = user_id
            album.Fablum_name = name
            self.db.add(album)
            self.db.commit()
            return album

    def delete_photo(self, **kwargs):
        query = self.db.query(Photos).filter(Photos.Fdeleted==0)

        if kwargs.get('photo_id'):
            query = query.filter(Photos.Fid==kwargs.get('photo_id')).update({Photos.Fdeleted: 1})

        self.db.commit()