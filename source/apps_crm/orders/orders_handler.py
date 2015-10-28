#encoding:utf-8

import tornado
from common.base import BaseHandler

from tornado.web import MissingArgumentError
from utils.error_util import Error
from services.orders.orders import ShowServices, AddServices
from conf.order_conf import _TYPE_ORDER, _SCHEDULE_TYPE, _ORDER_STATUS
from services.orders.order_services import OrderServices
from common.permission_control import company_permission_control
from common.regular_param import CheckHandler
from conf.msg_conf import PASSWD_TEMPLATE,ORDER_CONFIRM_TEMPLATE
from utils.random_utils import create_random_passwd
from utils.message.sms import send_phone_msg
from services.users.user_services import UserServices
from services.departments.department_services import DepartmentService
from models.album_do import Albums
import ujson,sys,datetime
from utils.wx_util import send_msg_to_owner
import setting
from conf.msg_conf import WEIXIN_TEMPLATES
from utils.datetime_util import datetime_format
from datacache.datacache import PageDataCache
from services.staffers.staffer_services import StafferServices
import sys
import xlwt
from tornado.options import options
from utils.oss_file_deal import upload_by_userinput,sign_download_url

order_serice = OrderServices()
user_service = UserServices()
starff_service = StafferServices()

class CHandlerOrdersList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('orders_view')
    def get(self):
        try:
            order_status = self.get_argument('order_status', '')
            uid = self.get_current_user().get('Fmerchant_id')
            search_date = self.get_argument('sch_date','')
            if search_date:
                start_date,tmp,end_date = search_date.split()
            else:
                start_date,end_date = '',''
            search_text = self.get_argument('search_text','')
            TEMP_STATUS = _ORDER_STATUS
            TEMP_STATUS.append('全部订单')
            tmp_status = order_status
            if not tmp_status:
                tmp_status = 3
            db_staffers = StafferServices(self.db)
            staffers = db_staffers.get_staffers(uid)

            order_serice.set_db(self.db)
            query = order_serice.query_order_list_by_status(uid,order_status,start_date=start_date,end_date=end_date,_content=search_text)
            page_data = self.get_page_data(query)
            page_html = page_data.render_page_html()

            self.echo('crm/order/order_list_py.html', {'order_status':order_status,'items': page_data,'stfs':staffers,
                                                       'ORDER_TYPES':_TYPE_ORDER,'SCHEDULE_TYPE':_SCHEDULE_TYPE,
                                                       'page_html':page_html,
                                                        'start_date':start_date,
                                                        'end_date':end_date,
                                                        'search_text':search_text,
                                                        'now':datetime.datetime.now()
                                                       })

        except Exception, e:

            self.echo('crm/404.html')

    def get_order_schedules(self,order_id):
        order_serice.set_db(self.db)
        if order_serice.check_order_permission(self.get_current_user().get('Fmerchant_id'),order_id):
            return order_serice.get_schedule_by_order_id(order_id)
        else:
            return []


    @tornado.web.authenticated
    def post(self):
        self.echo('crm/404.html')


class CHandlerOrdersAdd(BaseHandler, CheckHandler):
    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self):
        department_service = DepartmentService(self.db)
        merchant_id = self.get_current_user().get('Fmerchant_id')
        departments = department_service.get_dpt_list(merchant_id)
        order_serice.set_db(self.db)
        orders_from  = order_serice.query_order_from_conf(merchant_id)
        data=[]
        for d in departments:
            dept={'id':d[0], 'pId':d[4] and d[4] or 0, 'name':d[1]}
            data.append(dept)

        return self.echo('crm/order/order_add_py.html',{'data':data,'orders_from':orders_from,'now':datetime_format(format='%Y-%m-%d')})

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def post(self):
        """添加订单"""
        try:
            self.get_paras_dict()
            if not self.qdict.get('user_name') or not self.qdict.get('user_mobi'):
                return self.write(ujson.dumps({'stat':'error','msg':'用户名或手机号码不能为空'}))
            self.qdict['uid_mct'] = self.get_current_user().get('Fmerchant_id')

            db_orders = AddServices(self.db)
            order, album = db_orders.add_orders(**self.qdict)

            customer_user_id = self.create_user_and_send_msg(album, self.qdict,order)
            order_serice.set_db(self.db)
            order_serice.update_schedule_and_order_customer_id(order.Fid, customer_user_id)
        except Exception,e:
            
            self.db.rollback()
            return self.write(ujson.dumps({'stat':'error','msg':'添加订单失败,失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'ok','msg':''}))

    def create_user_and_send_msg(self, album, args,order):
        '''
        :todo 创建用户并更新到相册信息 同时发送万丈秘法
        :param album:
        :param args:
        :return:
        '''
        user_service.set_db(self.db)
        passwd = create_random_passwd(3)
        content = PASSWD_TEMPLATE%(self.get_current_user().get('Fcompany_name',''),args.get('user_mobi'),passwd)
        is_success,is_create,user = user_service.create_user_by_order(args.get('user_mobi'),passwd,args.get('user_name'))
        if is_create:
            send_phone_msg(args.get('user_mobi'),content)

        if user and user.Fweixin:
            try:
                template = WEIXIN_TEMPLATES.get('new_order_confirm')
                page_cache = PageDataCache(self.db)
                access_token = page_cache.get_access_token(setting.WX_GZH_AppID, setting.WX_GZH_AppSecret)
                send_msg_to_owner(access_token,
                                  user.Fweixin,
                                  template.get('jsonText'),
                                  link=str('http://m.gongzhuhao.com/mobile/20151985112504291695293/schedules'),
                                  template_id=template.get('TEMPLATE_ID'),
                                  first=str('尊敬的{0}，您在“{1}”的生成了一条新订单，详细信息如下:'.format(order.Fuser_name,self.get_current_user().get('Fcompany_name',''))),
                                  keyword1=str(order.Forder_id_user),
                                  keyword2=str(_TYPE_ORDER[order.Forder_type]),
                                  keyword3='****',
                                  keyword4=str(datetime_format(input_date=order.Fcreate_time)),
                                  keyword5=str(album.Fablum_name),
                                  remark='祝您心情愉快，点击查看排期详情')
            except Exception,e:
                print e.message
        if not user:
            raise
        return user.Fid

class CHandlerOrdersUpdate(BaseHandler, CheckHandler):
    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self, order_id):
        try:
            uid = self.get_current_user().get('Fmerchant_id')
            db_orders = ShowServices(self.db)
            order_serice.set_db(self.db)
            #db_orders.check_order_owner(uid, order_id)
            o,staffs = db_orders.get_order_info(order_id,uid)
            item = {}
            item['order_id'] = o.Fid
            item['order_id_user'] = o.Forder_id_user
            item['order_name'] = o.Fuser_name
            item['order_mobi'] = o.Fuser_mobi
            item['order_user_birth'] = str(o.Fuser_birth)
            item['order_type'] = o.Forder_type
            if o.Forder_type in (1,'1'):  # 婚纱
                item['order_name_ex'] = o.Fuser_name_ex
                item['order_mobi_ex'] = o.Fuser_mobi_ex
                item['order_birth_ex'] = str(o.Fuser_birth_ex)
            item['order_amount'] = int(o.Famount)
            item['order_date'] = str(o.Fcreate_time)
            item['order_comment'] = o.Fcomment
            item['order_stf_id'] = o.Fuid_stf#.replace('&', ' ')
            if staffs:
                item['order_stf_name'] = ' '.join([n.Fname for n in staffs])
            else:item['order_stf_name'] = ''
            item['pre_order_acount'] = o.Fdeposit
            department_service = DepartmentService(self.db)
            departments = department_service.get_dpt_list(uid)
            starff_service.set_db(self.db)
            if item['order_stf_id']:
                user_ids = item['order_stf_id'].split('&')
            else:user_ids=[]
            department_ids=[]

            _order_from = ','.join([str(d[0]) for d in order_serice.query_orderfromids_by_order_id(o.Fid,uid)])
            orders_fron_conf = order_serice.query_order_from_conf(uid)
            retainages = order_serice.query_retainages(o.Fid)
            if user_ids:
                department_ids = starff_service.get_department_id_by_user(user_ids)
                department_ids =list(set([d[0] for d in department_ids if d]))

            data = []
            for d in departments:
                dept = {'id': d[0], 'pId': d[4] and d[4] or 0, 'name': d[1]}
                data.append(dept)
            self.echo('crm/order/order_edit_py.html', {
                'item': item,
                'retainages':retainages,
                'data': data, 'staffers': staffs,'department_ids':department_ids,'_order_from':_order_from,'orders_from':orders_fron_conf})
        except Exception, e:
            print e
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            self.write(Error(3, 'error').__dict__)

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def post(self, order_id):
        try:
            # res = self.check_args(
            #     user_birth='',
            #     user_birth_ex='',
            #     user_name_ex='',
            #     user_mobi_ex='',
            #     comment=''
            # )
            # if res:
            #     raise Error(2000, res, "参数错误")
            self.get_paras_dict()
            if not self.qdict.get('user_name') or not self.qdict.get('user_mobi'):
                return self.write(ujson.dumps({'stat':'error','msg':'用户名或手机号码不能为空'}))
            self.qdict['uid_mct'] = self.get_current_user().get('Fmerchant_id')
            db_orders = AddServices(self.db)
            db_orders.update_orders(**self.qdict)
        except Exception,e:
            
            return self.write(ujson.dumps({"stat":'error','msg':'修改失败，失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'ok','msg':''}))
        #     self.write(Error(0, 'succ').__dict__)
        # except MissingArgumentError, e:
        #     err_msg = "lack param[%s]" % e.arg_name
        #     return self.write(Error(1, err_msg).__dict__)
        # except Error, e:
        #     return self.write(e.__dict__)
        # except Exception, e:
        #     if self.settings.get('debug'):
        #         self.write(str(e))
        #         raise
        #     err_msg = "update failed"
        #     self.write(Error(2, err_msg).__dict__)


class OrderConfirmHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('send_photoes')
    def get(self,order_id,*args, **kwargs):

        data={'status':'ok','info':'通知成功'}
        order_serice.set_db(self.db)
        try:
            album = self.db.query(Albums).filter(Albums.Fuid_mct == self.get_current_user().get('Fmerchant_id'),Albums.Forder_id == order_id,Albums.Fdeleted == 0).scalar()
            if album:
                if album.Ftotal==0:
                    data={'status':'error','info':'还没有精修图'}
                    self.write(ujson.dumps(data))
                else:
                    order_serice.confirm_order(self.get_current_user().get('Fmerchant_id'),order_id)
                order = order_serice.get_order_by_id(order_id,self.get_current_user().get('Fmerchant_id')).scalar()

                template = WEIXIN_TEMPLATES.get('photo_confirm')
                page_cache = PageDataCache(self.db)
                access_token = page_cache.get_access_token(setting.WX_GZH_AppID, setting.WX_GZH_AppSecret)
                user_service.set_db(self.db)
                user = user_service.get_user_by_id(album.Fuser_id)
                #access_token,open_id,jsonText,**kargs
                if user:
                    send_msg_to_owner(access_token,
                                  user.Fweixin,
                                  template.get('jsonText'),
                                  link=str('http://m.gongzhuhao.com/mobile/20151985112504291695293/photolist/'+str(album.Fid)),
                                  template_id=template.get('TEMPLATE_ID'),
                                  first=str('尊敬的{0}，您在“{1}”拍摄的照片已经发送给你,详细信息如下:'.format(order.Fuser_name,self.get_current_user().get('Fcompany_name',''))),
                                  keyword1=str(order.Forder_id_user),
                                  keyword2=str(_TYPE_ORDER[order.Forder_type]),
                                  keyword3=str(album.Ftotal),
                                  remark='你可以通过点击详情，接收照片')
                #user_service.set_db(self.db)
                #user_service.get_user_by_id()
                #user = order_serice.get_user_by_order_id(self.get_current_user().get('Fmerchant_id'),order_id)
                if user:
                    content = ORDER_CONFIRM_TEMPLATE%(self.get_current_user().get('Fcompany_name'))
                    send_phone_msg(user.Fuser_mobi,content)
                self.write(ujson.dumps(data))
            else:
                data={'status':'error','info':'还没有精修图'}
                self.write(ujson.dumps(data))


        except Exception,e:
            
            data['status']='error'
            data['info']='通知失败:'+e.message
            self.write(ujson.dumps(data))

    def post(self, *args, **kwargs):
        pass



class OrderQueryHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('orders_view')
    def get(self,order_type='', **kwargs):

        uid = self.get_current_user().get('Fmerchant_id')
        search_date = self.get_argument('sch_date','')
        if search_date:
            start_date,tmp,end_date = search_date.split()
        else:
            start_date,end_date = '',''
        search_text = self.get_argument('search_text','')
        db_staffers = StafferServices(self.db)
        staffers = db_staffers.get_staffers(uid)
        order_serice.set_db(self.db)

        query = order_serice.query_orders_by_schedule_state(uid,order_type,start_date=start_date,end_date=end_date,_content=search_text)
        page_data = self.get_page_data(query)
        page_html = page_data.render_page_html()

        url = 'crm/order/order_schedule_list.html'
        if order_type=='8':
            url = 'crm/order/order_delete_list.html'
        self.echo(url, {'order_status':order_type,'items': page_data,'stfs':staffers,
                                                   'ORDER_TYPES':_TYPE_ORDER,'SCHEDULE_TYPE':_SCHEDULE_TYPE,
                                                   'page_html':page_html,
                                                    'start_date':start_date,
                                                    'end_date':end_date,
                                                    'search_text':search_text,
                                                    'now':datetime.datetime.now()
                                                   })

    def get_order_schedules(self,order_id):
        order_serice.set_db(self.db)
        if order_serice.check_order_permission(self.get_current_user().get('Fmerchant_id'),order_id):
            return order_serice.get_schedule_by_order_id(order_id)
        else:
            return []

class OrderDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self,order_id):
        try:
            uid = self.get_current_user().get('Fmerchant_id')
            order_serice.set_db(self.db)
            order_serice.delete_order_by_orderid_and_merchantid(order_id,uid)
        except Exception,e:
            pass
        self.write(ujson.dumps({'stat':'1000','msg':'订单删除成功'}))

from models.order_do import Orders,OrderSignUser,OrderFromConf,OrdersFrom,OrderDataBackup
from models.schedule_do import OrdersSchedule,SchedulePlan

class OrdersBackupHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self, *args, **kwargs):

        merchant_id = self.get_current_user().get('Fmerchant_id')
        order_back = self.db.query(OrderDataBackup).filter(OrderDataBackup.Fmerchant_id==merchant_id).order_by('Fcreate_time desc')
        self.echo('crm/order/orders_backup.html',{
                'start_date':datetime_format(format='%Y-%m-%d',input_date=datetime.datetime.now()-datetime.timedelta(days=31)),
                'end_date':datetime_format('%Y-%m-%d'),
                'query':order_back
            })


    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def post(self, *args, **kwargs):


        merchant_id = self.get_current_user().get('Fmerchant_id')
        back_date = self.get_argument('sch_date')
        start_date,tmp,end_date = back_date.split()
        orders = self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fuid_mct==merchant_id,Orders.Fcreate_time>=start_date,Orders.Fcreate_time<=end_date).order_by('Fcreate_time')

        name = u'订单数据备份'
        file_name = u'订单数据导出'+'.xls'
        clumns = (u'订单时间',u'类型',u'订单号',u'金额',u'定金',u'接单人',
                  u'来源',u'备注',u'主用户名/新娘',u'手机号',u'生日',u'新郎',
                  u'手机号',u'生日',
                  u'试衣时间',u'礼服师',u'地点',
                  u'摄影时间',u'档期类型',u'摄影师',u'化妆师',u'地点',
                  u'选样时间',u'选样师',u'地点',
                  u'定稿时间',u'看样师',u'地点',
                  u'取件时间',u'客服',u'地点')

        from conf.order_conf import _TYPE_ORDER as ORDER_TYPES
        file = xlwt.Workbook(encoding='utf-8') #注意这里的Workbook首字母是大写，无语吧
        table = file.add_sheet(name)

        table.write_merge(0, 0, 0, 31,name)
        clumn_index=0
        for c in clumns:
            table.write(1,clumn_index,c)
            clumn_index+=1
        index=2
        for i in xrange(7):
            table.col(i).width = 5000

        # orders_conf = self.db.query(OrderFromConf).filter(OrderFromConf.Fmerchant_id==merchant_id,OrderFromConf.Fdeleted==0)
        # order_conf={}
        # for conf in orders_conf:
        #     order_conf[conf.Fid]=conf.Fname


        def get_sign_names(order_id):
            data = self.db.query(OrderSignUser.Fstaff_name).filter(OrderSignUser.Forder_id ==order_id)
            if data:
                return ','.join([d[0] for d in data])
            else:
                return ''
        def get_schedules(order_id):
            order_scheduls = self.db.query(OrdersSchedule).filter(OrdersSchedule.Forder_id==order_id).order_by('Fid')
            schedules = []
            # Foperation_id = Column(Integer, nullable=True)                              #操作人ID
            # Fnotified_num = Column(SmallInteger, default=0)                             # 此排期已通知用户次数0未通知
            # Fschedule_category_id = Column(Integer,doc='排期分类',nullable=True)         #档期分类id
            # Fschedule_category_name = Column(String(128),default='',doc='排期分类名称')   #档期分类name
            #
            # Fdatetime = Column(DateTime)                                                # 此排期时间
            # Fshot_date = Column(Date)                                                   # 此排期时间  精确到某一天
            #
            # Fsite = Column(String(128), default='')                             # 服务地点
            # Fuid_stf = Column(String(256), default='')                          # 排期中参与的员工ID
            # Fname_stf = Column(String(256), default='')                         # 排期中参与的员工姓名
            # Ftitle_stf = Column(String(256), default='')                        # 排期中员工职称
            # Freminder = Column(String(512), default='')                         # 温馨提示

            for os in order_scheduls:
                schedules.append(datetime_format(input_date=os.Fdatetime))
                if os.Fid==1:
                    schedules.append(os.Fschedule_category_name)
                    tmp_s=[]
                    if os.Fname_stf:
                        tmp_s = os.Fname_stf.split('&')
                        if len(tmp_s)==2:
                            schedules.extend(tmp_s)
                        elif len(tmp_s)==1:
                            schedules.append(os.Fname_stf)
                    else:
                        schedules.append('')
                        schedules.append('')
                else:
                    schedules.append(os.Fname_stf)
                schedules.append(os.Fsite)
            return schedules


        for order in orders:
            table.write(index,0,datetime_format(format='%Y-%m-%d',input_date=order.Fcreate_time))
            table.write(index,1,ORDER_TYPES[order.Forder_type])
            table.write(index,2,order.Forder_id_user)
            table.write(index,3,str(order.Famount))
            table.write(index,4,str(order.Fdeposit))
            table.write(index,5,str(get_sign_names(order.Fid)))

            order_confs = self.db.query(OrdersFrom.Ffrom_name).filter(OrdersFrom.Forder_id==order.Fid)
            oconfs = ''
            if order_confs.count()>0:
                oconfs = ','.join([ of.Ffrom_name for of in order_confs ])
            table.write(index,6,str(oconfs))
            table.write(index,7,order.Fcomment)
            table.write(index,8,order.Fuser_name)
            table.write(index,9,order.Fuser_mobi)
            table.write(index,10,'')
            table.write(index,11,order.Fuser_name_ex)
            table.write(index,12,order.Fuser_mobi_ex)
            table.write(index,13,'')
            schedule_index=14
            for s in get_schedules(order.Fid):
                table.write(index,schedule_index,s)
                schedule_index+=1
            index+=1
        file.save(file_name)
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+file_name)
        contents=''
        with open(file_name, 'rb') as f:
            contents = data = f.read()
            self.write(data)

        save_name='excel/'+str(merchant_id)+"/"+datetime_format(format="%Y%m%d%H%M")+'/'+file_name
        is_ok = upload_by_userinput(options.MEDIA_BUCKET,file_name,save_name,contents)
        if is_ok=='OK':
            request_url = options.MEDIA_DOMAIN+'/'+save_name
            order_back = OrderDataBackup()
            order_back.Fmerchant_id = merchant_id
            order_back.Fback_url = request_url
            order_back.Fsave_name = save_name
            order_back.Fstart_date = start_date
            order_back.Fend_date = end_date
            self.db.add(order_back)
            self.db.commit()
        self.finish()

class OrderBackDownload(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('orders_edit')
    def get(self, backup_id, **kwargs):

        merchant_id = self.get_current_user().get('Fmerchant_id')
        back_up = self.db.query(OrderDataBackup).filter(OrderDataBackup.Fid==backup_id,OrderDataBackup.Fmerchant_id==merchant_id).scalar()
        down_load_url = sign_download_url(back_up.Fback_url,options.MEDIA_BUCKET,back_up.Fsave_name)
        # self.set_header ('Content-Type', 'application/octet-stream')
        #
        # self.set_header ('Content-Disposition', 'attachment; filename='+)
        # contents=''
        # with open(file_name, 'rb') as f:
        #     contents = data = f.read()
        #     self.write(data)
        # self.finish()
        self.redirect(down_load_url)