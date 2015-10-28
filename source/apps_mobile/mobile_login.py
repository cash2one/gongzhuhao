#encoding:utf-8
__author__ = 'binpo'
import urlparse
from mobile_base import MobileBaseHandler
from services.users.user_services import UserServices
from tornado.web import create_signed_value
import ujson
import urllib

from utils.common_util import is_mobile
from setting import WX_GZH_AppID,WX_GZH_AppSecret
from common.mweixin_oauth.wx_mobile_info import get_wx_login_redirect_url_with_none_access,get_wx_login_redirect_url
user_service = UserServices()

class MobileLoginHandler(MobileBaseHandler):

    def get(self,*ars,**kargs):

        back_url = urlparse.urljoin(self.request.full_url(), self.get_argument('next', '/mobile/user/index/'))

        self.set_cookie('login_regrdiect_url',back_url,expires_days=1)
        if self.get_secure_cookie('loginuser'):
            self.redirect(back_url)
        else:
            try:
                self.get_paras_dict()
                user_agent = self.request.headers.get('User-Agent')
                user_agent = user_agent.lower()

                if is_mobile(user_agent)!=3:#从微信来的，直接跳转到手机微信页面
                    return self.echo('login.html',{'next':back_url,'action':None})
                if not self.qdict.has_key('code'):
                    raise
                else:
                    code = self.qdict.get('code')
                    redirect_url = self.get_cookie('login_regrdiect_url')
                    code = code.strip()
                    content = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(WX_GZH_AppID,WX_GZH_AppSecret,code)).read()
                    token_info = ujson.loads(content)
                    openid = token_info.get('openid')

                    access_token = token_info.get('access_token')
                    user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'%(access_token,openid)).read()
                    user = ujson.loads(user_info)
                    nick=user.get('nickname')
                    photo=user.get('headimgurl')

                    self.set_secure_cookie('wx_login_open_id',openid,expires_days=1)
                    self.set_secure_cookie('nick',nick,expires_days=1)
                    self.set_secure_cookie('photo',photo,expires_days=1)

                    user_service.set_db(self.db)
                    user = user_service.get_user_by_weixin_id(openid)
                    if user:
                        cookies = user_service.user_format(user)
                        data = self.child_account_key(user)
                        if nick and (not user.Fnick_name or user.Fnick_name.startswith('公主号')):
                            user.Fnick_name = nick
                        if photo and (user.Fphoto_url=='/static/common/images.png' or not user.Fphoto_url):
                            user.Fphoto_url = photo
                        if data:
                            cookies.update(data)
                        self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=10)
                        self.db.add(user)
                        self.db.commit()
                        if redirect_url:
                            return self.redirect(redirect_url)
                        else:
                            return self.redirect('/mobile/user/index/')
                    if redirect_url:
                        return self.echo('login.html',{'next':redirect_url,'action':None,'info':''})
                    else:
                        return self.echo('login.html',{'next':back_url,'action':None,'info':''})
            except Exception,e:
                params = urllib.urlencode(self.qdict)
                _url='http://m.gongzhuhao.com/mobile/user/login?'+params
                direct_url = get_wx_login_redirect_url(_url)
                return self.redirect(direct_url)

    def child_account_key(self,user):
        if 'merchant' in user.Frole_codes:
            company = user_service.get_company_merchant_id(user.Fid)
            if company:
                return {'Fcompany_id':company.Fid,'Fmerchant_id':user.Fid,'Fcompany_name':company.Fcompany_name}
            else:
                return {'Fcompany_id':'','Fmerchant_id':'','Fcompany_name':''}

        if user.Fpermission:
            user_id = user.Fid
            data = user_service.get_merchant_id_by_child_acount(user_id)
            return data

    def post(self):
        user_service.set_db(self.db)
        self.get_paras_dict()
        mobile = self.qdict.get('mobile','')
        passwd = self.qdict.get('password','')
        user = user_service.login_with_phone(mobile,passwd)
        if not user:
            user = user_service.login_with_username(mobile,passwd)

        if self.get_argument('next',''):
            back_url = self.get_argument('next')
        elif self.get_cookie('login_regrdiect_url'):
            back_url = self.get_cookie('login_regrdiect_url')
        else:
            back_url = self.get_argument('next', '/')
        next = back_url
        try:
            if user:
                open_id = self.get_secure_cookie('wx_login_open_id')
                nick = self.get_secure_cookie('nick')
                photo = self.get_secure_cookie('photo')

                exist_user = user_service.get_user_by_weixin_id(open_id)
                if exist_user and exist_user.Fid!=user.Fid:
                    exist_user.Fweixin=''
                    self.db.add(exist_user)
                if open_id:
                    user.Fweixin=open_id
                if nick and (not user.Fnick_name or user.Fnick_name.startswith('公主号')):
                    user.Fnick_name = nick
                if photo and (user.Fphoto_url=='/static/common/images.png' or not user.Fphoto_url):
                    user.Fphoto_url=photo
                cookies = user_service.user_format(user)
                self.db.add(user)
                self.db.commit()
                if self.child_account_key(user):
                    cookies.update(self.child_account_key(user))
                self.set_secure_cookie('loginuser', ujson.dumps(cookies), expires_days=200)
                self.redirect(back_url)
            else:
                self.echo('login.html',{'next':next,'info':u'用户名或密码错误','action':None,'info':''})
        except Exception,e:
            self.echo('login.html',{'next':next,'info':e.message,'action':None})


class LoginOutHandler(MobileBaseHandler):

    def get(self,**kargs):
        self.clear_cookie("loginuser")
        self.clear_cookie('login_regrdiect_url')
        if self.request.uri.startswith('/api/json'):
            self.write_json({'stat':'ok','info':'','data':{}})
        else:
            self.echo('login.html',{'action':'/mobile/user/login','info':''})

class IndexHandler(MobileBaseHandler):

    def get(self,args,**kargs):
        self.echo('login.html',{'action':None,'info':''})

class APPLoginHandler(MobileBaseHandler):

    def post(self, *args, **kwargs):
        rsp = {
            'stat': 'err',
            'info': '',
        }
        self.get_paras_dict()
        username = self.qdict.get('username','')           # 用户名
        passwd = self.qdict.get('passwd','')                # 密码
        if not username or not passwd:
            rsp['info'] = '账号和密码不能为空'
            return self.write(ujson.dumps(rsp))
        user_service = UserServices(self.db)
        status,user = user_service.check_user_login_pwd(username,passwd)

        if status:
            cookies = user_service.user_format_app(user)
            login_token = create_signed_value(self.application.settings["cookie_secret"], 'loginuser', ujson.dumps(cookies))
            rsp['stat'] = 'ok'
            rsp['data'] = {'login_token':login_token,'nick_name':user.Fnick_name,'photo_url':user.Fphoto_url}
            return self.write(ujson.dumps(rsp))
        else:
            rsp['info'] = user
            return self.write(ujson.dumps(rsp))


