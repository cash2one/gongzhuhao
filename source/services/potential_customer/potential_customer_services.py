#encoding:utf-8
__author__ = 'binpo'
from services.base_services import BaseService
import datetime
from models.share_do import PotentialCustomer,PotentialCustomerVisit
ACCESS_STATUS={
    '1':'未接通',
    '2':'有意向',
    '3':'无意向'
}

class PotentialCustomerServices(BaseService):

    def query_potential_customer_list(self,merchant_id):
        '''
        :todo 根据商户ID查询所有潜客信息
        :param merchant_id:
        :return:
        '''
        return self.db.query(PotentialCustomer).\
            filter(PotentialCustomer.Fdeleted==0,PotentialCustomer.Fmerchant_id==merchant_id).\
            order_by('Fcreate_time desc')

    def query_potential_customer_visits(self,merchant_id,potential_customer_id):
        '''
        :todo 获取回访纪录
        :param merchant_id:
        :param potential_customer_id:
        :return:
        '''
        return self.db.query(PotentialCustomerVisit).\
            filter(PotentialCustomerVisit.Fdeleted==0,PotentialCustomerVisit.Fmerchant_id==merchant_id,PotentialCustomerVisit.Fpotential_customer_id==potential_customer_id)\
            .order_by('Fcreate_time desc')

    def create_potential_customer(self,**kargs):
        '''
        :todo 创建潜客数据
        :param kargs:
        :return:
        '''

        potential_customer = PotentialCustomer()
        potential_customer.Fuser_photos_share_id = kargs.get('phonts_id')
        potential_customer.Fshare_user_id = kargs.get('share_user_id')
        potential_customer.Fshare_name = kargs.get('share_name')
        potential_customer.Fmerchant_id = kargs.get('merchant_id')
        potential_customer.Fcompany_id = kargs.get('company_id')
        potential_customer.Fpotential_customer_name = kargs.get('customer_name')
        potential_customer.Fpotential_customer_phone = kargs.get('customer_phone')
        self.db.add(potential_customer)
        self.db.commit()

    def get_potential_customer_by_id(self,merchant_id,potential_customer_id):
        '''
        :todo 根据 商户ID 回访id 获取数据
        :param merchant_id:
        :param potential_customer_id:
        :return:
        '''
        return self.db.query(PotentialCustomer).filter(PotentialCustomer.Fmerchant_id==merchant_id,PotentialCustomer.Fid==potential_customer_id).scalar()
    def create_potential_customer_visits(self,merchant_id,**kargs):
        '''
        :todo 潜客回访
        :param kargs:
        :return:
        '''
        pc_customer = self.get_potential_customer_by_id(merchant_id,kargs.get('potential_customer_id'))
        potential_custmer_visit = PotentialCustomerVisit()
        potential_custmer_visit.Fpotential_customer_id = kargs.get('potential_customer_id')
        potential_custmer_visit.Fintention = ACCESS_STATUS.get(kargs.get('is_access'),'未接通')

        potential_custmer_visit.Fmerchant_id = merchant_id
        potential_custmer_visit.Fshare_name = pc_customer.Fshare_name#kargs.get('share_name')

        potential_custmer_visit.Fdesc = kargs.get('remark')
        potential_custmer_visit.Fvistor = kargs.get('visitor_user')
        self.db.add(potential_custmer_visit)
        self.db.query(PotentialCustomer).filter(PotentialCustomer.Fid==kargs.get('potential_customer_id'))\
            .update({'Fintention':ACCESS_STATUS.get(kargs.get('is_access'),'未接通'),'Fmodify_time':datetime.datetime.now()})
        self.db.commit()

