# encoding:utf-8
import tornado
from common.base import BaseHandler
from services.orders.orders import ShowServices as OrderShowServices
from services.schedules.schedules import ShowServices
from services.staffers.staffer_services import StafferServices
from utils.error_util import Error
from conf.order_conf import _TYPE_ORDER
from conf.order_conf import _SCHEDULE_TYPE


class CHandlerScheduleH5List(BaseHandler):
    def get(self, order_id):
        try:
            db_schedule = ShowServices(self.db)
            schedules = db_schedule.get_schedule(order_id)

            db_order = OrderShowServices(self.db)
            order, stf = db_order.get_order_info(order_id)
            order.Forder_type = _TYPE_ORDER[int(order.Forder_type)]

            self.echo(
                'crm/order/H5/index_py.html',
                {'items': schedules, 'order': order})

        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            self.echo("crm/404.html")

    def post(self, order_id):
        pass


class CHandlerScheduleH5Tips(BaseHandler):
    def get(self, order_id, shd_no):
        try:
            db_schedule = ShowServices(self.db)
            schedules = db_schedule.get_schedule(order_id)
            stf_id = schedules[int(shd_no)].Fuid_stf.split('$')[0]
            stf = StafferServices(self.db).get_staffer_by_id_(stf_id)

            self.echo('crm/order/H5/detail_py.html', {
                'item': schedules[int(shd_no)],
                'stf': stf,
                'shd_no': shd_no,
                'shd_nm': _SCHEDULE_TYPE[int(shd_no)]
            })

        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            self.echo("crm/404.html")

    def post(self, order_id):
        pass



