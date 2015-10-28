#encoding: utf-8
__author__='hongjiongteng'

from weddingdress_handler import WeddingDressSeriesHandler, WeddingDressSeriesDetailHandler,\
                                 WeddingDressMerchantHandler, WeddingDressMerchantDetailHandler,\
                                 WeddingDressMerchantAllSeriesHandler,\
                                 WeddingDressWorkHandler, WeddingDressWorkHandler,\
                                 WeddingDressWorkDetailHandler, WeddingDressMerchantAllWorkHandler


handlers = [
    (r'/weddingdress/series/', WeddingDressSeriesHandler),
    (r'/weddingdress/series/(\d+)', WeddingDressSeriesDetailHandler),

    (r'/weddingdress/merchant/', WeddingDressMerchantHandler),
    (r'/weddingdress/merchant/(\d+)', WeddingDressMerchantDetailHandler),
    (r'/weddingdress/merchant/all/series/(\d+)', WeddingDressMerchantAllSeriesHandler),

    (r'/weddingdress/work/', WeddingDressWorkHandler),
    (r'/weddingdress/work/(\d+)', WeddingDressWorkDetailHandler),
    (r'/weddingdress/work/all/work/(\d+)', WeddingDressMerchantAllWorkHandler)
]