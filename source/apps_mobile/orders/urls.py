#!/usr/bin/env python
# encoding: utf-8

from orders_handler import CHandlerOrdersList, CHandlerOrdersAdd, \
    CHandlerOrdersUpdate, OrderConfirmHandler,OrderScheduleQueryHandler

_handlers = [
    #(r'/mobile/merchant/orders/', CHandlerOrdersList),
    (r'/mobile/merchant/service/', CHandlerOrdersList),
    (r'/mobile/merchant/orders/add/([\w\W]*)/([\w\W]*)', CHandlerOrdersAdd),
    #(r'/mobile/merchant/orders/update/([\d]{1,28})/', CHandlerOrdersUpdate),
    #(r'/mobile/merchant/orders/confirm/([\d]{1,28})', OrderConfirmHandler),
    (r'/mobile/order/query_schedule/', OrderScheduleQueryHandler),

]
