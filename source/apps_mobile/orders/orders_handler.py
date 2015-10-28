# encoding:utf-8

import tornado
from tornado.options import options
from common.base import BaseHandler
from tornado.web import MissingArgumentError
import ujson
import json
from apps_mobile.mobile_base import MobileBaseHandler

from utils.error_util import Error
from utils.upload_utile import upload_to_oss
from services.orders.orders import ShowServices, AddServices
from services.staffers.staffer_services import StafferServices
from conf.order_conf import _TYPE_ORDER, _SCHEDULE_TYPE, _ORDER_STATUS,week_day_dict
from services.orders.order_services import OrderServices
from common.permission_control import company_permission_control
from common.regular_param import CheckHandler
from common.permission_control import Mobile_login_control
from utils.message.sms import send_phone_msg
from conf.msg_conf import PASSWD_TEMPLATE, ORDER_CONFIRM_TEMPLATE
from utils.random_utils import create_random_passwd
from utils.message.sms import send_phone_msg
from services.users.user_services import UserServices
from services.ablums.photos_service import PhotosServices
from services.schedules.schedules_service import ScheduleService
from models.album_do import Albums
from utils.common_util import is_mobile
from utils.datetime_util import datetime_format
from utils.date_util import datetime_format_2
import datetime
import sys

order_serice = OrderServices()
user_service = UserServices()
schedule_service = ScheduleService()

class CHandlerOrdersList(MobileBaseHandler):

    @Mobile_login_control()
    @company_permission_control('orders_view')
    def get(self):
        try:
            order_status = self.get_argument('order_status', '')
            uid = self.get_current_user().get('Fmerchant_id')
            TEMP_STATUS = _ORDER_STATUS
            TEMP_STATUS.append('全部订单')
            tmp_status = order_status
            if not tmp_status:
                tmp_status = 3
            db_staffers = StafferServices(self.db)
            staffers = db_staffers.get_staffers(uid)
            order_serice.set_db(self.db)
            orders = order_serice.query_order_list_by_status(uid)

            user_id = self.get_current_user().get('Fid')
            user_service.set_db(self.db)
            user = user_service.get_user_by_id(user_id)

            lstdata = []
            for order in orders:
                lstdata.append({'id':order.Fid,'user_name':order.Fuser_name,'user_mobi':order.Fuser_mobi,
                                'type':_TYPE_ORDER[order.Forder_type],'order_amount':order.Famount,
                                'order_id':order.Forder_id_user,'create_time':datetime_format_2(format='%Y-%m-%d',input_date=order.Fcreate_time)})

        except Exception,e:
            pass
            return self.write_json({'stat':'1001','list':[],'data':{},'info':'获取订单失败,失败原因:'+e.message})
        self.write_json({'stat':'1000','list':lstdata,'data':{},'info':''})

    def get_order_schedules(self, order_id):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        order_serice.set_db(self.db)
        if order_serice.check_order_permission(uid_mct, order_id):
            return order_serice.get_schedule_by_order_id(order_id)
        else:
            return []

class CHandlerOrdersAdd(MobileBaseHandler):

    @Mobile_login_control()
    @company_permission_control('orders_edit')
    def get(self,operation,sc_id):
        schedule_service.set_db(self.db)
        merchant_id = self.get_current_user().get('Fmerchant_id')
        try:
            schedule_category = schedule_service.query_schedule_category_by_id(merchant_id,sc_id)
            lstdata = []
            for index,order_type in enumerate(_TYPE_ORDER):
                lstdata.append({'order_type_id':index,'order_type':order_type})
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','list':[],'data':{},'info':'发生错误,错误原因:'+e.message})
        self.write_json({'stat':'1000','list':lstdata,'data':{},'info':''})

    @Mobile_login_control()
    @company_permission_control('orders_edit')
    def post(self,operation,sc_id):
        """添加订单"""
        try:
            user_id = self.get_current_user().get('Fid')
            mct_id = self.get_current_user().get('Fmerchant_id')
            if not mct_id:
                return self.write_json({'stat':'1000','list':[],'data':{},'info':'非商户员工不能添加订单'})

            body = ujson.loads(self.request.body)
            data = {}
            data['user_name'] = body.get('user_name','')
            data['order_id_user'] = body.get('order_id_user','')
            data['order_type'] = body.get('order_type_id')
            if operation == '0': #验证录入
                data['schedule_category_id'] = sc_id
            data['user_mobi'] = body.get('user_mobi','')
            data['user_name_ex'] = body.get('user_name_ex','')
            data['amount'] = body.get('amount','')
            data['pre_order_amount'] = body.get('pre_order_amount','')
            data['uid_mct'] = mct_id

            db_orders = AddServices(self.db)
            user_agent = self.request.headers.get('User-Agent')
            user_agent = user_agent.lower()
            if is_mobile(user_agent):  #从微信来的，直接跳转到手机微信页面
                data['user_agent'] = 'mobile'
            order, album = db_orders.add_orders(**data)

            customer_user_id = self.create_user_and_send_msg(album, data)
            order_serice.set_db(self.db)
            order_serice.update_schedule_and_order_customer_id(order.Fid, customer_user_id)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','list':[],'data':{},'info':'An exception occurred,causes:'+e.message})
        self.write_json({'stat':'1000','list':[],'data':{},'info':''})

    def img_compression(self, img_size=0, img_type=''):
        '''
            jpg格式压缩
            原图:876K
            80q压缩:134
            43q压缩:70
            30q压缩:55
        '''
        img_size = img_size/1000
        if img_size > 4000:
            return '@50q_0r.jpg'
        elif img_size > 3000:
            return '@60q_0r.jpg'
        elif img_size > 2000:
            return '@65q_0r.jpg'
        elif img_size > 1000:
            return '@70q_0r.jpg'
        elif img_size > 500:
            return '@90q_0r.jpg'
        elif img_size < 300:
            return ''  # '@100q_0r.jpg'
        else:
            return '@80q_0r.jpg'

    def upload_order_pic(self, user_id, mct_id, album_id, order_id):
        """
        TODO: Docstring for upload_order_pic.
        :user_id: 当前用户ID
        :mct_id: 商户ID
        :album_id: 相册ID
        :returns:
        """
        photo_service = PhotosServices()
        photo_service.set_db(self.db)

        # 检查有没有ablum_id对应的相册
        if not photo_service.check_album_permission(mct_id, album_id):
            raise Error(1, "album not exist", "您的相册不存在")

        file_prex = '/'.join(['album', 'users', album_id, 'exquisite'])
        is_ok, filenames = upload_to_oss(
            self,
            options.IMG_BUCKET,
            param_name='image',
            file_type='img',
            file_prex=file_prex,
            max_size=30,
            water_mark=True)
        f_info = []
        if is_ok:
            for f in filenames:
                f_info.append({
                    "name": f.get('file_name'),
                    "size": f.get('size'),
                    "type": f.get('content_type'),
                    "url": options.IMG_DOMAIN+'/'+f.get('full_name') +
                    self.img_compression(f.get('size')),
                    "full_name": f.get('full_name')
                    })
            photo_service.album_add_photos(
                album_id,
                merchant_id=mct_id,
                user_id=user_id,
                files=f_info,
                is_exquisite=False,
                is_order_pic=True,
                order_id=order_id)
            return f_info[0]
        else:
            return f_info

    def create_user_and_send_msg(self, album, args):
        '''
        :todo 创建用户并更新到相册信息 同时发送万丈秘法
        :param album:
        :param args:
        :return:
        '''
        user_service.set_db(self.db)
        passwd = create_random_passwd(6)
        content = PASSWD_TEMPLATE%(self.get_current_user().get('Fcompany_name',''),passwd,args.get('user_mobi'))
        is_success, is_create, user = user_service.create_user_by_order(args.get('user_mobi'),passwd,args.get('user_name'))
        if is_create:
            send_phone_msg(args.get('user_mobi'), content)
        if user:  # 相册更新用户Id
            album.Fuser_id = user.Fid
            self.db.add(album)
            self.db.commit()
            return user.Fid



class OrderScheduleQueryHandler(MobileBaseHandler):

    @Mobile_login_control()
    @company_permission_control('orders_edit')
    def get(self, *args, **kwargs):
        schedule_service.set_db(self.db)
        try:
            schedules = schedule_service.query_schedule_category(self.get_current_user().get('Fmerchant_id'))
            start_date = datetime_format(format='%Y-%m-%d')
            end_date = datetime_format(format='%Y-%m-%d',input_date=datetime.datetime.now()+datetime.timedelta(days=30))
            lstdata = []
            for schedule in schedules:
                lstdata.append({'id':schedule.Fid,'name':schedule.Fname})
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','list':[],'data':{},'info':'错误,错误原因:'+e.message})
        self.write_json({'stat':'1000','list':lstdata,'data':{'start_date':start_date,'end_date':end_date},'info':''})


    @Mobile_login_control()
    @company_permission_control('orders_edit')
    def post(self, *args, **kwargs):
        body = json.loads(self.request.body)
        start_date = body.get('start_date')
        end_date = body.get('end_date')
        category_id = body.get('category')

        merchant_id = self.get_current_user().get('Fmerchant_id')

        schedule_service.set_db(self.db)
        schedule_category = schedule_service.query_schedule_category_by_id(merchant_id,category_id)
        operation='1'
        if operation=='0':
            self.redirect('/mobile/merchant/orders/add/')
        elif operation=='1':
            try:
                schedule = schedule_service.query_schedule_category_by_id(merchant_id,category_id)
                if schedule:
                    _schedules = schedule_service.query_available_schedule_by_input_time_and_category(category_id,merchant_id,start_date,end_date)
                else:
                    _schedules=[]
                lstdata = []
                for schedule in _schedules:
                    lstdata.append({'date':datetime_format(format='%Y-%m-%d',input_date=schedule[0]),
                                    'week_day':week_day_dict[schedule[0].weekday()],'total':schedule[2]})
            except Exception,e:
                pass
                return self.write_json({'stat':'1001','list':[],'data':{},'info':'查询错误,错误原因:'+e.message})
            self.write_json({'stat':'1000',
                             'list':lstdata,
                             'data':{'schedule_category_id':schedule_category.Fid,
                                     'schedule_category_name':schedule_category.Fname,
                                     'start_date':start_date,
                                     'end_date':end_date
                                    }
                            })
        else:
            self.write_json({'stat':'1000','list':[],'data':{},'info':'not found result'})


class CHandlerOrdersUpdate(MobileBaseHandler, CheckHandler):

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self, order_id):
        try:
            uid = self.get_current_user().get('Fmerchant_id')
            db_orders = ShowServices(self.db)
            db_orders.check_order_owner(uid, order_id)
            o, s = db_orders.get_order_info(order_id)
            item = {}
            item['order_id'] = o.Fid
            item['order_id_user'] = o.Forder_id_user
            item['order_name'] = o.Fuser_name
            item['order_mobi'] = o.Fuser_mobi
            item['order_user_birth'] = str(o.Fuser_birth)
            item['order_type'] = o.Forder_type
            if o.Forder_type == '1':  # 婚纱
                item['order_name_ex'] = o.Fuser_name_ex
                item['order_mobi_ex'] = o.Fuser_mobi_ex
                item['order_birth_ex'] = str(o.Fuser_birth_ex)
            item['order_amount'] = float(o.Famount)
            item['order_date'] = str(o.Fcreate_time)
            item['order_comment'] = o.Fcomment
            if s:
                item['staff_id'] = s.Fid
                item['staff_name'] = s.Fname
                item['staff_department_name'] = s.Fdepartment_name
                item['staff_photo_url'] = s.Fphoto_url
            db_staffers = StafferServices(self.db)
            staffers = db_staffers.get_staffers(uid)
            self.echo('apps_crm/order/order_edit_py.html', {
                'item': item, 'stfs': staffers})
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            self.write(Error(3, 'error').__dict__)

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def post(self, order_id):
        try:
            res = self.check_args(
                user_birth='',
                user_birth_ex='',
                user_name_ex='',
                user_mobi_ex='',
                comment=''
            )
            if res:
                raise Error(2000, res, "参数错误")

            self.get_paras_dict()
            self.qdict['uid_mct'] = self.get_current_user().get('Fmerchant_id')
            db_orders = AddServices(self.db)
            db_orders.update_orders(**self.qdict)
            self.write(Error(0, 'succ').__dict__)
        except MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            err_msg = "update failed"
            self.write(Error(2, err_msg).__dict__)

class OrderConfirmHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self, order_id, *args, **kwargs):
        mct_id = self.get_current_user().get('Fmerchant_id')
        order_serice.set_db(self.db)

        try:
            album = self.db.query(Albums).filter(
                Albums.Fuid_mct == mct_id,
                Albums.Forder_id == order_id,
                Albums.Fdeleted == 0
                ).scalar()
            if album:
                if album.Ftotal == 0:
                    e = Error(1, 'error:no adorn pic', '还没有精修图')
                    self.write(e.__dict__)
                else:
                    order_serice.confirm_order(mct_id, order_id)
                    user_service.set_db(self.db)
                    # user_service.get_user_by_id()
                    user = order_serice.get_user_by_order_id(mct_id, order_id)
                    if user:
                        content = ORDER_CONFIRM_TEMPLATE % mct_id
                        send_phone_msg(user.Fuser_mobi, content)
                    self.write(ujson.dumps(Error(0).__dict__))
            else:
                e = Error(1, 'error:no adorn pic', '还没有精修图')
                self.write(e.__dict__)

        except Exception, e:
            err = Error('1', 'notify failed:'+e.message, '通知失败:'+e.message)
            self.write(err.__dict__)







