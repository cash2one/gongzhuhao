# encoding:utf-8
__author__ = 'binpo'

import tornado
from tornado.options import options
from common.base import BaseHandler
from utils.upload_utile import upload_to_oss
from services.ablums.photos_service import PhotosServices
from common.permission_control import company_permission_control
import ujson
import sys


from concurrent.futures import ThreadPoolExecutor
from functools import partial, wraps
EXECUTOR = ThreadPoolExecutor(max_workers=10)
def unblock(f):

    @tornado.web.asynchronous
    @wraps(f)
    def wrapper(*args, **kwargs):
        self = args[0]

        def callback(future):
            if future.result():
                self.write(future.result())
            self.finish()

        EXECUTOR.submit(
            partial(f, *args, **kwargs)
        ).add_done_callback(
            lambda future: tornado.ioloop.IOLoop.instance().add_callback(
                partial(callback, future)))

    return wrapper

album_service = PhotosServices()


def img_compression(img_size=0, img_type=''):
    '''
        jpg格式压缩
        原图:876K
        80q压缩:134
        43q压缩:70
        30q压缩:55
    '''
    img_size = img_size/1000
    if img_size > 4000:
        return '@50q_0r.jpg'
    elif img_size > 3000:
        return '@60q_0r.jpg'
    elif img_size > 2000:
        return '@65q_0r.jpg'
    elif img_size > 1000:
        return '@70q_0r.jpg'
    elif img_size > 500:
        return '@90q_0r.jpg'
    elif img_size < 300:
        return ''  # '@100q_0r.jpg'
    else:
        return '@80q_0r.jpg'


def img_qulities_compression(img_size=0, img_type=''):
    '''
        质量压缩率处理
    '''
    img_size = img_size/1000
    if img_size > 4000:
        return '50'
    elif img_size > 3000:
        return '60'
    elif img_size > 2000:
        return '65'
    elif img_size > 1000:
        return '70'
    elif img_size > 500:
        return '90'
    elif img_size < 300:
        return '100'  # '@100q_0r.jpg'
    else:
        return '80'

from conf.order_conf import _TYPE_ORDER
class PhotoUploadHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('photos_view')
    def get(self,ablum_id,is_exquisite=None, *args, **kwargs):
        album_service.set_db(self.db)
        photos = album_service.query_photos_by_ablum_id(ablum_id, self.get_current_user().get('Fmerchant_id'),True)
        album = album_service.query_album_by_id(self.get_current_user().get('Fmerchant_id'),ablum_id)
        order = album_service.get_order_by_album_id(self.get_current_user().get('Fmerchant_id'),ablum_id)
        rt_url='crm/photo/photo_upload_finish.html'
        self.echo(rt_url,{'ablum_id':ablum_id,'photos':photos,'order':order,'album':album,'_TYPE_ORDER':_TYPE_ORDER})

    @tornado.web.authenticated
    @company_permission_control('photos_edit')
    @unblock
    def post(self,ablum_id,is_exquisite=None, *args, **kwargs):
        """
        :todo 上传图片
        :param album_id 相册ID
        """
        try:
            rsp = {'files': [], 'stat': 'err', 'msg': ''}
            user_id = self.current_user.get('Fid')
            merchant_id = self.current_user.get('Fmerchant_id')

            album_service.set_db(self.db)
            if not ablum_id or not ablum_id.isdigit():
                rsp = {'msg': u'参数错误'}
                return self.write(rsp)

            if not album_service.check_album_permission(merchant_id,ablum_id): #检查有没有ablum_id对应的相册
                rsp['msg'] = "check failed"
                return self.write(rsp)

            ablum_name = album_service.get_ablum_name_by_ablum_id(ablum_id)
            file_prex = '/'.join(['album', 'users', ablum_id,'exquisite'])

            self.album_Fid = ablum_id
            self.merchant_id = merchant_id
            self.user_id = user_id
            self.album_service = album_service

            is_ok, filenames = upload_to_oss(
                self, options.IMG_BUCKET, param_name='files',
                file_type='img', file_prex=file_prex, max_size=30,
                water_mark=True,is_sort=True)
            if is_ok:
                rsp['files'] = filenames
                rsp['stat'] = 'ok'
                file_ids = album_service.album_add_photos(ablum_id,merchant_id,user_id, rsp['files'],is_exquisite=is_exquisite)
                rsp['files'][0]['id'] = file_ids
            else:
                rsp['stat'] = 'err'
                rsp['msg'] = filenames
            print 'rsp:',rsp
            return self.write(ujson.dumps(rsp))

        except Exception, e:
            
            return self.write(ujson.dumps({'state':'ok','url':''}))

class PhotosDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('photos_edit')
    def get(self,image_id, *args, **kwargs):
        data={'status':'ok','info':'删除成功'}
        try:
            album_service.set_db(self.db)
            album_service.delete_photo_by_photo_id(self.get_current_user().get('Fmerchant_id'),image_id)
        except Exception,e:
            data['status']='error'
            data['info']='删除失败:'+e.message

        self.write(ujson.dumps(data))




class MerchantProductUploadHandler(BaseHandler):

    @tornado.web.authenticated
    def post(self,product_type,*args, **kwargs):
        """
        :todo 上传图片
        :param album_id 相册ID
        """
        try:
            rsp = {'files': [], 'stat': 'err', 'msg': ''}
            user_id = self.current_user.get('Fid')
            merchant_id = self.current_user.get('Fmerchant_id')
            album_service.set_db(self.db)
            if product_type=='series':
                album_name=u'套系'
                album = album_service.get_album_by_album_name(album_name,merchant_id)
            elif product_type=='product':
                album_name=u'产品'
                album = album_service.get_album_by_album_name(album_name,merchant_id)
            else:
                album_name=u'其他'
                album = album_service.get_album_by_album_name(album_name,merchant_id)

            file_prex = '/'.join(['album', 'merchant', str(album.Fid)])

            self.album_Fid = album.Fid
            self.merchant_id = merchant_id
            self.user_id = user_id
            self.album_service = album_service

            is_ok,filenames = upload_to_oss(
                self, options.IMG_BUCKET, param_name='files',
                file_type='img', file_prex=file_prex, max_size=30,
                water_mark=True,is_sort=True)
            if is_ok:
                rsp['files'] = filenames
                rsp['stat'] = 'ok'
                rsp['files'][0]['id'] = ','.join(filenames[0].get('file_ids'))
            else:
                rsp['stat'] = 'err'
                rsp['msg'] = filenames
            return self.write(ujson.dumps(rsp))

        except Exception, e:
            
            return self.write(ujson.dumps(rsp))
