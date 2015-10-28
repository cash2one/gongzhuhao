
from series_handler import *

handlers = [
    (r'/merchant/series/', SeriesList),
    (r'/merchant/series/add/', SeriesAdd),
    (r'/merchant/series/add/(\d*)/', SeriesAdd),
    (r'/merchant/series/edit/(\d*)/', SeriesAdd),
    (r'/merchant/series/delete/(\d*)/', SeriesDelete),
    (r'/merchant/series/delete/img/(\d*)',SerieImageDelete)
]

