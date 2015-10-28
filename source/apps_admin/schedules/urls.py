__author__ = 'frank'

from apps_admin.schedules.schedules_handler import *
from apps_admin.schedules.schedule_handler import QuerySchedulePlanHandler,SchedulePlanCompanyHandler

handlers = [
    (r'/gzh/ops/schedule/attention/template/([\w\W]*)',ScheduleAttentionHandler),
    (r'/gzh/ops/create/schedule/([\w\W]*)',CreateSchedulesHandler),
    (r'/gzh/ops/schedule_plan/list/([\w\W]*)',QuerySchedulePlanHandler),
    (r'/gzh/ops/schedule_plan/company/list/',SchedulePlanCompanyHandler),
]