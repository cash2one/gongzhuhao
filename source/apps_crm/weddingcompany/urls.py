#encoding: utf-8
__author__ = 'hongjiongteng'

from weddingcompany_handler import WeddingCompanySeriesAddHandler, WeddingCompanySeriesListHandler,\
                                   WeddingCompanySeriesEditHandler, WeddingCompanySeriesDeleteHandler,\
                                   WeddingCompanySeriesDeleteImgHandler,\
                                   WeddingCompanyWorkListHandler, WeddingCompanyWorkAddHandler,\
                                   WeddingCompanyWorkEditHandler, WeddingCompanyWorkDeleteHandler,\
                                   WeddingCompanyWorkDeleteImgHandler

handlers = [
    (r'/merchant/weddingcompany/series/list/', WeddingCompanySeriesListHandler),
    (r'/merchant/weddingcompany/series/add/', WeddingCompanySeriesAddHandler),
    (r'/merchant/weddingcompany/series/edit/(\d+)', WeddingCompanySeriesEditHandler),
    (r'/merchant/weddingcompany/series/delete/(\d+)', WeddingCompanySeriesDeleteHandler),
    (r'/merchant/weddingcompany/series/delete/img/(\d+)', WeddingCompanySeriesDeleteImgHandler),
    
    (r'/merchant/weddingcompany/work/list/', WeddingCompanyWorkListHandler),
    (r'/merchant/weddingcompany/work/add/', WeddingCompanyWorkAddHandler),
    (r'/merchant/weddingcompany/work/edit/(\d+)', WeddingCompanyWorkEditHandler),
    (r'/merchant/weddingcompany/work/delete/(\d+)', WeddingCompanyWorkDeleteHandler),
    (r'/merchant/weddingcompany/work/delete/img/(\d+)', WeddingCompanyWorkDeleteImgHandler),
]