#encoding:utf-8
__author__ = 'binpo'

from services.base_services import BaseService
from models.share_do import UserPhotosShare,ShareMusic,ShareImages,ShareWishes,\
    PotentialCustomer,MerchantShareWishes
from models.album_do import AdornPhotos,Photos,Albums
import datetime
class ShareServices(BaseService):

    def query_shares_by_user_id(self,user_id):
        '''
        :todo 根据用户获取用户分享列表
        :param user_id:
        :return:
        '''
        return self.db.query(UserPhotosShare).filter(
            UserPhotosShare.Fuser_id == user_id,
            UserPhotosShare.Fdeleted == 0
            )

    def query_shares_by_merchant_id(self,merchant_id):
        '''
        :todo 根据商户查询用户分享
        :param merchant_id:
        :return:
        '''
        return self.db.query(UserPhotosShare).filter(UserPhotosShare.Fmerchant_id==merchant_id).order_by('Fcreate_time desc')

    def update_share(self,album_id,**kwargs):
        '''
        todo:更新
        :param album_id:
        :return:
        '''
        query = self.db.query(UserPhotosShare).filter(UserPhotosShare.Fdeleted == 0,UserPhotosShare.Falbum_id == album_id)
        if query.count():
            query.update(kwargs)
            self.db.commit()

    def query_all_musics(self):
        return self.db.query(ShareMusic).filter(ShareMusic.Fdeleted==0).order_by('Fcreate_time desc')

    def create_share(self,**kwargs):
        user_photos_share = UserPhotosShare()
        user_photos_share.Fuser_id = kwargs.get('user_id')
        user_photos_share.Fmerchant_id = kwargs.get('Fmerchant_id')
        user_photos_share.Falbum_id = kwargs.get('album_id')
        user_photos_share.Ftitle = kwargs.get('title')
        user_photos_share.Fdescription = kwargs.get('description')
        user_photos_share.Fmusic_id = kwargs.get('music_id')
        user_photos_share.Fmusic_name = kwargs.get('music_name')
        user_photos_share.Fmusic_url = kwargs.get('music_url')
        user_photos_share.Fcover_img = kwargs.get('Fcover_img')
        user_photos_share.Forder_id = kwargs.get('Forder_id','')
        self.db.add(user_photos_share)
        self.db.commit()
        return user_photos_share

    def create_share_image(self,user_photo_share_id,photos):
        for photo in photos:
            share_images = ShareImages()
            share_images.Fuser_photos_share_id = user_photo_share_id
            share_images.Fimg_id = photo.Fid
            share_images.Fimg_url = photo.Fimage_url
            share_images.Fimg_size = photo.Fimage_size
            # share_images.Fsort = index
            self.db.add(share_images)
            self.db.commit()

    def create_share_photos(self,state,**kargs):

        adorm_photo = self.db.query(AdornPhotos).filter(AdornPhotos.Fid==kargs.get('cover')).scalar()

        user_photos_share = UserPhotosShare()
        user_photos_share.Fuser_id = kargs.get('user_id')
        user_photos_share.Falbum_id = kargs.get('album_id')

        album = self.db.query(Albums).filter(Albums.Fid==kargs.get('album_id')).scalar()
        if album:
            user_photos_share.Fmerchant_id = album.Fuid_mct
            user_photos_share.Forder_id = album.Forder_id
        user_photos_share.Ftitle = kargs.get('title','')
        user_photos_share.Fdescription = kargs.get('description','')
        music = self.get_music_by_id(kargs.get('bg_music',None))
        if music:
            user_photos_share.Fmusic_name = music.Fmusic_name                 #:音乐名称
            user_photos_share.Fmusic_url = music.Fmusic_url
            user_photos_share.Fmusic_id = music.Fid
        user_photos_share.Fcover_img = self.db.query(AdornPhotos.Fimage_url).filter(AdornPhotos.Fid==kargs.get('cover_id')).scalar()
        if state=='1':
            user_photos_share.Fdeleted=1
        self.db.add(user_photos_share)
        self.db.commit()
        images=[]
        images_id_str = kargs.get('images',None)
        images_id_str = images_id_str.replace('[','')
        images_id_str = images_id_str.replace(']','')
        images_id_str = images_id_str.replace("'",'')
        images_id_str = images_id_str.split(',')
        for img_id in images_id_str:
            if not img_id:
                continue
            if kargs.get('cover_id',None):
                if img_id !=kargs.get('cover_id'):
                    photo_img = self.db.query(AdornPhotos.Fimage_url).filter(AdornPhotos.Fid==img_id).scalar()
                    if not photo_img:
                        continue
                    share_images = ShareImages()
                    share_images.Fuser_photos_share_id = user_photos_share.Fid
                    share_images.Fimg_url = photo_img
                    share_images.Fimg_id = int(img_id)
                    self.db.add(share_images)
            else:
                photo_img = self.db.query(AdornPhotos.Fimage_url).filter(AdornPhotos.Fid==img_id).scalar()
                if not photo_img:
                    continue
                share_images = ShareImages()
                share_images.Fuser_photos_share_id = user_photos_share.Fid
                share_images.Fimg_url = photo_img
                share_images.Fimg_id = int(img_id)
                self.db.add(share_images)
        self.db.commit()
        return user_photos_share,images



    def get_music_by_id(self,musict_id):
        '''
        :todo根据id查询北京音乐信息
        :param musict_id:
        :return:
        '''
        if musict_id:
            try:
                return self.db.query(ShareMusic).filter(ShareMusic.Fid==musict_id).scalar()
            except:
                return None
        else:
            return None


    def get_by_id(self, _id, is_preview=0):
        '''
        :todo 根据ID查询
        :param _id:
        :return:
        '''
        return self.db.query(UserPhotosShare).filter(
            UserPhotosShare.Fdeleted == is_preview,
            UserPhotosShare.Fid == _id).scalar()


    def get_images_by_id(self,_share_id):
        '''
        :todo 根据分享ID查询分线图片
        :param user_share_id:
        :return:
        '''
        return self.db.query(ShareImages).filter(ShareImages.Fdeleted==0,ShareImages.Fuser_photos_share_id==_share_id).order_by('Fsort')

    def get_wishs_by_share_id(self,_share_id):
        '''
        :todo 根据id查询祝福
        :param _share_id:
        :return:
        '''
        return self.db.query(ShareWishes).filter(ShareWishes.Fdeleted==0,ShareWishes.Fuser_photos_share_id==_share_id)


    def count_share_wishes(self,user_share_id):
        '''
        :todo 祝福统计信息
        :param user_share_id:
        :return:
        '''
        return self.db.query(ShareWishes).filter(ShareWishes.Fdeleted==0,ShareWishes.Fuser_photos_share_id==user_share_id).count()


    def commit_wishes(self, **kwargs):
        '''
        :todo 祝福提交
        :param 祝福信息:
        :return:
        '''
        weixin_user = kwargs.get('weixin')
        if weixin_user:
            check_open_id = str(weixin_user.get('view_weixin_openid')).strip()
            _share_wish = self.db.query(ShareWishes).filter(ShareWishes.Fweixin_id==check_open_id,ShareWishes.Fuser_photos_share_id==kwargs.get('Fshare_id')).scalar()
            if _share_wish:
                wish=_share_wish
                wish.Fmodify_time = datetime.datetime.now()
            else:
                wish = ShareWishes()
        else:
            wish = ShareWishes()

        wish.Fuser_id = kwargs.get('Fuser_id')
        wish.Fuser_photos_share_id = kwargs.get('Fshare_id')
        wish.Fwish_content = kwargs.get('Fcontent','')

        if kwargs.get('weixin',None):
            user = kwargs.get('weixin')
            wish.Fweixin_id = str(user.get('view_weixin_openid','')).strip()
            if not wish.Fsend_user:
                wish.Fsend_user = user.get('nick_name','')
            wish.Fweixin_photos = user.get('photo','')
        self.db.add(wish)
        self.db.commit()

        return wish

    def commit_potential(self,**kwargs):

        cust = PotentialCustomer()

        cust.Fuser_photos_share_id = kwargs.get('Fshare_id')
        cust.Fshare_user_id = kwargs.get('Fuser_id')
        cust.Fshare_name = kwargs.get('Fuser_name')  # 用户名称
        cust.Fmerchant_id = kwargs.get('Fmerchant_id')
        cust.Fcompany_id = kwargs.get('Fcompany_id')
        cust.Fpotential_customer_name = kwargs.get('Fsend_user')
        cust.Fpotential_customer_phone = kwargs.get('Fcust_phone')
        self.db.add(cust)
        self.db.commit()
        return cust


    def get_wish_by_weixin_and_share_id(self,share_id,weixin_id):
        '''
        :todo 根据微信和分享ID查询祝福
        :param share_id:
        :param weixin_id:
        :return:
        '''
        query = self.db.query(ShareWishes).\
            filter(ShareWishes.Fdeleted==0,ShareWishes.Fweixin_id==weixin_id,ShareWishes.Fuser_photos_share_id==share_id)
        if query.count()>0:
            return 1
        else:
            return 0

    def create_merchant_wishes(self,**kwargs):
        '''
        todo:添加商户祝福语言
        :param kwargs:
        :return:
        '''
        merchant_share_wishes = MerchantShareWishes()
        merchant_share_wishes.Fmerchant_id = kwargs.get('Fuid_mct','')
        #merchant_share_wishes.Fuser_id = kwargs.get('Fuser_id','')
        #merchant_share_wishes.Fmerchant_share_id = kwargs.get('Fmerchant_share_id','')
        merchant_share_wishes.Foperation_id = kwargs.get('Foperation_id','')
        merchant_share_wishes.Fwishes_type = kwargs.get('Fwishes_type','')
        merchant_share_wishes.Fwishes_content = kwargs.get('Fwishes_content','')
        self.db.add(merchant_share_wishes)
        self.db.commit()

    def update_merchant_wishes(self,merchant_wishes_id,**kwargs):
        '''
        todo:更新商户祝福
        :param merchant_wishes_id:
        :return:
        '''
        query = self.db.query(MerchantShareWishes).filter(MerchantShareWishes.Fdeleted == 0,MerchantShareWishes.Fid == merchant_wishes_id)
        query.update(kwargs)
        self.db.commit()

    def get_merchant_wishes(self,uid_mct,s_type=None):
        '''
        todo:获取商户祝福
        :param uid_mct:
        :return:
        '''
        query = self.db.query(MerchantShareWishes).filter(MerchantShareWishes.Fdeleted == 0,MerchantShareWishes.Fmerchant_id == uid_mct)
        if s_type:
            query = query.filter(MerchantShareWishes.Fwishes_type==s_type)
        return query



