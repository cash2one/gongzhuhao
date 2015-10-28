#encoding:utf-8
__author__ = 'binpo'
from apps_mobile.mobile_base import MobileBaseHandler
from services.series.series_services import SeriesServices
from services.work.work_services import WorkServices
from services.orders.order_services import OrderServices
from services.company.company_services import CompanyServices
from services.users.user_services import UserServices
from models.company_do import CompanyGift
from models.company_do import Company
from conf.work_conf import SERIES_KEYS
from conf.merchant import COMPANY_KEYS
from common.permission_control import Mobile_login_control
import sys

series_serivce = SeriesServices()
work_service = WorkServices()
order_service = OrderServices()
company_service = CompanyServices()

class BespeakOrdersHandler(MobileBaseHandler):

    def get(self,order_type,refer_id,merchant_id,**kwargs):
        if self.current_user:
            if not self.current_user.get('Fuser_mobi',None):
               self.current_user['Fuser_mobi'] = UserServices(self.db).get_user_by_id(self.current_user.get('Fid')).Fuser_mobi

        company = self.db.query(Company).filter(Company.Fuser_id == merchant_id,Company.Fdeleted == 0).scalar()
        company_gift = self.db.query(CompanyGift).filter(CompanyGift.Fuid_mct==merchant_id,CompanyGift.Fdeleted==0,CompanyGift.Fgift_type==1).scalar()
        order_gift = self.db.query(CompanyGift).filter(CompanyGift.Fuid_mct==merchant_id,CompanyGift.Fdeleted==0,CompanyGift.Fgift_type==2).scalar()
        phone = self.current_user and self.current_user.get('Fuser_mobi') or ''
        if self.request.uri.startswith('/api/json/'):
            self.write_json({'stat':'ok',
                             'data':{'company_gift':company_gift.Fcontent if company_gift else '',
                                     'order_gift':order_gift.Fcontent if order_gift else '',
                                     'company_name':company.Fcompany_name if company else '',
                                     'phone':phone
                                    },
                             'info':''
                            })
        else:
            self.echo('views/merchant/order.html',{'gift1':company_gift,'gift2':order_gift,'phone':phone},layout='')

    def post(self,order_type,refer_id,merchant_id, **kwargs):

        self.get_paras_dict()
        series_serivce.set_db(self.db)
        series_serivce.query_series()
        order_service = OrderServices(self.db)

        try:
            user_id = self.current_user and self.current_user.get('Fid') or None

            order_service.create_bespeak_orders(merchant_id,order_type,refer_id,self.qdict.get('phone'),user_id=user_id)
            series = series_serivce.query_series(merchant_id=merchant_id).order_by('Fcreate_time desc').limit(2).offset(0)

            if self.request.uri.startswith('/api/json/'):
                company = self.db.query(Company.Fcompany_name).filter(Company.Fdeleted == 0)
                lst_series = []
                for s in series:
                    d = self.obj_to_dict(s,SERIES_KEYS)
                    d.update({'company_name': company.filter(Company.Fuser_id == s.Fmerchant_id).scalar()})
                    lst_series.append(d)

                self.write_json({'stat':'ok','data':lst_series,'info':''})
            else:
                self.echo('views/merchant/order_success.html',{'series':series,'merchant_id':merchant_id},layout='')

        except Exception,e:
            self.captureException(*sys.exc_info())

class UserBespeakHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self, *args, **kwargs):

        try:
            order_service.set_db(self.db)
            company_service.set_db(self.db)
            user_id = self.get_current_user().get('Fid')
            lst_data = []
            bespeak_orders = order_service.query_bespeaker_orders(user_id=user_id)
            for bespeak_order in bespeak_orders:
                company = company_service.get_company_by_uid(bespeak_order.Fmerchant_id)
                company_dict = self.obj_to_dict(company,COMPANY_KEYS)
                lst_data.append(company_dict)

            self.write_json({'stat':'ok','data':lst_data,'info':''})

        except Exception,e:
            pass














