#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import BaseApiHandler as BaseHandler
from services.activities.activities_service import ActivitiesService
import sys

activities_service = ActivitiesService()

class ActivityHandler(BaseHandler):

    def get(self, *args, **kwargs):

        activities_service.set_db(self.db)
        try:
            activities = activities_service.query_activities(order_by='Fsort')
            self.echo('view/activities/qx.html',{'activities': activities})
        except Exception,e:
            pass




