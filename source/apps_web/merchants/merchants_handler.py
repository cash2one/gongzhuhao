#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from services.company.company_services import CompanyServices
from services.work.work_services import WorkServices
from services.series.series_services import SeriesServices
from services.company.location_service import LocationServices
from conf.merchant import _STYLE
from conf.work_conf import _QUERY_PRICE,PAGE_SIZE
import sys

product_service = WorkServices()
company_service = CompanyServices()

series_service = SeriesServices()

SERIES_PAGE_NUM=18

class MerchantHandler(BaseApiHandler):

    def get(self,merchant_id, **kwargs):
        pass



class MerchantProducts(BaseApiHandler):

    def get(self,merchant_id,**kwargs):
        products = product_service.query_works(merchant_id)
        self.echo('' )

class MerchantListHandler(BaseApiHandler,WebCacheHandler):

    def get(self):
        '''
        todo:商家list
        :param page: 页码
        :param order: 排序
        :return:
        '''
        self.get_paras_dict()
        style = self.qdict.get('style','')
        between_price = self.qdict.get('price_between','')
        area = self.qdict.get('area','')
        order = self.qdict.get('order','Fcreate_time')
        location_service = LocationServices(self.db)
        page = self.qdict.get('page',1)
        company_service.set_db(self.db)
        try:
            query = company_service.get_companys(**self.qdict)
            companys = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            areas = location_service.get_location_name_list(type='area',father_id=73)

            top_banner = self.get_banner('merchant_banner')

            self.echo('view/merchant/merchant_list.html',{
                      'page_html':companys.render_admin_html_web(),
                      'companys':companys,
                      'company_count':companys.total,
                      'query_area':areas,
                      'query_style':_STYLE,
                      'query_price':_QUERY_PRICE,
                      'style':style,
                      'between_price':between_price,
                      'area':area,
                      'order':order,
                      'top_banner':top_banner
                      })
        except Exception,e:
            pass

    def get_count(self,type,merchant_id):
        '''
        todo:获取
        :param type:
        :param merchant_id:
        :return:
        '''
        if type=='product':
            count = self.get_product_count(merchant_id)
        elif type=='package':
            count = self.get_package_count(merchant_id)
        return count

    def get_area(self,area_id):
        return self.get_area_name(area_id)

    def get_essence_series(self):
        '''
        todo:获取精品套系
        :return:
        '''
        return self.get_essence(page_size=4)

class MerchantDetail(BaseApiHandler):

    def get(self,company_id, **kwargs):
        try:
            company_service.set_db(self.db)
            series_service.set_db(self.db)
            product_service.set_db(self.db)
            company = company_service.get_company_by_id(company_id)
            company_gift = company_service.get_gift(company.Fuser_id,1).scalar()       #到店礼
            order_gift = company_service.get_gift(company.Fuser_id,2).scalar()       #订单礼
            products = product_service.query_work(order_by='Fcreate_time',merchant_id=company.Fuser_id)
            product_count = products.count()
            products=products.limit(6).offset(0)
            series = series_service.query_series(order_by='Fcreate_time',merchant_id=company.Fuser_id)
            series_count = series.count()
            recommend_series = series.limit(3).offset(0)
            series = series.limit(6).offset(0)

            #1.商户订单,2.套系订单 3.作品订单
            order_url = '/order/create/1/'+str(company.Fuser_id)+'/'+str(company.Fuser_id)
            self.echo('view/merchant/merchant_detail.html',{
                'company':company,
                'order_gift':order_gift,
                'company_gift':company_gift,
                'products':products,
                'series':series,
                'series_count':series_count,
                'product_count':product_count,
                'recommend_series':recommend_series,
                'merchant_id':company.Fuser_id,
                'order_url':order_url
            })
        except Exception,e:
            print e.message
            raise

            #raise  HTTPError(404)


class MerchantProductsHandler(BaseApiHandler):

    def get(self,merchant_id,product_type='wedding',page=1,**kwargs):
        self.get_paras_dict()
        product_service.set_db(self.db)
        company_service.set_db(self.db)
        company = company_service.get_company_by_uid(merchant_id)
        query = product_service.query_works(merchant_id=merchant_id,product_type=product_type)
        recent_products = product_service.query_work(order_by='Fcreate_time').limit(3).offset(0)
        order_gift = company_service.get_gift(company.Fuser_id,1).scalar()       #到店礼
        other_gift = company_service.get_gift(company.Fuser_id,2).scalar()       #订单礼

        #page_data = self.get_page_data(query,page_size=SERIES_PAGE_NUM,page=page)
        # series_count = series.count()
        # recommend_series = series.limit(3).offset(0)
        #1.商户订单,2.套系订单 3.作品订单
        order_url = '/order/create/1/'+str(merchant_id)+'/'+str(merchant_id)
        self.echo('view/merchant/merchant_works.html',{'products':query,
                                                        'company':company,
                                                        'product_type':product_type,
                                                        'recent_products':recent_products,
                                                        'order_url':order_url,
                                                        'order_gift':order_gift,
                                                        'other_gift':other_gift
                                                        })

class MerchantSeriesHandler(BaseApiHandler):

    def get(self,merchant_id,page=1, **kwargs):

        self.get_paras_dict()
        series_service.set_db(self.db)
        company_service.set_db(self.db)
        company = company_service.get_company_by_uid(merchant_id)
        between_price = self.qdict.get('price')
        start,end = between_price and between_price.split('-') or ('','')
        if start and not end:
            end = start
        elif not start and end:
            start=end
        query = series_service.query_series(order_by='Fcreate_time',merchant_id=merchant_id,start_price=start,end_price=end)
        #page_data = self.get_page_data(query,page_size=SERIES_PAGE_NUM,page=page)
        # series_count = series.count()
        # recommend_series = series.limit(3).offset(0)
        recommend_series = series_service.query_series(order_by='Fcreate_time').limit(3).offset(0)
        order_gift = company_service.get_gift(company.Fuser_id,1).scalar()       #到店礼
        other_gift = company_service.get_gift(company.Fuser_id,2).scalar()       #订单礼

        #1.商户订单,2.套系订单 3.作品订单
        order_url = '/order/create/1/'+str(merchant_id)+'/'+str(merchant_id)
        self.echo('view/merchant/merchant_series.html',{'series':query,
                                                        'company':company,
                                                        'order_url':order_url,
                                                        'between_price':between_price,
                                                        'prices':_QUERY_PRICE,
                                                        'order_gift':order_gift,
                                                        'other_gift':other_gift,
                                                        'recommend_series':recommend_series
                                                        })