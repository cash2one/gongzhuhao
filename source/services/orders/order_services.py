#encoding:utf-8
__author__ = 'frank'

from ..base_services import BaseService
from models.order_do import *
from utils.unicode_check import is_chinese
from models.user_do import *
from models.company_do import *
from sqlalchemy import func, or_
from models.schedule_do import *
from services.schedules.schedules_service import ScheduleService
from models.album_do import Albums,AdornPhotos
from services.ablums.photos_service import PhotosServices
from models.order_do import OrderFromConf
import datetime

schedule_service = ScheduleService()
photo_service = PhotosServices()
class OrderServices(BaseService):

    def query_orders(self,user_id=None,**kwargs):
        '''
        todo:查询所有订单
        order_type
        order_status
        merchant_name
        user_name
        :return:
        '''
        query = self.db.query(Orders).filter(Orders.Fdeleted==0)
        if user_id:
            query = query.filter(Orders.Fuid_mct == user_id)
        if kwargs.get('order_type',''):
            query = query.filter(Orders.Forder_type==kwargs.get('order_type'))
        if kwargs.get('order_status',''):
            query = query.filter(Orders.Fstatus==kwargs.get('order_status'))
        if kwargs.get('start_date',''):
            query = query.filter(Orders.Fcreate_time > kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(Orders.Fcreate_time < kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('merchant_name',''):
            company_name = kwargs.get('merchant_name')
            company = self.db.query(Company).filter(Company.Fcompany_name.like('%'+company_name+'%')).scalar()
            query = query.filter(Orders.Fuid_mct == company.Fuser_id)
        if kwargs.get('user_name',''):
            content = kwargs.get('user_name')
            if is_chinese(content.decode('utf-8')):
                query = query.filter(or_(Orders.Fuser_name.like('%'+content+'%')))
            else:
                query = query.filter(or_(Orders.Fuser_name.like('%'+content+'%'),))
        if kwargs.get('order_by',''):
            query = query.order_by(kwargs.get('order_by'))
        else:
            query = query.order_by('Fcreate_time desc')
        return query

    def get_order_by_id(self,order_id,merchant_id=None):
        '''
        todo:根据order_id查找订单
        :param id:
        :return:
        '''
        query = self.db.query(Orders).filter(Orders.Fdeleted == 0)
        if order_id:
            query = query.filter(Orders.Fid == order_id)
        if merchant_id:
            query = query.filter(Orders.Fuid_mct==merchant_id)
        return query


    def delete_order_by_id(self,id):
        '''
        todo:删除订单以及对应的照片，相册，排期
        :param id:
        :return:
        '''
        data = {}
        data['Fdeleted'] = 1
        query_album = self.db.query(Albums).filter(Albums.Forder_id == id,Albums.Fdeleted == 0)#删除相册
        query_photos = self.db.query(AdornPhotos).filter(AdornPhotos.Falbum_id == query_album[0].Fid,AdornPhotos.Fdeleted == 0)
        if query_photos.count()>0 and query_photos:#删除照片
            for photo in query_photos.all():
                photo.Fdeleted = 1
                self.db.add(photo)
        query_order_schedule = self.db.query(OrdersSchedule).filter(OrdersSchedule.Forder_id == id,OrdersSchedule.Fdeleted == 0)
        for order_schedule in query_order_schedule:#删除排期
            order_schedule.Fdeleted = 1
            self.db.add(order_schedule)
        query_album.update(data)
        query_order = self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fid==id) #删除订单
        query_order.update(data)
        self.db.commit()

    def delete_order_by_orderid_and_merchantid(self,orderid,merhant_id):
        '''
        todo:删除订单以及对应的照片，相册，排期
        :param id:
        :return:
        '''
        data = {}
        data['Fdeleted'] = 2
        query_album = self.db.query(Albums).filter(Albums.Forder_id == orderid,Albums.Fdeleted == 0,Albums.Fuid_mct==merhant_id)#删除相册
        if query_album.count()>0:
            query_photos = self.db.query(AdornPhotos).filter(AdornPhotos.Falbum_id==query_album[0].Fid,AdornPhotos.Fuid_mct == merhant_id,AdornPhotos.Fdeleted == 0)
            if query_photos.count()>0 and query_photos:#删除照片
                for photo in query_photos.all():
                    photo.Fdeleted = 2
                    self.db.add(photo)
        query_order_schedule = self.db.query(OrdersSchedule).filter(OrdersSchedule.Forder_id == orderid,OrdersSchedule.Fmerchant_id==merhant_id,OrdersSchedule.Fdeleted == 0)
        for order_schedule in query_order_schedule:#删除排期
            order_schedule.Fdeleted = 2
            self.db.add(order_schedule)
        query_album.update(data)
        query_order = self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fid==orderid,Orders.Fuid_mct==merhant_id) #删除订单
        query_order.update(data)
        self.db.commit()

    def get_schedule_by_order_id(self, order_id):
        '''
        根据order_id获取订单排期
        :param order_id:
        :return:
        '''
        query = self.db.query(OrdersSchedule).filter(
            OrdersSchedule.Forder_id == order_id,
            OrdersSchedule.Fdeleted == 0).order_by('Fid')
        return query

    def query_order_list_by_status(self,user_id,order_status=None,**kargs):
        '''
        :todo 根据商户ID和订单状态查询订单列表
        :param user_id:
        :param order_status:
        :return:
        '''
        query=self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fuid_mct==user_id)
        if order_status:
            query=query.filter(Orders.Fstatus==order_status)
        if kargs.get('start_date',None):
            query = query.filter(Orders.Fcreate_time>=kargs.get('start_date'))
        end_date = kargs.get('end_date')
        if end_date:
            if len(end_date.strip())<=10:
                end_date = end_date.strip()+' 23:59:59'
            query = query.filter(Orders.Fcreate_time<=end_date)
        if kargs.get('_content',None):
            query = query.filter(
                or_(Orders.Fuser_name.like('%{0}%'.format(kargs.get('_content'))),
                    Orders.Forder_id_user.like('%{0}%'.format(kargs.get('_content'))),
                    Orders.Fuser_mobi.like('%{0}%'.format(kargs.get('_content'))))
            )
        query = query.order_by('Fcreate_time desc')
        return query


    def query_orders_by_schedule_state(self,user_id,schedule_state=None,**kargs):
        '''
        :todo 根据商户ID和订单状态查询订单列表
        :param user_id:
        :param order_status:
        :return:
        '''
        # if order_status:
        #     query=query.filter(Orders.Fstatus==order_status)
        #today = datetime.datetime.now()
        today = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d')
        if schedule_state=='8':
            query = self.db.query(Orders).filter(Orders.Fdeleted==2)
        else:
            query=self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fuid_mct==user_id)
            if schedule_state=='0':
                query = query.filter(Orders.Fshot_time==None).order_by('Fcreate_time desc')
            elif schedule_state=='1':
                #query = query.filter(Orders.Fshot_time!=None,Orders.Ffitting_time==None).order_by('Fshot_time desc')
                query = query.filter(Orders.Fshot_time>=today).order_by('Fshot_time')
            elif schedule_state=='2':
                query = query.filter(Orders.Fshot_time<=today,Orders.Fshot_time!=None).order_by('Fshot_time desc')
                #query = query.filter(Orders.Ffitting_time!=None,Orders.Fselect_time==None).order_by('Ffitting_time desc')
            elif schedule_state=='3':
                #query = query.filter(Orders.Fselect_time!=None,Orders.Fcertain_time==None).order_by('Fselect_time desc')
                query = query.filter(Orders.Fselect_time<=today,Orders.Fselect_time!=None).order_by('Fselect_time desc')
            elif schedule_state=='4':
                query = query.filter(Orders.Fcertain_time<=today,Orders.Fcertain_time!=None).order_by('Fcertain_time desc')
                #query = query.filter(Orders.Fcertain_time!=None,Orders.Fabtain_time==None).order_by('Fcertain_time desc')
            elif schedule_state=='5':
                #query = query.filter(Orders.Fabtain_time<=today).order_by('Fabtain_time desc')
                query = query.filter(Orders.Fabtain_time!=None,Orders.Fabtain_time>datetime.datetime.now()).order_by('Fabtain_time desc')
            elif schedule_state=='6':
                query = query.filter(Orders.Fabtain_time<=datetime.datetime.now()).order_by('Fabtain_time desc')
            elif schedule_state=='7':
                query = query.order_by('Fcreate_time desc')

        query = query.filter(Orders.Fuid_mct==user_id)
        if kargs.get('start_date',None):
            query = query.filter(Orders.Fcreate_time>=kargs.get('start_date'))
        end_date = kargs.get('end_date')
        if end_date:
            if len(end_date.strip())<=10:
                end_date = end_date.strip()+' 23:59:59'
            query = query.filter(Orders.Fcreate_time<=end_date)
        if kargs.get('_content',None):
            query = query.filter(
                or_(Orders.Fuser_name.like('%{0}%'.format(kargs.get('_content'))),
                    Orders.Forder_id_user.like('%{0}%'.format(kargs.get('_content'))),
                    Orders.Fuser_mobi.like('%{0}%'.format(kargs.get('_content'))))
            )
        #query = query.order_by('Fcreate_time desc')
        return query

    def check_order_permission(self,user_id,order_id):
        '''
        检查用户订单全县
        :param user_id:
        :param order_id:
        :return:
        '''
        return self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fid==order_id,Orders.Fuid_mct==user_id).scalar()

    def create_add(self,user_id,**kwargs):
        '''
        todo:创建订单、排期、默认相册
        :param user_id: 商户id
        :param kwargs:
        :return:
        '''
        order = Orders()
        order.Forder_id_user = kwargs.get('operation_order_id')
        order.Fuid_mct = user_id
        order.Forder_type = int(kwargs.get('order_type'))
        order.Fuser_name = kwargs.get('bride_name')
        album_name = order.Fuser_name
        order.Fuser_mobi = kwargs.get('bride_mobi')
        order.Fuser_birth = kwargs.get('bride_birth')
        if kwargs.get('groom_name',''):
            order.Fuser_name_ex = kwargs.get('groom_name')
            album_name = album_name+'&'+order.Fuser_name_ex
        if kwargs.get('groom_mobi'):
            order.Fuser_mobi_ex = kwargs.get('groom_mobi')
        if kwargs.get('groom_birth',''):
            order.Fuser_birth_ex = kwargs.get('groom_birth')
        order.Fuid_stf = kwargs.get('staffer')
        order.Famount = kwargs.get('order_price')
        order.Fstatus = 0 #conf.order_conf._ORDER_STATUS 初始状态
        if kwargs.get('comment',''):
            order.Fcomment = kwargs.get('comment')
        self.db.add(order)
        self.db.commit()
        schedule_service.set_db(self.db)
        photo_service.set_db(self.db)
        schedule_service.create_order_schedule(order.Fid,user_id)
        photo_service.create_albums(order.Fid,order.Fuid_mct,album_name,str(order.Forder_type))

    def update_order_by_id(self,order_id,**kwargs):
        query = self.db.query(Orders).filter(Orders.Fdeleted == 0,Orders.Fid == order_id)
        kwargs.pop('_xsrf')
        query.update(kwargs)
        self.db.commit()


    def update_schedule_and_order_customer_id(self,order_id,customer_id):
        '''
        :更新订单排期和商户
        :param order_id:
        :param customer_id:
        :return:
        '''
        self.db.query(OrdersSchedule).filter(OrdersSchedule.Forder_id==order_id).update({'Fcustomer_id':customer_id},synchronize_session=False)
        self.db.query(Orders).filter(Orders.Fid==order_id).update({'Fuid':customer_id},synchronize_session=False)
        self.db.query(Albums).filter(Albums.Forder_id==order_id).update({'Fuser_id':customer_id},synchronize_session=False)
        self.db.commit()

    def query_orders_by_customer_id(self,customer_id):
        '''
        :todo 根据客户ID获取订单列表
        :param customer_id:
        :return:
        '''
        return self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fuid!='',Orders.Fuid==customer_id).order_by('Fcreate_time desc')


    def confirm_order(self,merchant_id,order_id):


        '''
        :通知客户 精修图信息
        :param merchant_id:
        :param order_id:
        :return:
        '''
        #self.db.query(AdornPhotos).filter(AdornPhotos.Forder_id==order_id,AdornPhotos.Fuid_mct==merchant_id).update({'Fstatus':1},synchronize_session=False)
        query = self.db.query(Albums).filter(Albums.Forder_id==order_id,Albums.Fuid_mct==merchant_id)
        query.update({'Fstatus':1},synchronize_session=False)
        self.db.query(AdornPhotos).filter(AdornPhotos.Falbum_id==query.scalar().Fid).update({'Fstatus':1},synchronize_session=False)
        self.db.commit()


    def get_user_by_order_id(self,merchant_id,order_id):
        '''
        :todo 根据订单查询用户信息
        :param merchant_id:
        :param order_id:
        :return:
        '''
        user_ids = self.db.query(Orders.Fuid).filter(Orders.Fuid_mct==merchant_id,Orders.Fid==order_id).scalar()
        if order_id and user_ids:
            return self.db.query(Users).filter(Users.Fid==user_ids).scalar()
        return None

    def query_orders_by_schedule_date(self,merchant_id,schedule_type,input_date,schedule_category=None):
        '''
        :todo根据商户 排期类型 日期查询订单
        :param merchant_id:
        :param schedule_type:
        :param date:
        :return:
        '''
        query = self.db.query(OrdersSchedule.Forder_id).filter(OrdersSchedule.Fid==schedule_type,OrdersSchedule.Fshot_date==input_date,OrdersSchedule.Fmerchant_id==merchant_id)
        if schedule_category:
            if schedule_type in (1,'1'):
                query = query.filter(OrdersSchedule.Fschedule_category_id==schedule_category)
        order_id_list = [oid[0] for oid in query if query ]
        return self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fid.in_(order_id_list)).order_by('Fcreate_time')

    def create_evaluation_category(self,**kwargs):
        '''
        todo:添加评价分类
        :param kwargs:
        :return:
        '''
        evaluation_category = EvaluationCategory()
        evaluation_category.Fschedule_type_id = kwargs.get('schedule_type_id','')
        evaluation_category.Fname = kwargs.get('name','')
        self.db.add(evaluation_category)
        self.db.commit()

    def query_order_from_conf(self,merchant_id):
        '''
        :todo 根据商户查询订单来源
        :param merchant_id:
        :return:
        '''

        return self.db.query(OrderFromConf).filter(OrderFromConf.Fdeleted==0,OrderFromConf.Fmerchant_id==merchant_id)

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

    def query_orderfromids_by_order_id(self,order_id,merchant_id):
        '''
        :todo 根据订单ID查询订单来源列表
        :param order_id:
        :param merchant_id:
        :return:
        '''
        return self.db.query(OrdersFrom.Forder_from_id).filter(OrdersFrom.Fmerchant_id==merchant_id,OrdersFrom.Forder_id==order_id)

    def query_retainages(self,order_id):
        '''
        :尾款
        :param order_id:
        :return:
        '''
        return self.db.query(OfflinePayOrder).filter(OfflinePayOrder.Forder_id==order_id)

    def create_bespeak_orders(self,merchant_id,order_type,refer_id,mobile,user_id=None):
        '''
        :todo 创建预约订单
        :param merchant_id:
        :param order_type:
        :param refer_id:
        :param mobile:
        :param user_id:
        :return:
        '''
        query = self.db.query(BespeakOrders).filter(BespeakOrders.Fdeleted == 0,BespeakOrders.Fmobile == mobile)
        bespeak_order = BespeakOrders()

        if user_id:
            bespeak_order.Fuser_id = user_id
        bespeak_order.Fmerchant_id = merchant_id
        bespeak_order.Forder_type = order_type       #1.商户订单,2.套系订单 3.作品订单
        bespeak_order.Frefer_id = refer_id
        bespeak_order.Fmobile = mobile
        bespeak_order.Fstatus = 0
        self.db.add(bespeak_order)
        self.db.commit()

    def query_bespeaker_orders(self,**kwargs):
        '''
        todo:获取预约信息
        :param merchant_id:
        :return:
        '''
        query = self.db.query(BespeakOrders).filter(BespeakOrders.Fdeleted==0).order_by('Fcreate_time desc')

        if kwargs.get('merchant_id',''):
            query = query.filter(BespeakOrders.Fmerchant_id == kwargs.get('merchant_id'))
        if kwargs.get('user_id',''):
            query = query.filter(BespeakOrders.Fuser_id == kwargs.get('user_id'))

        return query

