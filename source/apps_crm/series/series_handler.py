# encoding:utf-8
__author__ = 'sunli'

import tornado
from tornado.web import MissingArgumentError
from utils.error_util import Error

from common.base import BaseHandler
from services.series.series_services import SeriesServices
from common.permission_control import company_permission_control
from models.product_do import ShotPackageImages

import ujson
import sys

series_service = SeriesServices()

class SeriesList(BaseHandler):
    '''
    套系一览Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('series_view')
    def get(self):
        try:
            if 'merchant' in self.get_current_user().get('Frole_codes'):
                uid = self.get_current_user().get('Fid')
            else:
                uid = self.get_current_user().get('Fmerchant_id')

            series_service.set_db(self.db)
            series = series_service.query_series(merchant_id=uid)

            self.echo('crm/series/series_list.html',
                      {
                          'series' : series,
                       })

        except Exception, e:
            
            self.echo('crm/404.html')

class SeriesAdd(BaseHandler):
    '''
    套系添加、编辑Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, series_id=None):
        try:
            if not series_id:   #新增
                series_id = 0
                series = None
                images=[]
            else:   #编辑
                series_id = int(series_id)
                merchant_id = self.current_user.get('Fmerchant_id') #商户id

                series_service.set_db(self.db)
                series = series_service.query_series(id=series_id, merchant_id=merchant_id)
                series = series.first()
                if series:
                    images = series_service.get_series_iamges_by_id(series_id)


            self.echo('crm/series/series_add.html',
                      {
                          'series_id' : series_id,
                          'series' : series,
                          'images': images
                      })
        except Exception, e:
            
            self.write(Error(2, e.message).__dict__)

    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def post(self, series_id=None):
        self.get_paras_dict()

        try:
            series_id = int(series_id)

            dic_para = {}
            if not series_id:   #新建时
                dic_para['Fuser_id'] = self.current_user.get('Fid') #子商户id
                dic_para['Fmerchant_id'] = self.current_user.get('Fmerchant_id') #商户id
            else:   #更新时
                dic_para['Fuser_id'] = self.current_user.get('Fid') #子商户id

            dic_para['Fpackage_name'] = self.qdict.get('package_name', None) #套系名称

            dic_para['Fprice'] = self.qdict.get('price', None)    #原价
            dic_para['Fsale_price'] = self.qdict.get('sale_price', None)    #现价

            dic_para['Fbride_style_count'] = self.qdict.get('bride_style_count', None)    #新娘造型X套 单位是套
            dic_para['Fgroom_style_count'] = self.qdict.get('groom_style_count', None)    #新郎造型X套 单位是套
            dic_para['Fcloth_select_type'] = self.qdict.get('cloth_select_type', None)    #服装选择区域  #服装选择类型  1.指定区域 2.全场任选
            dic_para['Fcloth_remark'] = self.qdict.get('cloth_remark', None)    #补充说明

            dic_para['Foutdoor_space'] = self.qdict.get('outdoor_space', None)    #外景地
            dic_para['Finner_space'] = self.qdict.get('inner_space', None)    #内景地
            dic_para['Fspace_remark'] = self.qdict.get('space_remark', None)    #补充说明

            dic_para['Fshot_desc'] = self.qdict.get('shot_desc', None)    #套系特色
            dic_para['Fphotographer_level'] = self.qdict.get('photographer_level', None)    #摄影师级别
            dic_para['Frecommend_photographer'] = self.qdict.get('recommend_photographer', None)    #推荐摄影师       #多个用空格隔开
            dic_para['Farter_level'] = self.qdict.get('arter_level', None)    #化妆师级别
            dic_para['Frecommend_arter'] = self.qdict.get('recommend_arter', None)    #推荐化妆师              #多个用空格隔开

            dic_para['Fphoto_album_desc'] = self.qdict.get('photo_album_desc', None)    #相册
            dic_para['Fphoto_frame_desc'] = self.qdict.get('photo_frame_desc', None)    #相框
            dic_para['Fmv_desc'] = self.qdict.get('mv_desc', None)    #相框
            dic_para['Fother_desc'] = self.qdict.get('other_desc', None)    #其他描述


            dic_para['Fdescription'] = self.qdict.get('description', None)    #套系补充说明#
            dic_para['Fother_pay_desc'] = self.qdict.get('other_pay',None)
            dic_para['images'] = self.qdict.get('images', None)
            dic_para['Fcover_img'] = self.qdict.get('cover_url',None) #封面图url

            series_service.set_db(self.db)

            if not series_id:   #新建时
                is_ok,series = series_service.create_series(**dic_para)
                self.delete_package_count(self.current_user.get('Fmerchant_id'))
                self.delete_essence()
            else:   #更新时
                series_id = int(series_id)
                is_ok,series = series_service.update_series(series_id, **dic_para)

            if is_ok:
                self.update_company_price(series.Fmerchant_id)

            self.write(ujson.dumps({'stat':'ok','info':'提交成功'}))

        except Exception, e:
            print e.message
            
            self.write(ujson.dumps({'stat':'error','info':'保存错误:'+e.message}))

class SeriesDelete(BaseHandler):
    '''
    套系删除Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, series_id):
        try:
            rsg={}
            series_service.set_db(self.db)
            series_id = int(series_id)
            series = series_service.query_series(id = series_id).scalar()
            merchant_id = self.current_user.get('Fmerchant_id') #商户id

            data = {}
            data['Fdeleted'] = 1
            series_service.update_series(series_id,**data)

            self.update_company_price(merchant_id)

            rsg['stat'] = 'ok'
            self.write(ujson.dumps(rsg))

        except Exception, e:
            
            self.write(ujson.dumps({'stat':'error','msg':'程序发生异常,异常原因是:'+e.message}))


class SerieImageDelete(BaseHandler):
    '''
    套系删除Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('series_edit')
    def get(self, series_img_id):
        try:
            series = self.db.query(ShotPackageImages).filter(ShotPackageImages.Fdeleted == 0,ShotPackageImages.Fid == series_img_id)
            if series.scalar():
                series.Fdeleted=1
                self.db.add(series)
                self.db.commit()
            self.write('ok')
        except Exception, e:
            
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)
