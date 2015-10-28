#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from conf.order_conf import _SCHEDULE_TYPE
from services.schedules.schedules_service import ScheduleService
import ujson
from models.order_do import Orders
from models.staffer_do import Staffers
from models.schedule_do import OrdersSchedule

schedule_service = ScheduleService()

class ScheduleAttentionHandler(AdminBaseHandler):
    def get(self,user_id):
        schedule_service.set_db(self.db)
        schedule_attentions = schedule_service.get_attention_by_mct_id(user_id)
        data = {}
        if schedule_attentions and schedule_attentions.count()>0:
            for schedule_attention in schedule_attentions.all():
                sch_description = schedule_attention.Fdescription
                if schedule_attention.Fschedule_type_name == _SCHEDULE_TYPE[0].decode('utf-8'):
                    data['schedule_item_0'] = sch_description
                elif schedule_attention.Fschedule_type_name == _SCHEDULE_TYPE[1].decode('utf-8'):
                    data['schedule_item_1'] = sch_description
                elif schedule_attention.Fschedule_type_name == _SCHEDULE_TYPE[2].decode('utf-8'):
                    data['schedule_item_2'] = sch_description
                elif schedule_attention.Fschedule_type_name == _SCHEDULE_TYPE[3].decode('utf-8'):
                    data['schedule_item_3'] = sch_description
                elif schedule_attention.Fschedule_type_name == _SCHEDULE_TYPE[4].decode('utf-8'):
                    data['schedule_item_4'] = sch_description
            self.echo('ops/company/attention.html',
                      {'schedule_attentions':data,'schedule_type':_SCHEDULE_TYPE,'user_id':user_id})
        else:
            self.echo('ops/company/attention.html',
                      {'schedule_type':_SCHEDULE_TYPE,'schedule_attentions':data,'user_id':user_id})

    def post(self,user_id):
        rsg = {
            'stat':'error',
            'info':'',
        }
        try:
            self.get_paras_dict()
            schedule_service.set_db(self.db)
            lst = []
            lst.append(self.qdict.get('schedule_item_0'))
            lst.append(self.qdict.get('schedule_item_1'))
            lst.append(self.qdict.get('schedule_item_2'))
            lst.append(self.qdict.get('schedule_item_3'))
            lst.append(self.qdict.get('schedule_item_4'))
            schedule_service.update_attention(user_id,_SCHEDULE_TYPE,lst)
        except Exception,e:
            print e
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))

class CreateSchedulesHandler(AdminBaseHandler):
    def get(self,order_id):
        order = self.db.query(Orders).filter(Orders.Fdeleted == 0,Orders.Fid == order_id).scalar()
        staffers = self.db.query(Staffers).filter(Staffers.Fdeleted == 0,Staffers.Fuid_mct == order.Fuid_mct)
        schedules = self.db.query(OrdersSchedule).filter(OrdersSchedule.Fdeleted == 0,OrdersSchedule.Forder_id == order_id)
        self.echo('ops/orders/create_schedule.html',{'order':order,'staffers':staffers,'schedules':schedules})

    def post(self,order_id):
        rsg = {
            'stat':'err',
            'msg':''
        }
        self.get_paras_dict()
        schedule_service.set_db(self.db)
        try:
            schedule_service.update_schedule_by_schedule_id(order_id,**self.qdict)
        except Exception,e:
            print e
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))
























