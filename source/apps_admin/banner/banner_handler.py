#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from common.cache_base import AdminCacheHandler
from services.banner.banner_service import BannerService
from utils.upload_utile import upload_to_oss
from tornado.options import options
from utils.datetime_util import datetime_format
import sys
import ujson

banner_service = BannerService()

class BannerTypeHandler(AdminBaseHandler):

    def get(self):
        self.echo('ops/banner/banner_type.html')

    def post(self,*args, **kwargs):
        rsg = {'stat':'error','info':''}
        self.get_paras_dict()

        print 'banner_type:',self.qdict

        banner_service.set_db(self.db)
        if not self.qdict.get('banner_code') or not self.qdict.get('banner_name'):
            rsg['info'] = '请将banner名称和code填写完整'
            return self.write(ujson.dumps(rsg))
        if self.qdict.get('banner_code') and banner_service.get_banner_type_by_code(self.qdict.get('banner_code').strip()):
            rsg['info'] = 'banner_code不能重复'
            return self.write(ujson.dumps(rsg))
        try:
            banner_service.create_banner_type(**self.qdict)
        except Exception,e:
            rsg['info'] = e.message
        rsg['stat'] = 'ok'
        rsg['info'] = '创建成功'
        self.write(ujson.dumps(rsg))

class BannerTypeListHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):

        banner_service.set_db(self.db)
        try:
            banner_types = banner_service.get_banner_type_list()
            self.echo('ops/banner/banner_types.html',{'banner_types':banner_types})
        except Exception,e:

            self.echo('ops/500.html')

class CreateBannerHandler(AdminBaseHandler,AdminCacheHandler):

    def get(self, *args, **kwargs):

        banner_service.set_db(self.db)
        banner_types = banner_service.get_banner_type_list()
        self.echo('ops/banner/banner.html',{'banner_types':banner_types})

    def post(self, *args, **kwargs):
        rsg = {'stat':'error','info':""}
        self.get_paras_dict()
        banner_service.set_db(self.db)
        try:
            if self.request.files.get('banner_img'):
                file_prex = 'music/'+datetime_format(format="%Y%m%d%H%M")
                is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET, param_name='banner_img',file_type='img',file_prex=file_prex)
                if is_ok:
                    for file in filenames:
                        img_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                        self.qdict['img_url'] = img_url
                else:
                    return self.write(ujson.dumps({'stat':'1005','info':'图片上传失败'}))
            banner = banner_service.create_banner(**self.qdict)
            self.delete_banner(banner.Fbanner_code)
        except Exception,e:

            rsg['info'] = e.message
            self.write(ujson.dumps(rsg))
        rsg['stat'] = 'ok'
        rsg['info'] = '创建成功'
        self.write(ujson.dumps(rsg))

class BannerListHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):

        banner_service.set_db(self.db)
        try:
            banners = banner_service.query_banner()
            self.echo('ops/banner/banners.html',{'banners':banners})
        except Exception,e:

            self.echo('ops/500.html')















