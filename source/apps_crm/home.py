#encoding:utf-8
__author__ = 'binpo'


from common.base import BaseHandler
#from datacache.datacache import PageDataCache
#import ujson
#from services.common.common_service import CommonService
import tornado
import json
class TestIEJson(BaseHandler):
    def get(self):
        self.write(json.dumps({'name':'name','age':'age'}))

class HomeHandler(BaseHandler):

    def get(self,p=None):
        if self.get_current_user():
            user = self.get_current_user()#.get('Frole_codes')
            if user.get('is_employee'):
                return self.redirect('/admin/index')
            if 'merchant' in user.get('Frole_codes'):
                return self.redirect('/merchant/index/')
            else:
                return self.redirect('/merchant/index/')
        else:
            self.echo('crm/login/login.html',{'msg':''})



class MerchantIndexHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.echo('crm/merchant/merchant_index.html')



class HealthCheck(BaseHandler):

    def get(self):
        self.echo('success')

    def head(self):
        self.get()
