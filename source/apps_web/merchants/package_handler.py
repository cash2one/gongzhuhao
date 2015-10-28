#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from conf.work_conf import _QUERY_PRICE,PAGE_SIZE
from services.series.series_services import SeriesServices
import sys
import random

series_service = SeriesServices()

class PackageHandler(BaseApiHandler):

    def get(self,product_id, **kwargs):
        pass


class PackagesHandler(BaseApiHandler,WebCacheHandler):

    def get(self):
        self.get_paras_dict()
        series_service.set_db(self.db)
        between_price = self.qdict.get('between_price','')
        start_price = self.qdict.get('start_price','')
        end_price = self.qdict.get('end_price','')
        order_by = self.qdict.get('order_by','')
        page = self.qdict.get('page',1)
        try:
            query = series_service.query_series(**self.qdict)
            packages = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            lst_package = packages.result.all()
            random.shuffle(lst_package)

            banner = self.get_banner('series_banner')

            self.echo('view/series/series_list.html',
                      {
                       'page_html':packages.render_admin_html_web(),
                       'packages':lst_package,
                       'packages_count':packages.total,
                       'query_prices':_QUERY_PRICE,
                       'between_price':between_price,
                       'start_price':start_price,
                       'end_price':end_price,
                       'order_by':order_by,
                       'series_banner':banner
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

    def get_essence_series(self):
        '''
        todo:获取精品套系
        :return:
        '''
        return self.get_essence(page_size=4)




