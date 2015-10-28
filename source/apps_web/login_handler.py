#encoding:utf-8
__author__ = 'binpo'
import urlparse
from common.base import BaseApiHandler
from services.users.user_services import UserServices
import ujson
from common.base import SiteError
import sys
from utils.random_utils import create_random_passwd
import datetime
from tenjin.helpers import *
user_service = UserServices()


class CheckLoginHandler(BaseApiHandler):

    def get(self, *args, **kwargs):
        user = self.get_current_user()
        if user:
            data = {'code':200,'data':{'login':True,'user':user},'info':"登录成功"}
        else:
            data = {'code':1001,'data':{},'info':'系统未登录,请登录'}
        self.write_json(data)


class RegApiHandler(BaseApiHandler):

    def post(self, *args, **kwargs):
        self.get_paras_dict()
        phone = self.qdict.get('phone')
        code = self.qdict.get('code')
        password = self.qdict.get('password')
        user_service.set_db(self.db)
        try:
            for key in ['phone','code']:
                if not self.qdict.get(key):
                    raise SiteError('参数错误')

            cache_code = self.mcache.get(str(self.qdict.get('phone'))+'_code')
            if str(cache_code)==code.strip():
                user = user_service.create_user_by_phone(phone,password=password)
                cookies = user_service.user_format(user)
                open_id = self.get_secure_cookie('wx_login_open_id')
                nick = self.get_secure_cookie('nick')
                photo = self.get_secure_cookie('photo')
                data = self.child_account_key(user)
                if open_id:
                    user.Fweixin=open_id
                if nick and not user.Fnick_name:
                    user.Fnick_name = nick
                if photo and (user.Fphoto_url=='/static/common/images.png' or not user.Fphoto_url):
                    user.Fphoto_url = photo
                if data:
                    cookies.update(data)
                self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=10)
                self.db.add(user)
                self.db.commit()

                context = { 'title': 'Bordered Table Example','items': [ '<AAA>', 'B&B', '"CCC"' ] }
                html_str = self.engine.render('web/login/table.pyhtml', context)
                # url = self.get_cookie('login_regrdiect_url')
                data={'code':200,'info':'验证通过并登陆','data':{'html':html_str}}

            else:
                data={'stat':2028,'data':{},'info':'验证码错误'}
        except Exception,e:
            pass
            data={'stat':'1005','info':'程序异常,异常原因是'+e.message,'data':{}}
        self.write_json(data)


class LoginApiHandler(BaseApiHandler):

    def post(self):
        user_service.set_db(self.db)
        self.get_paras_dict()
        mobile = self.qdict.get('phone','')
        passwd = self.qdict.get('password','')
        code = self.qdict.get('code','')

        if not mobile.strip():
            data={'code':2030,'data':{},'info':"登录用户名或手机号不能为空"}
        elif not (passwd.strip() or code):
            data={'code':2030,'data':{},'info':"密码或验证码错误"}
        else:
            if code:
                cache_code = self.mcache.get(str(mobile)+'_login')
                if not cache_code:
                    cache_code = self.mcache.get(str(mobile)+'_reg')
                if not cache_code:
                    cache_code = self.mcache.get(str(mobile)+'_code')

                if str(cache_code)==code.strip():
                    user = user_service.create_user_by_phone(mobile)
                    cookies = user_service.user_format(user)
                    if self.child_account_key(user):
                        cookies.update(self.child_account_key(user))
                    self.set_secure_cookie('loginuser', ujson.dumps(cookies), expires_days=10)
                    data = {'code':200,'data':{'user':cookies},'info':"用户登录成功"} 
                else:
                    data = {'code':2029,'data':{},'info':"验证码错误"}
            else:
                user = user_service.login_with_phone(mobile,passwd)
                if not user:
                    user = user_service.login_with_username(mobile,passwd)
                try:
                    if user:
                        cookies = user_service.user_format(user)
                        if self.child_account_key(user):
                            cookies.update(self.child_account_key(user))
                        self.set_secure_cookie('loginuser', ujson.dumps(cookies),expires_days=10)

                        data = {'code':200,'data':{'user':cookies},'info':"用户登录成功"}
                    else:
                        data = {'code':2004,'info':"用户登录失败，用户名或密码错"}
                except Exception,e:
                    data = {'code':500,'info':"程序异常:"+e.message}
        self.write_json(data)

class LoginOutApiHandler(BaseApiHandler):

    def get(self,**kargs):
        self.clear_cookie("loginuser")
        self.clear_cookie('login_regrdiect_url')
        #self.write_json({'code':200,'data':{},'info':'注销成功'})
        self.redirect('/topic')

class DemoTestHandler(BaseApiHandler):

    def get(self,*args,**kargs):

        # render template with context data
        # print html
        # print type(html)
        context={'items':[1,2,3,4,56],'title':'helloworld'}
        html = self.engine.get_template('web/login/table.pyhtml', context)
        content = html.render(context)
        #print content
        self.write_json({'code':200,'data':content,'info':'注销成功'})

        # _buf=[]
        # html_content = ''.join(html.render(context, _buf=_buf))
        # # print(''.join(_buf))
        # print dir(self.engine)
        # html = escape(html_str)
        # #html = self.engine.escape_html(html_str)
        # print html
        #data['data']['html'] = html_str
        #self.echo('login.html',{'action':None,'info':''})


class LoginHandler(BaseApiHandler):


    def get(self,**kargs):
        data={}
        next = self.get_argument('next', '/')
        if 'admin' in next:
            return self.redirect('/login?next='+next)
        if self.current_user and self.current_user.get('Fid'):

            return self.redirect(urlparse.urljoin(self.request.full_url(), '/'))

        count = self.mcache.get(self.get_client_ip+'_login_count')

        self.echo('view/login/login.html', {
            'next': next,
            'data':data,
            'img_check': True if count > 3 else False
        },layout='')

    def post(self):
        #login_count = self.mcache.get(self.get_client_ip+'_login_count')
        next = self.get_argument('next', '/topic')
        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/topic'))
        data={}
        username = self.get_argument('username','')           # 用户名
        passwd = self.get_argument('passwd','')                # 密码
        if not username or not passwd:
            data['error'] = '账号和密码不能为空'
            self.echo('view/login/login.html', {
                'next': next,
                'data':data
            },layout='')
        else:
            user_service = UserServices(self.db)
            status, user = user_service.check_user_login_pwd(username,passwd)
            if status:
                user.Flast_visit = datetime.datetime.now()
                user.Flast_visit_ip = self.get_client_ip
                user.Fvisit_times = user.Fvisit_times+1
                cookies = user_service.user_format(user)
                self.set_secure_cookie('loginuser', ujson.dumps(cookies),expires_days=100 if int(self.get_argument('login_forever', 0)) else 0.1, httponly=True )
                self.db.add(user)
                self.db.commit()
                self.redirect(back_url)
            else:
                data['error'] = '账号或密码错误'
                self.echo('view/login/login.html', {
                        'next': next,
                        'data':data
                },layout='')


class RegisterHandler(BaseApiHandler):


    def get(self, *args, **kwargs):
        next = self.get_argument('next', '/')
        self.echo('view/login/reg.html',{'next':next,'info':''},layout='')

    def post(self, *args, **kwargs):

        self.get_paras_dict()
        phone = self.qdict.get('phone')
        code = self.qdict.get('code')
        password = self.qdict.get('password')
        next = self.get_argument('next', '/')
        user_service.set_db(self.db)
        try:
            for key in ['phone','code']:
                if not self.qdict.get(key):
                    raise SiteError('参数错误')
            cache_code = self.mcache.get(str(self.qdict.get('phone'))+'_code')
            if str(cache_code)==code.strip():
                user = user_service.create_user_by_phone(phone,password=password)
                cookies = user_service.user_format(user)
                open_id = self.get_secure_cookie('wx_login_open_id')
                nick = self.get_secure_cookie('nick')
                photo = self.get_secure_cookie('photo')
                data = self.child_account_key(user)
                if open_id:
                    user.Fweixin=open_id
                if nick and not user.Fnick_name:
                    user.Fnick_name = nick
                if photo and (user.Fphoto_url=='/static/common/images.png' or not user.Fphoto_url):
                    user.Fphoto_url = photo
                if data:
                    cookies.update(data)
                if not user.Fnick_name:
                    user.Fnick_name='公主号_'+create_random_passwd(3)
                self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=10)
                self.db.add(user)
                self.db.commit()
                # url = self.get_cookie('login_regrdiect_url')
                data={'stat':'1000','info':'验证通过并登陆','data':{}}
            else:
                data={'stat':'1004','info':'验证码错误'}
        except Exception,e:
            pass
            data={'stat':'1005','info':'程序异常,异常原因是'+e.message}
        if data.get('stat')=='1000':
            self.redirect(next)
        else:
            self.echo('view/login/reg.html',{'next':next,'info':data.get('info')},layout='')



class MobileCodeLogin(BaseApiHandler):
    def get(self, *args, **kwargs):
        self.echo('view/login/login_code.html',layout='')