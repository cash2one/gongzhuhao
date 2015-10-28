# encoding:utf-8
from services.base_services import BaseService
from models.schedule_do import OrdersSchedule
from models.order_do import Orders
from utils.error_util import Error
from models.schedule_do import ScheduleAttentionTemplate, ScheduleSiteTemplate
from conf.order_conf import _SCHEDULE_TYPE


class ShowServices(BaseService):
    def __init__(self, db):
        self.db = db

    def set_db(self, db):
        self.db = db

    def check_order_owner(self, uid_mct, order_id):
        res_qry = self.db.query(Orders.Fuid_mct).filter(
            Orders.Fid == order_id,
            Orders.Fdeleted == 0).scalar()
        if str(uid_mct) != res_qry:
            err_msg = "order_id not belong mine [mct_id:%s]" % str(uid_mct)
            raise Error(300, err_msg)

    def get_schedule(self, order_id):
        """获取订单排期"""
        shd_entities = (
            OrdersSchedule.id,
            OrdersSchedule.Fid,
            OrdersSchedule.Fdatetime,
            OrdersSchedule.Fuid_stf,
            OrdersSchedule.Fname_stf,
            OrdersSchedule.Ftitle_stf,
            OrdersSchedule.Fsite,
            OrdersSchedule.Fshot_date,
            OrdersSchedule.Freminder,
            OrdersSchedule.Fschedule_category_id,
            OrdersSchedule.Fnotified_num,
            OrdersSchedule.Fschedule_category_name
            )
        schedules = self.db.query(*shd_entities).filter(
            OrdersSchedule.Forder_id == order_id,
            OrdersSchedule.Fdeleted == 0
            ).order_by(OrdersSchedule.Fid).all()
        return schedules


class UpdateServices(BaseService):
    def __init__(self, db):
        self.db = db

    def set_db(self, db):
        self.db = db

    def get_order_owner(self, order_id):
        return self.db.query(Orders.Fuid_mct).filter(
            Orders.Fid == order_id,
            Orders.Fdeleted == 0).scalar()

    def update_schedule(self, **kargs):
        uid_mct = kargs['uid_mct']
        order_id = kargs['order_id']
        if str(uid_mct) != self.get_order_owner(order_id):  # check order owner
            err_msg = "order_id not belong mine [mct_id:%s]" % str(uid_mct)
            raise Error(300, err_msg)
        try:
            # self.db.begin()
            for i, row in enumerate(kargs['items']):
                if row["ismodify_%d" % i] == "0":
                    continue
                item = {}
                if row["shd_date_%d" % i]:
                    item['Fdatetime'] = row["shd_date_%d" % i]
                    item['Fshot_date'] = item['Fdatetime'].split()[0]
                item['Fsite'] = row["shd_site_%d" % i]
                item['Freminder'] = row["shd_tips_%d" % i]
                item['Fuid_stf'] = row["shd_stff_id_%d" % i]
                item['Fname_stf'] = row["shd_stff_nm_%d" % i]
                item['Ftitle_stf'] = row["shd_stff_tt_%d" % i]
                shd_q = self.db.query(OrdersSchedule).filter(
                    OrdersSchedule.Fid == i,
                    OrdersSchedule.Forder_id == order_id,
                    OrdersSchedule.Fdeleted == 0)
                shd_q.update(item)
            # 订单排期以后,设置订单状态为执行中
            self.db.query(Orders).filter(Orders.Fid == order_id).update(
                {Orders.Fstatus: 1}, synchronize_session=False)
        except Exception, e:
            # self.db.rollback()
            raise e
        else:
            self.db.commit()

    def get_schedule_by_order_id(self, order_id):
        pass

    def add_evaluation_of_schedule(self, obj):
        self.db.add(obj)
        self.db.commit()


class TemplateServer(BaseService):
    def __init__(self, db):
        self.db = db

    def set_db(self, db):
        self.db = db

    def get_attention_msg_template(self, uid_mct):
        """获取排期消息模板"""
        return self.db.query(ScheduleAttentionTemplate).filter(
            ScheduleAttentionTemplate.Fmerchant_id == uid_mct,
            ScheduleAttentionTemplate.Fdeleted == 0).all()

    def update_attention_msg_template(self, uid_mct, *argv):
        """更新消息模板"""
        if len(argv) != 5:
            raise "this request info error!"
        for i in range(5):
            qry = self.db.query(ScheduleAttentionTemplate).filter(
                ScheduleAttentionTemplate.Fmerchant_id == uid_mct,
                ScheduleAttentionTemplate.Fschedule_type_id == i,
                ScheduleAttentionTemplate.Fdeleted == 0,
                )
            if qry.scalar():
                qry.update({"Fdescription": argv[i]})
            else:
                att = ScheduleAttentionTemplate()
                att.Fmerchant_id = uid_mct
                att.Fschedule_type_id = i
                att.Fschedule_type_name = _SCHEDULE_TYPE[i]
                att.Fdescription = argv[i]
                self.db.add(att)
        self.db.commit()

    def get_site_template(self, uid_mct):
        """获取排期中的服务地点信息模板"""
        return self.db.query(ScheduleSiteTemplate).filter(
            ScheduleSiteTemplate.Fmerchant_id == uid_mct,
            ScheduleSiteTemplate.Fdeleted == 0
            ).order_by(ScheduleSiteTemplate.Fisdefault.desc()).all()

    def update_site_template(self, uid_mct, **kwargs):
        """更新排期中的服务地点信息模板"""
        if len(kwargs) <= 2:
            raise "this request info error!"
        qry = self.db.query(ScheduleSiteTemplate).filter(
            ScheduleSiteTemplate.Fmerchant_id == uid_mct,
            ScheduleSiteTemplate.Fid == kwargs.get('Fid', '0'),
            ScheduleSiteTemplate.Fschedule_type_id == kwargs['Ftype_id'],
            ScheduleSiteTemplate.Fdeleted == 0,
            )
        if qry.scalar():
            qry.update({'Fsite': kwargs['Fsite']})
        else:
            att = ScheduleSiteTemplate()
            att.Fmerchant_id = uid_mct
            att.Fschedule_type_id = kwargs['Ftype_id']
            att.Fschedule_type_name = _SCHEDULE_TYPE[kwargs['Ftype_id']]
            att.Fsite = kwargs['Fsite']
            self.db.add(att)
        self.db.commit()

    def set_default_site_template(self, uid_mct, **kwargs):
        """设置排期对应的默认地址"""
        if len(kwargs) <= 1:
            raise "this request info error!"
        self.db.query(ScheduleSiteTemplate).filter(
            ScheduleSiteTemplate.Fmerchant_id == uid_mct,
            ScheduleSiteTemplate.Fschedule_type_id == kwargs['Ftype_id'],
            ScheduleSiteTemplate.Fdeleted == 0,
            ScheduleSiteTemplate.Fisdefault == 1,
            ).update({'Fisdefault': 0})
        self.db.query(ScheduleSiteTemplate).filter(
            ScheduleSiteTemplate.Fmerchant_id == uid_mct,
            ScheduleSiteTemplate.Fid == kwargs['Fid'],
            ScheduleSiteTemplate.Fdeleted == 0,
            ).update({'Fisdefault': 1})
        self.db.commit()

    def delete_site_template(self, uid_mct, **kwargs):
        """删除设置的地址"""
        self.db.query(ScheduleSiteTemplate).filter(
            ScheduleSiteTemplate.Fmerchant_id == uid_mct,
            ScheduleSiteTemplate.Fid == kwargs['Fid'],
            ScheduleSiteTemplate.Fdeleted == 0,
            ).update({'Fdeleted': 1})
        self.db.commit()

