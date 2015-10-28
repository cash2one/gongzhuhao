#encoding:utf-8
__author__ = 'binpo'
from common.cache_base import CacheBaseHandler
from apps_mobile.mobile_base import MobileBaseHandler
from services.company.company_services import CompanyServices
from services.work.work_services import WorkServices
from services.series.series_services import SeriesServices
from services.company.location_service import LocationServices
from conf.work_conf import _QUERY_PRICE as query_price,_WORK_STYLE as work_styles
from conf.merchant import COMPANY_KEYS
import sys
import ujson

PAGE_SIZE = 20
PAGE_SIZE_APP = 6

work_service = WorkServices()
series_service = SeriesServices()
company_service = CompanyServices()

class MerchantListHandler(MobileBaseHandler,CacheBaseHandler):

    def get(self,page = 1):
        '''
        todo:获取商家列表
        :param page:
        :return:
        '''

        if not page or page < 1:
            page = 1

        self.get_paras_dict()
        price_between = self.qdict.get('price','')
        selected_area = self.qdict.get('area','')
        company_service.set_db(self.db)
        style = ''
        try:
            location_service = LocationServices(self.db)
            areas = location_service.get_location_name_list('area',73)
            query = company_service.get_companys(area=selected_area,price_between=price_between,style=style)

            base_url = self.request.full_url().split('?')[0][:-1]+'1'

            if self.request.uri.startswith('/api/json/'):

                companys = self.get_page_data(query,page_size=PAGE_SIZE_APP,page=page)

                company_list = []
                for company in companys.result:
                    company_dict = self.obj_to_dict(company,COMPANY_KEYS)
                    company_dict['company_area'] = location_service.get_location_name_by_id('area',company.Farea)
                    company_list.append(company_dict)
                area_lst = []
                for area in areas:
                    area_lst.append({'key':area.Fid,'value':area.Farea_name})
                has_next = self.is_page(companys.page_num,page)
                data = {
                        'merchants':company_list,
                        'area_lst':area_lst,
                        'has_next':has_next
                        }
                self.write(ujson.dumps({'stat':'ok','data':data,'info':''}))
            else:
                companys = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
                has_next = self.is_page(companys.page_num,page)
                area_dict={}
                for a in areas:
                    area_dict[int(a.Fid)] = a.Farea_name

                if int(page) > 1:
                    return self.others_page(companys,area_dict,has_next)


                url = 'views/merchant/merchant_page.html'
                data = {'merchants':companys,
                        'areas':areas,
                        'query_price':query_price,
                        'work_styles':work_styles,
                        'area_dict':area_dict,
                        'price_between':price_between,
                        'selected_area':selected_area,
                        'my_style':style,
                        'has_next':has_next,
                        'base_url':base_url
                        }
                self.echo(url,data,layout='views/merchant/list.html')
        except Exception,e:
            pass
            self.write(ujson.dumps({'info':'exception:'+e.message}))

    def others_page(self,companys,area_dict,has_next):
        '''
        todo:获取商户分页数据
        :param companys:
        :param has_next:
        :return:
        '''
        _html = self.render('views/merchant/merchant_page.html',{'merchants':companys,'area_dict':area_dict})
        self.write_json({'stat':'ok','data':_html,'has_next':has_next})

class MerchantHandler(MobileBaseHandler):

    def get(self,merchant_id, **kwargs):
        '''
        todo:商家详情
        :param merchant_id:
        :param kwargs:
        :return:
        '''
        company_service.set_db(self.db)
        series_service.set_db(self.db)
        work_service.set_db(self.db)
        try:
            company = company_service.get_company_by_uid(merchant_id)
            query_series = series_service.query_series(merchant_id=company.Fuser_id)
            series = self.get_page_data(query_series,page_size=4,page=1)
            query_works = work_service.query_works(merchant_id,order_by='Fcreate_time desc')
            works = self.get_page_data(query_works,page_size=4,page=1)

            if self.request.uri.startswith('/api/json/'):
                hot_series = [self.obj_to_dict(s,['Fpackage_name','Fprice','Fsale_price','Fcover_img','Fid']) for s in series.result]
                essence_works = [self.obj_to_dict(w,['Fname','Fcover_img','Fid']) for w in works.result]
                company = self.obj_to_dict(company,COMPANY_KEYS)
                data = {
                         'cheapest_price':company.get('Fcheapest'),
                         'expensive_price':company.get('Fmost_expensive'),
                         'company_name':company.get('Fcompany_name'),
                         'contact_phone':company.get('Fphone'),
                         'detail_address':company.get('Fdetail_address'),
                         'photo_url':company.get('Fphoto_url'),
                         'company':company,
                         'hot_series':hot_series,
                         'essence_works':essence_works,
                         'series_count':series.total,
                         'works_count':works.total,
                         'Fuser_id':company.get('Fuser_id')
                       }
                self.write(ujson.dumps({'stat':'ok','data':data,'info':''}))
            else:
                self.echo('views/merchant/detail.html',{'merchant':company,'series':series,'works':works},layout='')
        except Exception,e:
            pass





