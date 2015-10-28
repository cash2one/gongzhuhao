#encoding:utf-8
__author__ = 'morichounami'
from services.users.user_services import UserServices
import tornado.web
import datetime
import urlparse
import ujson
from common.base import *
user_service = UserServices()

class LoginHandler(BaseHandler):

    def get(self,**kargs):
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/merchant/orders/'))
        rsp = {
            'stat': 'err',
            'msg': ''
        }
        if self.get_secure_cookie('loginuser'):
            self.redirect(back_url)
        self.echo('crm/login/login.html',{'msg':rsp['msg']},layout='')

    def post(self):
        username = self.get_argument('username',None)
        passwd = self.get_argument('password',None)
        rsg = {
            'stat': 'err',
            'msg': '',
        }
        if not username or not passwd:
            rsg['msg'] = '用户名或密码不能为空!'
            return self.echo('crm/login/login.html',{'msg':rsg['msg']})
        user_service.set_db(self.db)
        is_login,user = user_service.check_user_login_pwd(username,passwd)
        back_url = urlparse.urljoin(self.request.full_url(),self.get_argument('next','/merchant/index/'))
        if is_login:
            cookies = user_service.user_format(user)
            data = self.child_account_key(user)
            if data:
                cookies.update(data)
            self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=1)
            rsg['stat'] = 'ok'
            self.redirect(back_url)
        else:
            rsg['msg'] = '用户名或密码错误!'
            self.echo('crm/login/login.html',{'msg':rsg['msg']},layout='')

    def child_account_key(self,user):
        if 'merchant' in user.Frole_codes:
            company = user_service.get_company_merchant_id(user.Fid)
            if company:
                return {'Fcompany_id':company.Fid,'Fmerchant_id':user.Fid,'Fcompany_name':company.Fcompany_name}
            else:return {'Fcompany_id':'','Fmerchant_id':user.Fid,'Fcompany_name':''}

        if user.Fpermission:
            user_id = user.Fid
            data = user_service.get_merchant_id_by_child_acount(user_id)

            if data['Fmerchant_id']:
                data['company_role'] = user_service.get_role(data['Fmerchant_id'])

            return data

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("loginuser")
        next = self.get_argument('next','/')
        if 'admin' in next:
            self.render('admin/login.html',next=next)
        self.redirect("/login")
