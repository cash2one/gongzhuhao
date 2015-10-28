#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from conf.work_conf import SERIES_KEYS
from services.series.series_services import SeriesServices
from services.company.company_services import CompanyServices
from services.activities.activities_service import ActivitiesService
import sys
import ujson

company_service = CompanyServices()
series_service = SeriesServices()
activity_service = ActivitiesService()

class CreateActivityHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):

        series_service.set_db(self.db)
        try:
            series = series_service.query_series()
            self.echo('ops/activities/create_activity.html',{'series':series})
        except Exception,e:
            self.echo('ops/500.html')

    def post(self, *args, **kwargs):

        self.get_paras_dict()

        try:
            series_id = self.qdict.get('series_id')
            end_date = self.qdict.get('expire_time')
            series_service.set_db(self.db)
            series = series_service.query_series(id = series_id).scalar()

            data = self.obj_to_dict(series,SERIES_KEYS)

            company_service.set_db(self.db)
            company = company_service.get_company_by_uid(series.Fmerchant_id)
            company_gift = company_service.get_gift(series.Fmerchant_id,1).scalar() #到店礼
            order_gift = company_service.get_gift(series.Fmerchant_id,2).scalar()
            data['company_name'] = company.Fcompany_name
            data['company_gift'] = company_gift.Fcontent if company_gift else ''
            data['order_gift'] = order_gift.Fcontent if order_gift else ''
            data['end_date'] = end_date
            data['product_type'] = 1

            activity_service.set_db(self.db)
            activity_service.create_activity(**data)

        except Exception,e:
            self.echo('ops/500.html')

        self.write(ujson.dumps({'stat':'ok','info':'','data':{}}))

class ActivityListHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):

        activity_service.set_db(self.db)
        query = activity_service.query_activities()
        series = self.get_page_data(query)
        self.echo('ops/activities/activity_list.html',{'page_data':series,'page_html':series.render_admin_html()})


    def post(self, *args, **kwargs):

        self.get_paras_dict()
        activity_id = self.qdict.get('activity_id')
        order_num = self.qdict.get('order_num')

        data = {}
        data['Fsort'] = order_num

        activity_service.set_db(self.db)
        try:
            activity_service.update_activity(activity_id,**data)
        except Exception,e:
            self.echo('ops/500.html')

        self.redirect('/gzh/ops/query/activities')








