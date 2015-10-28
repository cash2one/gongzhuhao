#encoding:utf-8
__author__ = 'frank'

from apps_admin.orders.orders_handler import *
from apps_admin.orders.bespeak_handler import BespeakOrdrHandler

handlers=[
    (r'/gzh/ops/orders/list',OrderHandlerList),
    (r'/gzh/ops/bespeak/orders/list',BespeakOrdrHandler)
]
