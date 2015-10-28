#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.activities.activities_handler import *

_handlers = [
    (r'/gzh/ops/create/activities',CreateActivityHandler),
    (r'/gzh/ops/query/activities',ActivityListHandler),
]