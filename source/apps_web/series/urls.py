#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from series_handler import *

handlers = [
    (r'/series/(\d+)', SeriesDetailhandler), #产品详情product_id
]