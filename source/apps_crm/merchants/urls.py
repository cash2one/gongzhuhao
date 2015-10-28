# encoding:utf-8
from merchants_hander import CHandlerMerchantsEdit, CHandlerMerchantsListRole,\
    CHandlerMerchantsEditRole, CHandlerMerchantsAddRole, \
    CHandlerMerchantsDeleteRole, \
    CHandlerMerchantsEditProvince, CHandlerMerchantsEditCity, \
    CHandlerShareExtendInfo, CHandlerSharePrizeInfo,MerchantGiftHandler
from merchant_shares_handler import MerchantOrdersShareHandler

from potential_customer_handler import PotentialCustomerQuery,PotentialCustomerVisitorQuery,PotentialCustomerVisitorCreate
from orders_from_handler import *

handlers = [
    (r'/merchant/edit/', CHandlerMerchantsEdit),
    (r'/merchant/edit/province/([\w\W]*)/', CHandlerMerchantsEditProvince),
    (r'/merchant/edit/city/([\d]{1,8})/', CHandlerMerchantsEditCity),
    (r'/merchant/edit/listrole/', CHandlerMerchantsListRole),
    (r'/merchant/edit/addrole/', CHandlerMerchantsAddRole),
    (r'/merchant/edit/editrole/([\d]{1,8})/', CHandlerMerchantsEditRole),
    (r'/merchant/edit/deleterole/([\d]{1,8})/', CHandlerMerchantsDeleteRole),

    (r'/merchant/potential_customer/list/', PotentialCustomerQuery),
    (r'/merchant/potential_customer/visits/([\d]{1,8})/', PotentialCustomerVisitorQuery),

    (r'/merchant/create/visits/', PotentialCustomerVisitorCreate),
    (r'/merchant/shares/', MerchantOrdersShareHandler),

    (r'/merchant/system/edit/shareextendinfo/', CHandlerShareExtendInfo),
    (r'/merchant/system/edit/shareprizeinfo/', CHandlerSharePrizeInfo),

    (r'/merchant/system/order_from/list/', OrdersFromInfoQueryHandler),
    (r'/merchant/system/order_from/create/', OrdersFromInfoCreateHandler),
    (r'/merchant/system/order_from/delete/([\d]{1,8})', OrdersFromInfoDeleteHandler),

    (r'/merchant/system/gift/([\d]*)',MerchantGiftHandler),


]
