#!/usr/bin/env python2.7
# encoding:utf-8

from product_handler import *

handlers = [
    (r'/product/(\d+)', ProductDetailHandler), #产品详情product_id
]