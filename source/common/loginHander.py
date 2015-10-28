# -*- coding: utf-8 -*-
'''
Created on 2013-12-30

@author: qiuyan.zwp
'''
import sso
from common.base import BaseHandler
from tornado import gen
import tornado.web
import urlparse
from services.users.user_services import *
import ujson
from tornado.options import options
import datetime
login_allow_count = 4

user_service = UserServices()

class AdminLoginHandler(tornado.web.RequestHandler):

    @property
    def db(self):
        return self.application.db

    def get(self,**kargs):
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/admin/index'))

        if self.get_secure_cookie('loginuser'):
            self.redirect(back_url)
        self.render('ops/login.html')

    def post(self):
        username = self.get_argument('username',None)            #用户名
        passwd = self.get_argument('passwd',None)                #密码
        user_service.set_db(self.db)
        user = user_service.check_user_passwd(username,passwd)
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/admin/index'))
        try:
            if user:
                cookies = user_service.user_format(user)
                data = self.child_account_key(user)
                if data:
                    cookies.update(data)
                self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=1)
                self.redirect(back_url)
            else:
                self.render('ops/login.html',next=next,info=u'用户名或密码错误')
        except Exception,e:
            print e

    def child_account_key(self,user):
        user_service.set_db(self.db)
        if 'merchant' in user.Frole_codes:
            company = user_service.get_company_merchant_id(user.Fid)
            if company:
                return {'Fcompany_id':company.Fid,'Fmerchant_id':user.Fid,'Fcompany_name':company.Fcompany_name}
            else:return {'Fcompany_id':'','Fmerchant_id':user.Fid,'Fcompany_name':''}
        if user.Fpermission:
            user_id = user.Fid
            data = user_service.get_merchant_id_by_child_acount(user_id)
            return data

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_cookie("loginuser")
        next = self.get_argument('next','/')
        if 'admin' in next:
            self.render('admin/login.html',next=next)
        self.redirect("/gzh/ops/login")

class AuthHandler(BaseHandler,sso.AuthHandler):
   
    LOGIN_URL = '/login'
#    def authenticate_redirect(self, app_name, next, callback=None):
#        self.redirect(self.LOGIN_URL + '?' + urllib.urlencode(args))
        
    @tornado.web.asynchronous
    @gen.coroutine
    def get(self):
        if self.get_secure_cookie('loginuser'):
            self.redirect(next)
        else:
            back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/'))
            self.redirect(self.LOGIN_URL + '?next='+back_url)
            #self.authenticate_redirect(app_name=self.APP_NAME,next=back_url)  
    
    def post(self):
        pass
    

