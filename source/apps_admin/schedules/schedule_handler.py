#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from utils.datetime_util import datetime_format
from models.company_do import Company
from models.user_do import Users
from services.schedules.schedules_service import ScheduleService

schedule_service = ScheduleService()

class QuerySchedulePlanHandler(AdminBaseHandler):
    def get(self,merchant_id):
        current_month = self.get_argument('start_date','')
        current_month = current_month and current_month or datetime_format(format='%Y-%m')
        schedule_service.set_db(self.db)
        schedule_plans = schedule_service.get_merchant_schedule_plan(merchant_id,current_month)
        lstdata = []
        for schedule_plan in schedule_plans:
            data = {}
            data['Fid'] = schedule_plan.Fid
            data['Fuser_id'] = schedule_plan.Fuser_id
            data['Ftotal_per_day'] = schedule_plan.Ftotal_per_day
            data['Fschedule_day'] = schedule_plan.Fschedule_day
            data['plan_count'] = schedule_service.get_oneday_plan(merchant_id,schedule_plan.Fschedule_day)
            if data['plan_count'] > schedule_plan.Ftotal_per_day: #如果已有的档期数>档期设置总数
                data['_plan_count'] = 0
            else:
                data['_plan_count'] = data['Ftotal_per_day'] - data['plan_count']
            lstdata.append(data)
        self.echo('ops/schedule_plan/schedule_plan.html',{'page_data':lstdata,'current_month':current_month})

class SchedulePlanCompanyHandler(AdminBaseHandler):
    def get(self):
        query = self.db.query(Company).filter(Company.Fdeleted == 0)
        page_data = self.get_page_data(query)
        self.echo('ops/schedule_plan/schedule_plan_company.html',{'page_data':page_data,'page_html':page_data.render_page_html()})

    def get_user_by_id(self,user_id):
        return self.db.query(Users).filter(Users.Fdeleted == 0,Users.Fid == user_id).scalar()




