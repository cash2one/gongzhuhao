#encoding:utf-8
__author__ = 'morichounami'

from apps_admin.companys.companys_handler import *


handlers = [
    (r'/gzh/ops/companys/list/([\w\W]*)',CompanyHandlerList),
    (r'/gzh/ops/companys/edit/([\w\W]*)',CompanyEditHandler),
    (r'/gzh/ops/companys/delete/([\w\W]*)',CompanyDeleteHandler),
    (r'/gzh/ops/companys/accountable/create/([\w\W]*)',CreateCompanyAccountHandler),
    (r'/gzh/ops/company/activity/([\w\W]*)/([\w\W]*)',CompanyActivityHandler),
]


#/gzh/ops/company/activity/5/1