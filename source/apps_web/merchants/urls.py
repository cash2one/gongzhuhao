#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_web.merchants.merchants_handler import *
from apps_web.merchants.products_handler import *
from apps_web.merchants.package_handler import *

_handlers = [

    (r'/api/products/',ProductsHandler),
    (r'/api/product/([\d]*)',ProductHandler),

    (r'/api/package/([\d]*)',PackageHandler),
    (r'/api/packages/',PackagesHandler),

    (r'/api/merchant/list/',MerchantListHandler),

    (r'/merchant/detail/([\d]*)',MerchantDetail),

    (r'/merchant/products/([\d]*)/([\w\W]*)/([\d]*)',MerchantProductsHandler),
    (r'/merchant/series/([\d]*)/([\d]*)',MerchantSeriesHandler),
]