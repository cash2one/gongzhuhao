#encoding:utf-8
__author__ = 'binpo'
from common.base import AdminBaseHandler
from services.orders.order_services import OrderServices
from services.company.company_services import CompanyServices
from conf.order_conf import _TYPE_ORDER
import sys

order_service = OrderServices()
company_service = CompanyServices()

class BespeakOrdrHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        order_service.set_db(self.db)
        company_service.set_db(self.db)
        companys = company_service.get_companys()
        self.get_paras_dict()
        try:
            query = order_service.query_bespeaker_orders()
            page_data = self.get_page_data(query)

            self.echo('ops/orders/bespeak_order_list.html',
                      {'page_data':page_data,
                       'page_html':page_data.render_admin_html(),
                       'company_service':company_service,
                       'companys':companys,
                       'order_type':_TYPE_ORDER
                      })
        except Exception,e:
            # print e.message
            self.echo('ops/500.html')

    def post(self, *args, **kwargs):
        pass

