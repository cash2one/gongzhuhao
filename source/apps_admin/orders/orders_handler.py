#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from services.orders.order_services import OrderServices
from services.company.company_services import CompanyServices
from conf.order_conf import _TYPE_ORDER

order_service = OrderServices()
company_service = CompanyServices()

class OrderHandlerList(AdminBaseHandler):

    def get(self, *args, **kwargs):

        order_service.set_db(self.db)
        company_service.set_db(self.db)
        companys = company_service.get_companys()
        self.get_paras_dict()
        user_id = self.qdict.get('user_id')
        user_name = self.qdict.get('user_name')
        try:
            query = order_service.query_orders(user_id=user_id,user_name=user_name)
            page_data = self.get_page_data(query)
            self.echo('ops/orders/order_list.html',
                      {'page_data':page_data,
                       'page_html':page_data.render_admin_html(),
                       'order_type':_TYPE_ORDER,
                       'companys':companys
                      })
        except Exception,e:
            print e.message
            self.echo('ops/500.html')







