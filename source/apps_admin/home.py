#encoding:utf-8
'''
Created on 2014-5-28

@author: qiuyan.zwp
'''
from common.base import AdminBaseHandler
from tenjin_base import TenjinBase
import tornado.web

class AdminHandler(AdminBaseHandler):
    def get(self,html_name=None):

        render_html = 'ops/index.html'
        if html_name:
            render_html = 'ops/'+html_name
        self.echo(render_html, layout='ops/base.html')

    def post(self):
        pass

class ModelsHandler(TenjinBase):
    def get(self):
        rsp = [[1001, 'Lorem', 'ipsum', 'dolor', 'sit'], [1002 , 'amet', 'consectetur', 'adipiscing', 'elit']]
        render_html = 'ops/models.html'
        self.echo(render_html, context={
            'rsps': rsp,
            'title': 'yijiaren',
        }, layout='ops/base.html')

    @tornado.web.authenticated
    def post(self):
        pass

