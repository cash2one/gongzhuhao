#encoding:utf-8
__author__ = 'binpo'
import urlparse
from common.base import BaseHandler
from services.users.user_services import UserServices
import ujson

user_service = UserServices()


class MobileLoginHandler(BaseHandler):

    def get(self,*ars,**kargs):
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/mobile/user/index/'))
        if self.get_secure_cookie('loginuser'):
            self.redirect(back_url)
        else:
            self.echo('mobile/login/login.html',{'next':back_url})

    def child_account_key(self,user):
        if 'merchant' in user.Frole_codes:
            company = user_service.get_company_merchant_id(user.Fid)
            return {'Fcompany_id':company.Fid,'Fmerchant_id':user.Fid,'Fcompany_name':company.Fcompany_name}
        if user.Fpermission:
            user_id = user.Fid
            data = user_service.get_merchant_id_by_child_acount(user_id)
            return data
        return {}

    def post(self):
        user_service.set_db(self.db)
        mobile = self.get_argument('mobile',None)            #用户名
        passwd = self.get_argument('password',None)                #密码
        user = user_service.login_with_phone(mobile,passwd)
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/mobile/user/index/'))
        try:
            if user:
                cookies = user_service.user_format(user)
                cookies.update(self.child_account_key(user))
                self.set_secure_cookie('loginuser', ujson.dumps(cookies), expires_days=2)
                self.redirect(back_url)
            else:
                self.echo('mobile/login/login.html',{'next':next,'info':u'用户名或密码错误'})
        except Exception:
            if self.settings.get('debug'):
                raise
            self.echo('apps_crm/404.html')


class LoginOutHandler(BaseHandler):

    def get(self,**kargs):
        self.clear_cookie("loginuser")
        self.redirect('/mobile/user/login')
        #self.echo('mobile/login/login.html')

class IndexHandler(BaseHandler):

    def get(self,args,**kargs):
        self.echo('mobile/login/login.html')
