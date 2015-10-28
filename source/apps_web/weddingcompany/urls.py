#encoding: utf-8
__author__='hongjiongteng'

from weddingcompany_handler import WeddingCompanySeriesHandler, WeddingCompanySeriesDetailHandler,\
                                   WeddingCompanyMerchantHandler, WeddingCompanyMerchantDetailHandler,\
                                   WeddingCompanyMerchantAllSeriesHandler,\
                                   WeddingCompanyWorkHandler, WeddingCompanyWorkDetailHandler,\
                                   WeddingCompanyMerchantAllWorkHandler

handlers = [
    (r'/weddingcompany/series/', WeddingCompanySeriesHandler),
    (r'/weddingcompany/series/(\d+)', WeddingCompanySeriesDetailHandler),

    (r'/weddingcompany/merchant/', WeddingCompanyMerchantHandler),
    (r'/weddingcompany/merchant/(\d+)', WeddingCompanyMerchantDetailHandler),
    (r'/weddingcompany/merchant/all/series/(\d+)', WeddingCompanyMerchantAllSeriesHandler),
    
    (r'/weddingcompany/work/', WeddingCompanyWorkHandler),
    (r'/weddingcompany/work/(\d+)', WeddingCompanyWorkDetailHandler),
    (r'/weddingcompany/work/all/work/(\d+)', WeddingCompanyMerchantAllWorkHandler)
]