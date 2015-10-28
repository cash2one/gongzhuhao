#!/usr/bin/env python
# encoding: utf-8

import tornado
from tornado.options import options
from utils.upload_utile import upload_to_oss
from utils.date_util import datetime_format_2
from common.permission_control import Mobile_login_control
from services.orders.order_services import OrderServices
from services.schedules.schedules_service import ScheduleService
from services.orders.orders import ShowServices as OrderShowServices
from services.schedules.schedules import ShowServices
from services.staffers.staffer_services import StafferServices
from services.company.company_services import CompanyServices
from conf.order_conf import _SCHEDULE_TYPE,_EVALUATION_CATEGORY
from apps_mobile.mobile_base import MobileBaseHandler
from utils.datetime_util import datetime_format
import ujson
import sys

_SCHEDULE_WORD = '此阶段尚未排期，请耐心等候'

company_service = CompanyServices()
schedule_service = ScheduleService()


class CWxHandlerOrderList(MobileBaseHandler):
    #查询用户订单

    @Mobile_login_control()
    def get(self):
        try:
            uid = self.get_current_user().get('Fid')
            order_srv = OrderServices(self.db)
            company_service.set_db(self.db)
            orders = order_srv.query_orders_by_customer_id(uid)
            lstdata = []
            for order in orders:
                dictionary = {}
                dictionary['id'] = order.Fid
                dictionary['order_id_user'] = order.Forder_id_user
                dictionary['uid'] = order.Fuid
                dictionary['uid_mct'] = order.Fuid_mct
                company = company_service.get_company_by_uid(order.Fuid_mct)
                dictionary['merchant_logo_url'] = company.Fphoto_url if company else ''
                dictionary['order_type'] = order.Forder_type
                dictionary['user_name'] = order.Fuser_name
                dictionary['user_mobi'] = order.Fuser_mobi
                dictionary['user_birth'] = order.Fuser_birth
                dictionary['uid_stf'] = order.Fuid_stf
                dictionary['amount'] = order.Famount
                dictionary['comment'] = order.Fcomment
                dictionary['create_time'] = datetime_format_2(format="%Y-%m-%d",input_date=order.Fcreate_time)
                lstdata.append(dictionary)
        except Exception, e:
            pass
            return self.write(ujson.dumps({'stat':'1001','list':[],'data':{},'info':'查询用户订单失败,失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','list':lstdata,'data':{},'info':''}))

class CHandlerScheduleH5List(MobileBaseHandler):
    #查看排期
    @Mobile_login_control()
    def get(self, order_id):
        try:
            db_schedule = ShowServices(self.db)
            schedules = db_schedule.get_schedule(order_id)

            db_order = OrderShowServices(self.db)
            order, stf = db_order.get_order_info(order_id)
            company_service.set_db(self.db)
            company = company_service.get_company_by_uid(order.Fuid_mct)
            lstdata = []
            for schedule in schedules:
                dictionary = {}
                dictionary['id'] = schedule.id
                dictionary['schedule_type_id'] = schedule.Fid
                dictionary['schedule_type'] = _SCHEDULE_TYPE[schedule.Fid]
                dictionary['datetime'] = datetime_format_2(format="%Y-%m-%d",input_date=schedule.Fdatetime)
                dictionary['site'] = schedule.Fsite if schedule.Fdatetime else ''
                dictionary['schedule_word'] = _SCHEDULE_WORD if schedule.Fdatetime else ''
                lstdata.append(dictionary)
        except Exception, e:
            pass
            return self.write(ujson.dumps({'stat':'1001','data':{},'info':'获取排期失败,失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','list':lstdata,'data':{'user_name':order.Fuser_name,
                    'create_time':datetime_format_2(format="%Y-%m-%d %H:%M:%S",input_date=order.Fcreate_time),
                    'photo_url':self.get_show_img_url(company.Fphoto_url,128) if company else ''},'info':''}))


class CHandlerScheduleH5Tips(MobileBaseHandler):
    #排期详情
    @Mobile_login_control()
    def get(self, order_id, shd_no):
        '''
        :param order_id: 订单ID
        :param shd_no:
        :return:
        '''
        try:
            db_schedule = ShowServices(self.db)
            schedules = db_schedule.get_schedule(order_id)
            stf_id = schedules[int(shd_no)].Fuid_stf.split('$')[0]
            stf = StafferServices(self.db).get_staffer_by_id_(stf_id)
            schedule = schedules[int(shd_no)] #当前排期
            data = {'staffer_mobi':stf.Fmobi if stf else '',
                    'staffer_title':schedule.Ftitle_stf,
                    'staffer_name':schedule.Fname_stf,
                    'schedule_date':datetime_format_2(format="%Y-%m-%d",input_date=schedule.Fdatetime),
                    'schedule_site':schedule.Fsite if schedule.Fdatetime else '',
                    'schedule_reminder':schedule.Freminder,
                    'schedule_type_id':shd_no
                    }
        except Exception,e:
            pass
            return self.write(ujson.dumps({'stat':'1001','data':{},'list':[],'info':'获取排期详情失败，失败原因:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','data':data,'list':[],'info':''}))

    @tornado.web.authenticated
    def post(self, order_id):
        pass

class OrderEvaluationHandler(MobileBaseHandler):
    #评论
    @Mobile_login_control()
    def get(self,order_id,schedule_type_code):

        print 'schedule_type_code:',schedule_type_code
        print 'order_id:',order_id

        schedule_service.set_db(self.db)
        evaluation_categorys = schedule_service.get_evaluation_by_typeCode(schedule_type_code)
        m_key = str(order_id)+"order_evaluation"+str(schedule_type_code)
        code = self.mcache.get(m_key)
        if code: #更新
            order_evaluation = schedule_service.query_order_evaluations(order_id=order_id,schedule_type_code=schedule_type_code).scalar()
            if int(schedule_type_code) == 1:
                stars = order_evaluation.Fscore.split('&')
                self.write_json({'stat':'1000',
                                 'code':1,
                                 'shot_star':stars[0],
                                 'dressing_star':stars[1],
                                 'content':order_evaluation.Fcontent,
                                 'evaluation_category_name':evaluation_categorys[0].Fname,
                                 'evaluation_category_name_2':evaluation_categorys[1].Fname,
                                })
            else:
                self.write_json({'stat':'1000',
                                 'code':1,
                                 'star':order_evaluation.Fscore,
                                 'content':order_evaluation.Fcontent,
                                 'evaluation_category_name':evaluation_categorys[0].Fname,
                                })
        else:
            if evaluation_categorys.count() > 1:
                self.write_json({'stat':'1000',
                                 'info':'',
                                 'evaluation_category_id':evaluation_categorys[0].Fid,
                                 'evaluation_category_name':evaluation_categorys[0].Fname,
                                 'evaluation_category_id_2':evaluation_categorys[1].Fid,
                                 'evaluation_category_name_2':evaluation_categorys[1].Fname,
                                })
            else:
                self.write_json({'stat':'1000',
                                 'info':'',
                                 'evaluation_category_id':evaluation_categorys[0].Fid,
                                 'evaluation_category_name':evaluation_categorys[0].Fname,
                                })

    @Mobile_login_control()
    def post(self,order_id,schedule_type_code):
        schedule_service.set_db(self.db)
        m_key = str(order_id)+"order_evaluation"+str(schedule_type_code)
        body = ujson.loads(self.request.body)
        code = self.mcache.get(m_key)
        try:
            if code: #更新
                order_evaluation = schedule_service.query_order_evaluations(order_id=order_id,schedule_type_code=schedule_type_code).scalar()
                schedule_service.update_order_evaluation(order_evaluation.Fid,**body)
            else:
                user_id = self.get_current_user().get('Fid')
                order_schedule = schedule_service.get_order_schedule_by_order_id(order_id,schedule_type_code)

                body['user_id'] = user_id
                body['order_id'] = order_id
                body['schedule_type_code'] = schedule_type_code
                body['category_name'] = _EVALUATION_CATEGORY[schedule_type_code]
                body['staffer_name'] = order_schedule.Fname_stf

                order_evaluation = schedule_service.create_order_evaluation(**body)
                self.mcache.set(m_key,1)
            self.write_json({'stat':'1000','info':'','data':order_evaluation.Fid})

        except Exception,e:
            print e.message
            pass

class EvaluationUploadHandler(MobileBaseHandler):

    def post(self,evaluation_id):
        """
        todo:评论传图
        :evaluation_id:评论ID
        :returns:
        """
        schedule_service.set_db(self.db)

        date_format_prefix = datetime_format(format='%Y%m%d')
        file_prex = '/'.join(['evaluation',evaluation_id,date_format_prefix])
        try:
            is_ok, filenames = upload_to_oss(
            self,
            options.IMG_BUCKET,
            param_name='image',
            file_type='img',
            file_prex=file_prex)
            if is_ok:
                for f in filenames:
                    image_url = options.IMG_DOMAIN+'/'+f.get('full_name')
                    schedule_service.create_evaluation_images(evaluation_id,image_url)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})
        self.write_json({'stat':'1000','info':''})

class DeleteImagesHandler(MobileBaseHandler):

    def get(self,order_evaluation_id):
        schedule_service.set_db(self.db)

        try:
            images = schedule_service.get_evaluation_images(order_evaluation_id)
            if images.count():
                for image in images:
                    self.db.delete(image)
                    self.db.commit()
            else:
                pass
        except Exception,e:
            pass
            return self.write_json({'stat':1001,'info':e.message})

        return self.write_json({'stat':200,'info':''})


























