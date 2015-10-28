#encoding: utf-8
__author__ = 'hongjiongteng'

import sys
import ujson
import tornado
from common.base import BaseHandler
from common.permission_control import company_permission_control
from services.weddingdress.weddingdress_service import WeddingDressSeriesService, WeddingDressWorkService
from services.company.company_services import CompanyServices
from services.ablums.photos_service import PhotosServices
from conf.work_conf import _WEDDING_DRESS_CATEGORY, _WEDDING_DRESS_COLOR, _WEDDING_DRESS_STYLE


class WeddingDressSeriesListHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_view')
    def get(self, *args, **kwargs):
        try:
            merchant_id = self.get_current_user().get('Fmerchant_id')
            series_service = WeddingDressSeriesService(self.db)
            series = series_service.query_series(merchant_id=merchant_id)

            self.echo('crm/weddingdress/series_list.html', {'series': series})
        except Exception, e:
            self.captureException(*sys.exc_info())


class WeddingDressSeriesAddHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, *args, **kwargs):
        try:
            self.echo('crm/weddingdress/series_add.html')
        except Exception, e:
            self.captureException(*sys.exc_info())

    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def post(self, *args, **kwargs):
        self.get_paras_dict()
        self.qdict['merchant_id'], self.qdict['user_id'] = self.current_user.get('Fmerchant_id'), self.current_user.get('Fid')

        try:
            series_service = WeddingDressSeriesService(self.db)

            series_service.add_series(**self.qdict)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            #删除套系数量缓存
            self.delete_package_count(self.current_user.get('Fmerchant_id'))
            self.delete_essence()

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressSeriesEditHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, series_id):
        try:
            series_service = WeddingDressSeriesService()
            series_service.set_db(self.db)

            series = series_service.query_series(series_id=series_id).scalar()
            images = series_service.query_series_images(series_id=series_id).all()
            self.echo('crm/weddingdress/series_edit.html', {'series': series, 'images': images})

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))

        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())

    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def post(self, series_id):
        self.get_paras_dict()
        self.qdict['merchant_id'], self.qdict['user_id'] = self.current_user.get('Fmerchant_id'), self.current_user.get('Fid')

        try:
            series_service = WeddingDressSeriesService()
            series_service.set_db(self.db)

            series_service.update_series(series_id, **self.qdict)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressSeriesDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def post(self, series_id):
        try:
            series_service = WeddingDressSeriesService()
            series_service.set_db(self.db)

            series_service.delete_series(series_id)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            #删除套系数量缓存
            self.delete_package_count(self.current_user.get('Fmerchant_id'))
            self.delete_essence()

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressSeriesDeleteImgHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, img_id):
        try:
            series_service, album_service = WeddingDressSeriesService(self.db), PhotosServices(self.db)

            #删除套系图片
            series_service.delete_series_images(img_id=img_id)

            #删除相册图片
            album_service.delete_photo(photo_id=img_id)

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressWorkListHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('work_view')
    def get(self, *args, **kwargs):
        try:
            work_service = WeddingDressWorkService(self.db)
            work = work_service.query_work(merchant_id=self.current_user.get('Fmerchant_id'))

            self.echo('crm/weddingdress/work_list.html', {
                'work' : work,
                'category_info': _WEDDING_DRESS_CATEGORY,
                'color_info': _WEDDING_DRESS_COLOR,
                'style_info': _WEDDING_DRESS_STYLE
            })
        except Exception, e:
            self.captureException(*sys.exc_info())


class WeddingDressWorkAddHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self, *args, **kwargs):
        try:
            self.echo('crm/weddingdress/work_add.html',{
                'category_info': _WEDDING_DRESS_CATEGORY,
                'color_info': _WEDDING_DRESS_COLOR,
                'style_info': _WEDDING_DRESS_STYLE
            })
        except Exception, e:
            self.captureException(*sys.exc_info())

    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def post(self, *args, **kwargs):
        self.get_paras_dict()
        self.qdict['merchant_id'], self.qdict['user_id'] = self.current_user.get('Fmerchant_id'), self.current_user.get('Fid')

        try:
            work_service = WeddingDressWorkService()
            work_service.set_db(self.db)

            work_service.add_work(**self.qdict)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            #删除作品数量缓存
            self.delete_product_count(self.current_user.get('Fmerchant_id'))

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))

        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressWorkEditHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self, work_id):
        try:
            work_service = WeddingDressWorkService()
            work_service.set_db(self.db)

            work = work_service.query_work(work_id=work_id).scalar()
            images = work_service.query_work_images(work_id=work_id).all()

            self.echo('crm/weddingdress/work_edit.html', {
                'work': work,
                'images': images,
                'category_info': _WEDDING_DRESS_CATEGORY,
                'color_info': _WEDDING_DRESS_COLOR,
                'style_info': _WEDDING_DRESS_STYLE

            })
            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())

    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def post(self, work_id):
        self.get_paras_dict()
        self.qdict['merchant_id'], self.qdict['user_id'] = self.current_user.get('Fmerchant_id'), self.current_user.get('Fid')

        try:
            work_service = WeddingDressWorkService()
            work_service.set_db(self.db)

            work_service.update_work(work_id, **self.qdict)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            self.delete_product_count(self.current_user.get('Fmerchant_id'))   #删除作品数量缓存

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))

        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressWorkDeleteHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def post(self, work_id):
        try:
            work_service = WeddingDressWorkService()
            work_service.set_db(self.db)

            work_service.delete_work(work_id)

            #更新公司最低价与最高价
            company_service = CompanyServices(self.db)
            company_service.update_range_price(self.current_user.get('Fmerchant_id'), WeddingDressSeriesService(self.db), WeddingDressWorkService(self.db))

            #删除作品数量缓存
            self.delete_product_count(self.current_user.get('Fmerchant_id'))

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())


class WeddingDressWorkDeleteImgHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self, img_id):
        try:
            work_service, album_service = WeddingDressWorkService(self.db), PhotosServices(self.db)

            #删除作品图片
            work_service.delete_work_images(img_id=img_id)

            #删除相册图片
            album_service.delete_photo(photo_id=img_id)

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))
        except Exception, e:
            self.write(ujson.dumps({'stat':'error','info':'错误:'+e.message}))
            self.captureException(*sys.exc_info())
