#encoding:utf-8
__author__ = 'frank'

from apps_admin.series.series_handler import SeriesListHandler,DeleteSeriesHandler,SeriesActivityHandler

handlers = [
    (r'/gzh/ops/series/([\d]*)',SeriesListHandler),
    (r'/gzh/ops/delete/series/([\w\W]*)',DeleteSeriesHandler),
    (r'/gzh/ops/series/activity/([\d]*)/([\d]*)',SeriesActivityHandler),
]
