#encoding: utf-8
__author__ = 'hongjiongteng'

from weddingdress_handler import WeddingDressSeriesListHandler, WeddingDressSeriesAddHandler,\
                                 WeddingDressSeriesEditHandler, WeddingDressSeriesDeleteHandler,\
                                 WeddingDressSeriesDeleteImgHandler,\
                                 WeddingDressWorkListHandler, WeddingDressWorkAddHandler,\
                                 WeddingDressWorkEditHandler, WeddingDressWorkDeleteHandler,\
                                 WeddingDressWorkDeleteImgHandler

handlers = [
    (r'/merchant/weddingdress/series/list/', WeddingDressSeriesListHandler),
    (r'/merchant/weddingdress/series/add/', WeddingDressSeriesAddHandler),
    (r'/merchant/weddingdress/series/edit/(\d+)', WeddingDressSeriesEditHandler),
    (r'/merchant/weddingdress/series/delete/(\d+)', WeddingDressSeriesDeleteHandler),
    (r'/merchant/weddingdress/series/delete/img/(\d+)', WeddingDressSeriesDeleteImgHandler),

    (r'/merchant/weddingdress/work/list/', WeddingDressWorkListHandler),
    (r'/merchant/weddingdress/work/add/', WeddingDressWorkAddHandler),
    (r'/merchant/weddingdress/work/edit/(\d+)', WeddingDressWorkEditHandler),
    (r'/merchant/weddingdress/work/delete/(\d+)', WeddingDressWorkDeleteHandler),
    (r'/merchant/weddingdress/work/delete/img/(\d+)', WeddingDressWorkDeleteImgHandler),
]