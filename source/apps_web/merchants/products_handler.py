#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from services.work.work_services import WorkServices
from conf.work_conf import _WORK_STYLE_WX,_SHOOTING_SCENE_WX,_SHOOTING_SITE,_SHOOTING_SCENE_2,_MODE_STYLE,PAGE_SIZE
import sys
import random

work_service = WorkServices()

class ProductHandler(BaseApiHandler):

    def get(self,product_id, **kwargs):
        work_service.set_db(self.db)
        product,product_images = work_service.get_product_by_id(product_id)
        self.echo('','')

    def post(self, *args, **kwargs):
        pass


class ProductsHandler(BaseApiHandler,WebCacheHandler):

    def get(self):
        self.get_paras_dict()
        if not self.qdict.get('product_type',''):
            work_type = 'wedding'
            self.qdict['product_type'] = 'wedding'
        else:
            work_type = self.qdict.get('product_type')
        work_style = self.qdict.get('style','')
        work_scene = self.qdict.get('scene','')
        mode_style = self.qdict.get('mode_style','')
        shot_space = self.qdict.get('shot_space','')
        order = self.qdict.get('order','Fcreate_time')
        page = self.qdict.get('page',1)
        work_service.set_db(self.db)
        try:
            query = work_service.query_work(**self.qdict)
            works = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            lst_works = works.result.all()
            random.shuffle(lst_works)
            self.echo('view/work/work_list.html',{
                      'page_html':works.render_admin_html_web(),
                      'works':lst_works,
                      'query_style':_WORK_STYLE_WX,
                      'query_scene_wedding':_SHOOTING_SCENE_WX,
                      'query_site':_SHOOTING_SITE,
                      'query_scene_traveling':_SHOOTING_SCENE_2,
                      'query_mode':_MODE_STYLE,
                      'works_count':works.total,
                      'work_style':work_style,
                      'work_scene':work_scene,
                      'mode_style':mode_style,
                      'shot_space':shot_space,
                      'order':order,
                      'type':work_type
                      })
        except Exception,e:
            pass


    def get_company(self,merchant_id):
        '''
        todo:获取公司信息
        :param merchant_id:
        :return:
        '''
        return self.get_company_info(merchant_id)