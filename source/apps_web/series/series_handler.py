#encoding:utf-8
__author__ = 'binpo'

from common.base import BaseApiHandler
from services.series.series_services import SeriesServices
from services.company.company_services import CompanyServices

company_service = CompanyServices()
series_service = SeriesServices()

class SeriesQueryhandler(BaseApiHandler):

    def get(self, *args, **kwargs):
        pass




class SeriesDetailhandler(BaseApiHandler):

    def get(self, series_id, **kwargs):
        series_service.set_db(self.db)
        company_service.set_db(self.db)

        series = series_service.get_series_by_id(series_id)
        images = series_service.get_series_iamges_by_id(series_id)
        recommend_series = series_service.query_series(order_by='Fcreate_time').limit(3).offset(0)

        conpany = company_service.get_company_by_uid(series.Fmerchant_id)  #公司信息
        company_gift = company_service.get_gift(series.Fmerchant_id,1).scalar()     #到店礼
        order_gift = company_service.get_gift(series.Fmerchant_id,2).scalar()       #订单礼
        #1.商户订单,2.套系订单 3.作品订单
        order_url = '/order/create/2/'+str(series_id)+'/'+str(conpany.Fuser_id)
        self.echo('view/series/series_detail.html',{
                'series':series,
                'recommend_series':recommend_series,
                'company':conpany,
                'order_gift':order_gift,
                'company_gift':company_gift,
                'images':images,
                'order_url':order_url
            })
