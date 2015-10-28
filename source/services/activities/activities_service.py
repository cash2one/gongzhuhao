#encoding: utf-8
__author__ = 'hongjiongteng'

from services.base_services import BaseService
from models.activity_do import Activity
from models.company_do import Company, CompanyGift
from models.product_do import ShotPackage
from models.activity_do import Activity

class ActivitiesService(BaseService):

    def query_activities(self,**kwargs):
        '''
        todo:查询活动信息
        :return:
        '''
        query = self.db.query(Activity).filter(Activity.Fdeleted == 0)
        if kwargs.get('order_by',''):
            query = query.order_by(kwargs.get('order_by'))
        return query

    def create_activity(self,**kwargs):
        '''
        todo:新增活动
        :param kwargs:
        :return:
        '''
        activity = Activity()
        activity.Fproduct_id = kwargs.get('Fid')
        activity.Fmerchant_id = kwargs.get('Fmerchant_id')
        activity.Fproduct_name = kwargs.get('Fpackage_name')
        activity.Fproduct_type = kwargs.get('product_type')
        activity.Fprice = kwargs.get('Fprice')
        activity.Fsale_price = kwargs.get('Fsale_price')
        activity.Fcompany_name = kwargs.get('company_name')
        activity.Forder_gift = kwargs.get('order_gift')
        activity.Fcompany_gift = kwargs.get('company_gift')
        activity.Fend_date = kwargs.get('end_date')
        activity.Fcover_img = kwargs.get('Fcover_img')

        self.db.add(activity)
        self.db.commit()

        return True,activity

    def update_activity(self,activity_id,**kwargs):
        '''
        todo:更新活动信息
        :param product_id:
        :return:
        '''
        query = self.db.query(Activity).filter(Activity.Fdeleted == 0,Activity.Fid == activity_id)
        query.update(kwargs)
        self.db.commit()

