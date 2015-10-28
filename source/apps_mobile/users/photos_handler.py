# encoding:utf-8
__author__ = 'jinkuan'

import tornado
from services.users.user_services import UserServices
from services.ablums.photos_service import PhotosServices
from services.music.music_service import MusicServices
from apps_mobile.mobile_base import MobileBaseHandler
from common.permission_control import Mobile_login_control
from utils.datetime_util import datetime_format
import ujson
import sys

user_service = UserServices()
photos_service = PhotosServices()
music_service = MusicServices()

class WxAlbumPhotosHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self):
        uid = self.get_current_user().get('Fid')
        photos_service.set_db(self.db)
        try:
            albums = photos_service.query_user_album_by_status(uid,1)
            lstdata = []
            for album in albums:
                dictionary = {}
                dictionary['id'] = album.Fid
                dictionary['album_name'] = album.Fablum_name
                dictionary['album_cover_url'] = self.get_show_img_url(album.Furl_pic_cover,600)
                dictionary['photo_list_url'] = '/mobile/user/album/list/'+str(album.Fid)+'/'
                dictionary['create_time'] = datetime_format(format='%Y-%m-%d',input_date = album.Fcreate_time)
                lstdata.append(dictionary)
        except Exception,e:
            pass
            return self.write(ujson.dumps({'stat':'1001','data':{},'list':[],'info':'获取相册失败,失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','data':{},'list':lstdata,'info':''}))


class AlbumPhotosListHandler(MobileBaseHandler):

    #相片列表
    @Mobile_login_control()
    def get(self, album_id, *args, **kwargs):
        photos_service.set_db(self.db)
        try:
            user_id = self.get_current_user().get('Fid')
            photos = photos_service.query_photos_by_ablum_user_id(album_id,user_id)
            lstdata = []
            for photo in photos:
                dictionary = {}
                dictionary['id'] = photo.Fid
                dictionary['album_id'] = photo.Falbum_id
                dictionary['photo_url'] = self.get_show_img_url(photo.Fimage_url,400)
                dictionary['photo_href'] = photo.Fimage_url
                dictionary['share_href'] = '/mobile/user/album/detail/'+str(photo.Falbum_id)+'/'
                lstdata.append(dictionary)
        except Exception,e:
            pass
            return self.write(ujson.dumps({'stat':'1001','data':'','list':[],'info':'获取相片失败，失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','data':{},'list':lstdata,'info':''}))


class AlbumPhotosDetailHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self, album_id, *args, **kwargs):
        photos_service.set_db(self.db)
        music_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        try:
            photos = photos_service.query_photos_by_ablum_user_id(album_id,user_id)
            album = photos_service.query_album_by_user_id(user_id,album_id)
            lstdata = []
            for photo in photos:
                dictionary = {}
                dictionary['id'] = photo.Fid
                dictionary['photo_url'] = self.get_show_img_url(photo.Fimage_url,600)
                dictionary['photo_href'] = self.get_show_img_url(photo.Fimage_url,600)
                lstdata.append(dictionary)
        except Exception,e:
            pass
            return self.write(ujson.dumps({'stat':'1001','data':{},'list':[],'info':'分享失败,失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','data':{'album_id':album.Fid},'list':lstdata,'info':''}))

