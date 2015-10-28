#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from common.cache_base import AdminCacheHandler
from services.home.home_service import HomeService
from conf.home_conf import packages_position,products_position,companys_position
from tornado.options import options
from utils.upload_utile import upload_to_oss
from utils.datetime_util import datetime_format
import tornado
import ujson

home_service = HomeService()

class RecommendsHandler(AdminBaseHandler,AdminCacheHandler):

    def get(self,code):

        home_service.set_db(self.db)
        query = home_service.query_recommend(code=code)
        recommends = self.get_page_data(query)
        self.echo('ops/home/homes.html',
                  {'recommends':recommends,
                   'page_html':recommends.render_admin_html(),
                   'packages_position':packages_position,
                   'products_position':products_position,
                   'companys_position':companys_position,
                   'code':code
                  })

    def post(self,code):

        rsg = {'stat':'error','msg':''}
        self.get_paras_dict()

        type = self.qdict.get('Frecommend_type')
        position = self.qdict.get('Fposition')
        re_id = self.qdict.get('re_id')
        if not self.request.files.get('recommend_img') or not position:
            rsg['msg'] = '请上传首页展示图或选择展示位置'
            return self.write(ujson.dumps(rsg))

        home_service.set_db(self.db)
        self.qdict['Fis_on_share'] = 1

        try:
            old_re = home_service.query_recommend(**self.qdict)
            if old_re.count():
                old_re.update({'Fis_on_share':0})
            date_format_prefix = datetime_format(format='%Y%m%d')
            file_prex = '/'.join(['recommends',str(self.get_current_user().get('Fid')),date_format_prefix])
            is_ok,filenames = upload_to_oss(self,options.IMG_BUCKET,param_name='recommend_img',file_type='img',file_prex=file_prex,max_size=3)
            if is_ok:
                for f in filenames:
                    url = options.IMG_DOMAIN+'/'+f.get('full_name')
                    self.qdict['Frecommend_url'] = url
            self.qdict.pop('re_id')
            home_service.update_recommend(re_id,**self.qdict)
            if type == '1':
                self.delete_recommend_series()
            elif type == '2':
                self.delete_recommend_products()
            elif type == '3':
                self.delete_recommend_merchant()
        except Exception,e:
            rsg['msg'] = e.message
            return self.write(ujson.dumps(rsg))
        rsg['stat'] = 'ok'
        self.write(ujson.dumps(rsg))


class CreateRecommendHandler(AdminBaseHandler):

    def post(self):

        rsg = {'stat':'error','msg':''}
        self.get_paras_dict()
        home_service.set_db(self.db)
        product_id = self.qdict.get('product_id')
        type = self.qdict.get('type')
        query = home_service.query_recommend(Fproduct_id = product_id,Frecommend_type = type)
        if query.count():
            rsg['msg'] = '该产品在首页列表中已存在'
            return self.write(ujson.dumps(rsg))
        data = {}
        data['user_id'] = self.get_current_user().get('Fid')
        data['product_id'] = product_id
        data['product_name'] = self.qdict.get('product_name')
        data['merchant_id'] = self.qdict.get('merchant_id')
        data['type'] = type
        try:
            home_service.create_recommend(**data)
        except Exception,e:
            rsg['msg'] = e.message
            return self.write(ujson.dumps(rsg))
        rsg['stat'] = 'ok'
        self.write(ujson.dumps(rsg))

class DeleteRecommendHandler(AdminBaseHandler):

    def get(self,re_id,re_type):
        '''
        todo:从首页分享列表中移除
        :param re_id:
        :return:
        '''
        rsg = {'stat':'error','msg':''}
        home_service.set_db(self.db)
        try:
            home_service.delete_recommend(re_id)
            if re_type == '1':
                self.delete_recommend_series()
            elif re_type == '2':
                self.delete_recommend_products()
            elif re_type == '3':
                self.delete_recommend_merchant()
        except Exception,e:
            rsg['msg'] = e.message
            return self.write(ujson.dumps(rsg))
        rsg['stat'] = 'ok'
        self.write(ujson.dumps(rsg))



































