#encoding:utf-8
__author__ = 'binpo'

from common.cache_base import CacheBaseHandler
from apps_mobile.mobile_base import MobileBaseHandler
from models.company_do import Company
from services.series.series_services import SeriesServices
from services.company.company_services import CompanyServices
from services.company.location_service import LocationServices
from conf.work_conf import _QUERY_PRICE as query_status,PAGE_SIZE,_QUERY_PRICE_APP,PAGE_SIZE_APP,SERIES_KEYS
import ujson

series_service = SeriesServices()
company_service = CompanyServices()
location_service = LocationServices()

class SeriesHandler(MobileBaseHandler,CacheBaseHandler):

    def get(self,page=1,merchant_id=0,**kwargs):

        if int(page) <1:
            page = 1

        series_service.set_db(self.db)
        self.get_paras_dict()

        prices = self.qdict.get('price','').split('-')
        start_price = prices[0]
        end_price = prices[-1]

        series_query = series_service.query_series(start_price=start_price,end_price=end_price,merchant_id=merchant_id)

        if self.request.uri.startswith('/api/json/'):

            series = self.get_page_data(series_query,page_size=PAGE_SIZE_APP,page=page)

            has_next = self.is_page(series.page_num,page=page)

            company_service.set_db(self.db)
            lst_series = []
            for s in series.result:
                series_dict = self.obj_to_dict(s,SERIES_KEYS)
                series_dict['company_name'] = company_service.get_company_by_uid(s.Fmerchant_id).Fcompany_name
                lst_series.append(series_dict)

            if int(page) > 1:
                data = {
                        'lst_series':lst_series,
                        'has_next':has_next
                       }
            else:
                data = {
                        'lst_series':lst_series,
                        'has_next':has_next,
                        'query_price':_QUERY_PRICE_APP
                        }
            self.write_json({'stat':'ok','data':data,'info':''})
        else:

            series = self.get_page_data(series_query,page_size=PAGE_SIZE,page=page)

            has_next = self.is_page(series.page_num,page=page)

            if int(page) > 1:
                return self.others_page(series,has_next,self.qdict.get('price',''),merchant_id)
            else:
                if merchant_id and int(merchant_id):
                    self.echo('views/merchant/merchant_series_page.html',
                              {'series':series,
                               'has_next':has_next,
                               'merchant_id':merchant_id
                              },
                              layout='views/merchant/merchant_series.html')
                else:
                    self.echo('views/series/series_page.html',
                              {'series':series,
                              'query_status':query_status,
                              'price':self.qdict.get('price',''),
                              'has_next':has_next,
                              },layout='views/series/series.html')

    def get_company(self,merchant_id):
        '''
        todo:获取公司
        :param merchant_id:
        :return:
        '''
        return self.db.query(Company).filter(Company.Fuser_id == merchant_id,Company.Fdeleted == 0).scalar()

    def others_page(self,series,has_next,price,merchant_id):
        if merchant_id:
            _html = self.render('views/merchant/merchant_series_page.html',{'series':series})
        else:
            _html = self.render('views/series/series_page.html',{'series':series})
        self.write(ujson.dumps({'stat':'ok','html':_html,'has_next':has_next,'price':price}))

class SeriesQueryHandler(MobileBaseHandler):

    def get(self,package_id):

        series_service.set_db(self.db)
        company_service.set_db(self.db)
        package = series_service.query_series(id = package_id)

        query = series_service.query_series(merchant_id=package.scalar().Fmerchant_id)
        series = self.get_page_data(query,page_size=4,page=1)

        package_images = series_service.get_series_iamges_by_id(package_id)
        company = company_service.get_company_by_uid(package.scalar().Fmerchant_id)

        if self.request.uri.startswith('/api/json/'):
            images = [img.Furl for img in package_images]
            package = self.obj_to_dict(package.scalar(),SERIES_KEYS)
            hot_series = [self.obj_to_dict(s,SERIES_KEYS) for s in series.result]
            location_service.set_db(self.db)
            package['images'] = images
            data = {
                    'company_name':company.Fcompany_name,
                    'cheapest_price':company.Fcheapest,
                    'expensive_price':company.Fmost_expensive,
                    'company_phone':company.Fphone,
                    'company_url':company.Fphoto_url,
                    'company_id':company.Fuser_id,
                    'area':location_service.get_location_name_by_id('area',company.Farea),
                    'package':package,
                    'hot_series':hot_series,
                    'Fid':package.get('Fid'),
                    'series_count':series.total
                    }
            return self.write_json({'stat':'ok','data':data,'info':''})
        else:
            self.echo('views/series/series_detail.html',
                      {'package':package.scalar(),
                      'package_images':package_images,
                      'company':company,
                      'hot_series':series
                     })

