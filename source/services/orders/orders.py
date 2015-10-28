# encoding:utf-8
from models.order_do import Orders,OrderSignUser,OrdersFrom,OrderFromConf,OfflinePayOrder
from models.schedule_do import OrdersSchedule,\
    ScheduleAttentionTemplate, ScheduleSiteTemplate
from models.staffer_do import Staffers
from models.album_do import Albums
from utils.error_util import Error
from conf.order_conf import _SCHEDULE_REMINDER_MSG,_TYPE_ORDER
from models.staffer_do import Staffers
import datetime
from ..schedules.schedules_service import ScheduleService
schedule_service = ScheduleService()

class ShowServices(object):
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

    def get_order_info(self, order_id,merchant_id=None):
        """获取某个订单信息"""
        if merchant_id:
            order = self.db.query(Orders).\
                filter(Orders.Fid == order_id,
                       Orders.Fuid_mct == merchant_id,Orders.Fdeleted == 0).scalar()
        else:
            order = self.db.query(Orders).filter(
                Orders.Fid == order_id,
                Orders.Fdeleted == 0).scalar()
        if not order:
            raise Error(1, "check uid and orderid failed")
        #print order.Fuid_stf
        try:
            if order.Fuid_stf:
                uid_stf = [int(d) for d in order.Fuid_stf.split('&')]
                #print 'uid_stf:',uid_stf,type(uid_stf)
                staffers = self.db.query(Staffers).filter(
                    Staffers.Fid.in_(uid_stf),
                    Staffers.Fdeleted == 0)
            else:staffers=[]
        except:
            staffers=[]
        return order, staffers

    def get_orders(self, uid_mct):
        """获取商户所有订单列表"""
        orders = self.db.query(Orders).filter(
            Orders.Fuid_mct == uid_mct,
            Orders.Fdeleted == 0
            ).order_by(Orders.Fcreate_time.desc()).all()

        is_schedule, schedules = [], []
        for order in orders:
            shds = self.db.query(OrdersSchedule).filter(
                OrdersSchedule.Forder_id == order.Fid,
                OrdersSchedule.Fdatetime != '',
                OrdersSchedule.Fdeleted == 0
                ).order_by(OrdersSchedule.Fid).all()
            if len(shds) < 5:
                is_schedule.append(False)
            else:
                is_schedule.append(True)
            schedules.append(shds)
        return orders, is_schedule, schedules


class AddServices(object):
    def __init__(self, db):
        self.db = db

    def set_db(self, db):
        self.db = db

    def add_orders(self, **kargs):
        """ 添加订单 """
        schedule_category_id = kargs.get('schedule_category_id',None)
        shot_date = kargs.get('shot_date',None)
        ablum_name = ''
        order = Orders()
        order.Fuid_mct = kargs['uid_mct']
        order.Forder_id_user = kargs['order_id_user']
        order.Forder_type = kargs['order_type']
        order.Fuser_name = kargs['user_name']
        ablum_name = kargs['user_name']
        order.Fuser_mobi = kargs['user_mobi']
        if 'user_birth' in kargs:
            order.Fuser_birth = kargs['user_birth']
        if int(kargs['order_type']) == 1:  # 婚纱
            order.Fuser_name_ex = kargs['user_name_ex']
            if kargs['user_name_ex']:
                ablum_name = ablum_name+'&'+kargs['user_name_ex']
            if 'user_mobi_ex' in kargs:
                order.Fuser_mobi_ex = kargs['user_mobi_ex']
            if 'user_birth_ex' in kargs:
                order.Fuser_birth_ex = kargs['user_birth_ex']
        order.Famount = kargs['amount']
        order.Fdeposit = kargs.get('pre_order_amount',0)
        order.Fcreate_time = kargs.get('create_time')

        if 'uid_stf' in kargs: #接单人
            staffs_id = kargs['uid_stf'].split('&')
            order.Fuid_stf = kargs['uid_stf']
        else:
            order.Fuid_stf = '0'
        if 'comment' in kargs:
            order.Fcomment = kargs['comment']
        if schedule_category_id and shot_date:
            order.Fstatus = 1
        else:
            order.Fstatus = 0  #初始化订单状态
        order.Forder_from = kargs.get('user_agent','apps_crm')
        self.db.add(order)
        self.db.commit()

        self.create_order_froms(order.Fid,kargs['uid_mct'],kargs.get('orders_from',''))
        if 'uid_stf' in kargs:
            self.create_sign_user(order.Fid,staffs_id,kargs['uid_mct'])
        _category_id,_category_name= None,None

        schedule_service.set_db(self.db)
        if schedule_category_id:
            schedule = schedule_service.query_default_category(kargs['uid_mct'],schedule_category_id)
            if schedule:
                _category_id,_category_name = schedule.Fid,schedule.Fname
        self._add_empty_schedules(order.Fid, kargs['uid_mct'],shot_date=shot_date,schedule_category_id=_category_id,schedule_category_name=_category_name)
        abm = self._add_empty_album(order.Fid, order.Fuid_mct, ablum_name,album_type=_TYPE_ORDER[int(kargs['order_type'])])
        self.db.commit()
        return order, abm

    def create_sign_user(self,order_id,staffids,merchant_id,operation='add'):
        '''
        :todo 创建接单人
        :param order_id:
        :param staff_id:
        :return:
        '''
        if operation=='update':
            self.db.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==merchant_id,Staffers.Fid.in_(staffids)).delete(synchronize_session=False)

        if isinstance(staffids,list):
            for sid in staffids:
                staff = self.db.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fid==sid,Staffers.Fuid_mct==merchant_id).scalar()
                if staff:
                    order_sign_user=OrderSignUser()
                    order_sign_user.Forder_id = order_id       #订单号(对内) 21位
                    order_sign_user.Fstaff_id = staff.Fid
                    order_sign_user.Fstaff_name = staff.Fname
                    self.db.add(order_sign_user)
            self.db.commit()

    def create_order_froms(self,order_id,merchant_id,order_from_ids):
        from_ids = [int(_id) for _id in order_from_ids.split(',') if _id]
        for _id in from_ids:
            from_obj = self.query_order_from_by_id(_id,merchant_id)
            order_from = OrdersFrom()
            order_from.Forder_id = order_id                 #订单名称
            order_from.Forder_from_id = _id
            order_from.Fmerchant_id = merchant_id
            order_from.Ffrom_name = from_obj.Fname
            self.db.add(order_from)
        self.db.commit()
        self.db.query(OrdersFrom).filter(OrdersFrom.Forder_id==order_id,OrdersFrom.Fmerchant_id==merchant_id).filter(~OrdersFrom.Forder_from_id.in_(from_ids)).delete(synchronize_session=False)
        self.db.commit()

    def _add_empty_schedules(self, order_id, merchant_id=None, customer_id=None,shot_date=None,schedule_category_id=None,schedule_category_name=None):
        for i in range(5):  # contain 5 schedules every order
            shd = OrdersSchedule()
            shd.Fid = i
            shd.Forder_id = order_id
            msg_tmp = self.db.query(ScheduleAttentionTemplate).filter(
                ScheduleAttentionTemplate.Fmerchant_id == merchant_id,
                ScheduleAttentionTemplate.Fschedule_type_id == i,
                ScheduleAttentionTemplate.Fdeleted == 0
                ).scalar()
            if msg_tmp:
                shd.Freminder = msg_tmp.Fdescription
            else:
                shd.Freminder = _SCHEDULE_REMINDER_MSG[i]
            if merchant_id:
                shd.Fmerchant_id = merchant_id
            if customer_id:
                shd.Fcustomer_id = customer_id

            site_tmp = self.db.query(ScheduleSiteTemplate).filter(
                ScheduleSiteTemplate.Fmerchant_id == merchant_id,
                ScheduleSiteTemplate.Fschedule_type_id == i,
                ScheduleSiteTemplate.Fdeleted == 0
                ).order_by(ScheduleSiteTemplate.Fisdefault.desc()).first()
            if site_tmp:
                shd.Fsite = site_tmp.Fsite
            if i==1:
                if schedule_category_id and shot_date:
                        shd.Fschedule_category_id = schedule_category_id                 #档期分类ID
                        shd.Fschedule_category_name = schedule_category_name             #档期分类名称
                        shd.Fdatetime = shot_date                                        # 此排期时间
                        shd.Fshot_date = shot_date                                       # 此排期时间  精确到某一天
            self.db.add(shd)

    def _add_empty_album(self, order_id, uid_mct, ablum_name,album_type=None):
        abm = Albums()
        abm.Forder_id = order_id
        abm.Fuid_mct = uid_mct
        abm.Fablum_name = ablum_name
        if album_type:
            abm.Falbum_type = album_type
        self.db.add(abm)
        return abm

    def update_orders(self, **kargs):
        """ 更新订单信息 """
        order_id = kargs['order_id']
        order = {}
        album_name = ''
        order['Forder_id_user'] = kargs['order_id_user']
        order['Forder_type'] = kargs['order_type']
        order['Fuser_name'] = kargs['user_name']
        album_name = kargs['user_name']
        order['Fuser_mobi'] = kargs['user_mobi']
        if kargs['user_birth']:
            order['Fuser_birth'] = kargs['user_birth']
        if int(kargs['order_type']) == 1:  # 婚纱
            order['Fuser_name_ex'] = kargs['user_name_ex']
            if kargs['user_name_ex']:
                album_name = album_name+'&'+kargs['user_name_ex']
            order['Fuser_mobi_ex'] = kargs['user_mobi_ex']
            if kargs['user_birth_ex']:
                order['Fuser_birth_ex'] = kargs['user_birth_ex']
        order['Famount'] = kargs['amount']
        order['Fuid_stf'] = kargs['uid_stf']
        order['Fcomment'] = kargs['comment']
        order['Fdeposit'] = kargs.get('pre_order_amount',0)
        order['Fcreate_time'] = kargs.get('create_time')
        qry = self.db.query(Orders).filter(
            Orders.Fid == order_id,
            Orders.Fdeleted == 0)
        if qry:
            qry.update(order)
            self.db.commit()
        self.create_order_froms(order_id,kargs.get('uid_mct'),kargs.get('orders_from',''))
        album = self.db.query(Albums).filter(Albums.Forder_id==order_id).scalar()
        if not album:
            album = Albums()
        album.Fuid_mct = kargs.get('uid_mct')
        album.Fablum_name = album_name
        album.Falbum_type = kargs['order_type']
        album.Fmodify_time = datetime.datetime.now()
        self.db.add(album)
        self.db.commit()
        retainages = kargs.get('retainage','').split(',')
        for tain in retainages:
            if tain:
                offline_pay = OfflinePayOrder()
                offline_pay.Forder_id = order_id
                offline_pay.Famount = tain
                self.db.add(offline_pay)
                self.db.commit()
        return order


    def query_order_from_by_id(self,from_id,merchant_id):
        '''
        :todo 根据订单和商户查询订单来源配置
        :param from_id:
        :param merchant_id:
        :return:
        '''
        return self.db.query(OrderFromConf).filter(OrderFromConf.Fdeleted==0,OrderFromConf.Fmerchant_id==merchant_id,OrderFromConf.Fid==from_id).scalar()

    def query_orderfrom_by_order_id(self,order_id,merchant_id):
        '''
        :todo 根据订单ID查询订单来源列表
        :param order_id:
        :param merchant_id:
        :return:
        '''
        return self.db.query(OrdersFrom).filter(OrdersFrom.Fmerchant_id==merchant_id,OrdersFrom.Forder_id==order_id)
