#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from services.series.series_services import SeriesServices
import ujson
import sys

series_services = SeriesServices()

class SeriesListHandler(AdminBaseHandler):

    def get(self,code=0):
        series_services.set_db(self.db)
        self.get_paras_dict()
        self.qdict['code'] = code
        try:
            query = series_services.query_series(**self.qdict)
            page_data = self.get_page_data(query)
            self.echo('ops/series/series_list.html',
                      {
                        'page_data':page_data,
                        'page_html':page_data.render_page_html(),
                        'code':code
                      })
        except Exception,e:
            print e.message
            self.echo('ops/500.html')

class DeleteSeriesHandler(AdminBaseHandler):
    def get(self,series_id):
        rsg = {
            'stat':'error',
            'msg':''
        }
        try:
            series_services.set_db(self.db)
            data = {}
            data['Fdeleted'] = 1
            series_services.update_series(series_id,**data)
        except Exception,e:
            rsg['msg'] = e.message
            raise
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))

class SeriesActivityHandler(AdminBaseHandler):

    def post(self,series_id,code):

        rsp = {'stat':'error','info':''}

        data = {}
        data['Fis_activity'] = code

        try:
            series_services.set_db(self.db)
            series_services.update_series(series_id,**data)
        except Exception,e:
            print e.message

            rsp['info'] = '添加活动失败'
            self.write(ujson.dumps(rsp))

        rsp['stat'] = 'ok'
        self.write(ujson.dumps(rsp))






