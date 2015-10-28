#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseHandler
from services.series.series_services import SeriesServices
from services.work.work_services import WorkServices
from services.orders.order_services import OrderServices
from services.users.user_services import UserServices
from models.company_do import CompanyGift
from services.orders.order_services import OrderServices
series_serivce = SeriesServices()
work_service = WorkServices()
order_service = OrderServices()

import tornado

class BespeakOrdersHandler(BaseHandler):


    @tornado.web.authenticated
    def get(self,**kwargs):

        order_service.set_db(self.db)
        merchant_id = self.get_current_user().get('Fmerchant_id')
        query = order_service.query_bespeaker_orders(merchant_id=merchant_id)
        page_data = self.get_page_data(query)
        page_html = page_data.render_page_html()
        self.echo('crm/order/order_break_list.html',{'page_data':page_data,'page_html':page_html,'start_date':'','search_text':''})