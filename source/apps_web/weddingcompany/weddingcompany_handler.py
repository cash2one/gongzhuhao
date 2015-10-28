#encoding: utf-8
__author__ = 'hongjiongteng'

import sys
from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from conf.work_conf import _QUERY_PRICE,PAGE_SIZE, _WEDDING_COMPANY_CATEGORY, _WEDDING_COMPANY_COLOR, _WEDDING_COMPANY_STYLE
from services.weddingcompany.weddingcompany_service import WeddingCompanySeriesService, WeddingCompanyWorkService
from services.company.company_services import CompanyServices
from services.company.location_service import LocationServices

class WeddingCompanySeriesHandler(BaseApiHandler, WebCacheHandler):
    def get(self, *args, **kwargs):
        self.get_paras_dict()

        between_price, start_price, end_price = self.qdict.get('between_price',''), self.qdict.get('start_price',''),\
                                                self.qdict.get('end_price','')
        order_by, page = self.qdict.get('order_by',''), self.qdict.get('page',1)

        service = WeddingCompanySeriesService()
        service.set_db(self.db)
        try:
            query = service.query_series_and_company_name(**self.qdict)
            packages = self.get_page_data(query, page_size=PAGE_SIZE, page=page)
            lst_package = packages.result.all()

            banner = self.get_banner('series_banner')
            essence = self.get_essence(page_size=4, series_service=WeddingCompanySeriesService())

            self.echo('view/weddingcompany/series_list.html',{
               'page_html':packages.render_admin_html_web(),
               'packages':lst_package,
               'packages_count':packages.total,
               'query_prices':_QUERY_PRICE,
               'between_price':between_price,
               'start_price':start_price,
               'end_price':end_price,
               'order_by':order_by,
               'series_banner':banner,
               'series_essence': essence
            })
        except Exception, e:
            self.captureException(*sys.exc_info())

class WeddingCompanySeriesDetailHandler(BaseApiHandler, WebCacheHandler):
    def get(self, series_id):
        try:
            series_service, company_service = WeddingCompanySeriesService(), CompanyServices()
            series_service.set_db(self.db)
            company_service.set_db(self.db)

            series = series_service.query_series(series_id=series_id).scalar()
            images = series_service.query_series_images(series_id=series_id)
            recommend_series = series_service.query_series(order_by='Fcreate_time').limit(3).offset(0)

            conpany = company_service.get_company_by_uid(series.Fmerchant_id)           #公司信息
            company_gift = company_service.get_gift(series.Fmerchant_id,1).scalar()     #到店礼
            order_gift = company_service.get_gift(series.Fmerchant_id,2).scalar()       #订单礼
            #1.商户订单,2.套系订单 3.作品订单
            order_url = '/order/create/2/'+str(series_id)+'/'+str(conpany.Fuser_id)
            self.echo('view/weddingCompany/series_detail.html',{
                'series':series,
                'recommend_series':recommend_series,
                'company':conpany,
                'order_gift':order_gift,
                'company_gift':company_gift,
                'images':images,
                'order_url':order_url
            })

        except Exception, e:
            self.captureException(*sys.exc_info())


class WeddingCompanyMerchantHandler(BaseApiHandler, WebCacheHandler):
    def get(self):
        self.get_paras_dict()
        between_price = self.qdict.get('between_price','')
        area = self.qdict.get('area','')
        order = self.qdict.get('order','Fcreate_time')
        page = self.qdict.get('page',1)

        company_service = CompanyServices(self.db)
        location_service = LocationServices(self.db)
        series_service =  WeddingCompanySeriesService(self.db)
        try:
            query = company_service.get_companys_by_role('merchant_weddingcompany', **self.qdict)       #婚庆公司role_code: merchant_weddingcompany
            companys = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            areas = location_service.get_location_name_list(type='area',father_id=73)

            top_banner = self.get_banner('merchant_banner')

            self.echo('view/weddingcompany/merchant_list.html',{
                      'page_html':companys.render_admin_html_web(),
                      'companys':companys,
                      'company_count':companys.total,
                      'query_area':areas,
                      'query_price':_QUERY_PRICE,
                      'between_price':between_price,
                      'area':area,
                      'order':order,
                      'top_banner':top_banner
                      })
        except Exception,e:
            self.captureException(*sys.exc_info())

    def get_count(self,type,merchant_id):
        '''
        todo:获取
        :param type:
        :param merchant_id:
        :return:
        '''
        if type=='product':
            count = self.get_product_count(merchant_id, WeddingCompanyWorkService(self.db))
        elif type=='package':
            count = self.get_package_count(merchant_id, WeddingCompanySeriesService(self.db))
        return count

    def get_area(self,area_id):
        return self.get_area_name(area_id)

    def get_essence_series(self):
        '''
        todo:获取精品套系
        :return:
        '''
        return self.get_essence(page_size=4)


class WeddingCompanyMerchantDetailHandler(BaseApiHandler, WebCacheHandler):
    def get(self, merchant_id):
        try:
            company_service, series_service = CompanyServices(self.db), WeddingCompanySeriesService(self.db)
            work_service = WeddingCompanyWorkService(self.db)

            company = company_service.get_company_by_id(merchant_id)
            company_gift = company_service.get_gift(company.Fuser_id,1).scalar()       #到店礼
            order_gift = company_service.get_gift(company.Fuser_id,2).scalar()       #订单礼

            works = work_service.query_work(order_by='Fcreate_time',merchant_id=company.Fuser_id)
            work_count = works.count()
            works = works.limit(6).offset(0)

            series = series_service.query_series(order_by='Fcreate_time',merchant_id=company.Fuser_id)
            series_count = series.count()
            recommend_series = series.limit(3).offset(0)
            series = series.limit(6).offset(0)

            #1.商户订单,2.套系订单 3.作品订单
            order_url = '/order/create/1/'+str(company.Fuser_id)+'/'+str(company.Fuser_id)
            self.echo('view/weddingcompany/merchant_detail.html',{
                'company':company,
                'order_gift':order_gift,
                'company_gift':company_gift,
                'works':works,
                'series':series,
                'series_count':series_count,
                'work_count':work_count,
                'recommend_series':recommend_series,
                'merchant_id':company.Fuser_id,
                'order_url':order_url
            })
        except Exception,e:
            self.captureException(*sys.exc_info())


class WeddingCompanyMerchantAllSeriesHandler(BaseApiHandler, WebCacheHandler):
    pass


class WeddingCompanyWorkHandler(BaseApiHandler, WebCacheHandler):
    def get(self):
        self.get_paras_dict()
        qcategory, qcolor, qstyle = self.qdict.get('category', ''), self.qdict.get('color', ''), self.qdict.get('style', '')
        order, page = self.qdict.get('order','Fcreate_time'), self.qdict.get('page',1)

        work_service = WeddingCompanyWorkService(self.db)
        try:
            query = work_service.query_work_and_company_name(**self.qdict)
            works = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            lst_works = works.result.all()

            self.echo('view/weddingcompany/work_list.html',{
                      'page_html':works.render_admin_html_web(),
                      'works':lst_works,
                      'works_count': works.total,
                      'qcategory': qcategory,
                      'qcolor': qcolor,
                      'qstyle': qstyle,
                      'order':order,
                      'category_info': _WEDDING_COMPANY_CATEGORY,
                      'color_info': _WEDDING_COMPANY_COLOR,
                      'style_info': _WEDDING_COMPANY_STYLE
                      })
        except Exception,e:
            self.captureException(*sys.exc_info())


class WeddingCompanyWorkDetailHandler(BaseApiHandler, WebCacheHandler):
    def get(self, work_id):
        try:
            work_service, company_service = WeddingCompanyWorkService(self.db), CompanyServices(self.db)

            work, images = work_service.query_work(work_id=work_id).scalar(), work_service.query_work_images(work_id=work_id).all()

            recent_works = work_service.query_work(merchant_id=work.Fmerchant_id,order_by='Fcreate_time').limit(3).offset(0)
            company = company_service.get_company_by_uid(work.Fmerchant_id)  #公司信息
            company_gift = company_service.get_gift(work.Fmerchant_id,1).scalar()       #到店礼
            order_gift = company_service.get_gift(work.Fmerchant_id,2).scalar()       #y优惠
            #1.商户订单,2.套系订单 3.作品订单
            order_url = '/order/create/3/'+str(work_id)+'/'+str(company.Fuser_id)

            category = _WEDDING_COMPANY_CATEGORY.get(work.Fcategory) if _WEDDING_COMPANY_CATEGORY.get(work.Fcategory) else work.Fcategory
            color = _WEDDING_COMPANY_COLOR.get(work.Fcolor) if _WEDDING_COMPANY_COLOR.get(work.Fcolor) else work.Fcolor
            style = _WEDDING_COMPANY_STYLE.get(work.Fstyle) if _WEDDING_COMPANY_STYLE.get(work.Fstyle) else work.Fstyle

            self.echo('view/weddingcompany/work_detail.html',{
                'work':work,
                'images':images,
                'recent_works':recent_works,
                'company':company,
                'order_gift':order_gift,
                'company_gift':company_gift,
                'order_url':order_url,
                'category': category,
                'color': color,
                'style': style
            })
        except Exception,e:
            self.captureException(*sys.exc_info())


class WeddingCompanyMerchantAllWorkHandler(BaseApiHandler, WebCacheHandler):
    pass
