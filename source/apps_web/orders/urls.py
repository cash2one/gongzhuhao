#!/usr/bin/env python2.7
# encoding:utf-8

from order_handler import *

handlers = [
    (r'/order/create/(\d+)/(\d+)/(\d+)', OrderHandler), #产品详情product_id
]