#encoding:utf-8
__author__ = 'binpo'

import sys
from common.base import BaseApiHandler
from models.order_do import BespeakOrders
from services.series.series_services import SeriesServices
from services.orders.order_services import OrderServices

series_serivce = SeriesServices()

class OrderHandler(BaseApiHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self,order_type,refer_id,merchant_id, **kwargs):

        try:
            self.get_paras_dict()
            series_serivce.set_db(self.db)
            series_serivce.query_series()
            order_service = OrderServices(self.db)
            user_id = self.current_user and self.current_user.get('Fid') or None
            order_service.create_bespeak_orders(merchant_id,order_type,refer_id,self.qdict.get('phone'),user_id=user_id)
            self.write_json({'code':200,'info':'预定成功'})
        except Exception,e:
            pass

    def put(self, *args, **kwargs):
        pass


