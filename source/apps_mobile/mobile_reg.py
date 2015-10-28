#encoding:utf-8
__author__ = 'binpo'
from utils.message.sms import send_phone_msg
from utils.random_utils import create_random_passwd
from conf.msg_conf import PHONE_REG_TEMPLATE
from mobile_base import MobileBaseHandler
from common.base import SiteError
from tornado.web import create_signed_value
from tornado.options import options
from utils.regular import Regular
from conf.msg_conf import PHONE_REG_TEMPLATE,PHONE_LOGIN_TEMPLATE,CHECK_CODE_TEMPLATE
import ujson
import time
import sys

from services.users.user_services import UserServices
user_service = UserServices()

class SendRegistCodeHandler(MobileBaseHandler):
    def get(self, *args, **kwargs):
        phone = self.get_argument('phone')
        code = create_random_passwd(2)
        if self.mcache.get(str(phone)+'_reg'):
            self.mcache.set(str(phone)+'_reg',self.mcache.get(str(phone)+'_reg'),180)
            data={'stat':'1000','info':'操作成功'}
        else:
            is_ok = self.mcache.set(str(phone)+'_reg',str(code),180)
            content=PHONE_REG_TEMPLATE%(code)
            if is_ok:
                send_phone_msg(str(phone),content)
                data={'stat':'1000','info':'操作成功'}
            else:
                data={'stat':'1001','info':'操作失败'}
        self.write_json(data)

class RegisterHandler(MobileBaseHandler):

    def post(self, *args, **kwargs):
        phone = self.get_argument('phone',None)
        code = self.get_argument('code',None)
        user_service.set_db(self.db)
        try:
            if not phone or not code:
                raise SiteError('参数错误')
            cache_code = self.mcache.get(str(phone)+'_reg')
            if str(cache_code)==code.strip():
                user = user_service.create_user_by_phone(phone)
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
                url = self.get_cookie('login_regrdiect_url')
                data={'stat':'1000','info':'验证通过','url':url}
            else:
                data={'stat':'1001','info':'验证码错误'}
        except Exception,e:
               data={'stat':'1001','info':e.message}
        self.write_json(data)


class APPRegHandler(MobileBaseHandler):

    def post(self, *args, **kwargs):

        self.get_paras_dict()
        user_service.set_db(self.db)
        rsp = {
            'stat': 'err',
            'info': ''
        }

        try:
            is_ok,info = self.check_params()
            if not is_ok:
                rsp['info'] = info
                return self.write(ujson.dumps(rsp))

            is_ok,info = self.check_phone_code()
            if not is_ok:
                rsp['info'] = info
                return self.write(ujson.dumps(rsp))

            kargs = {
                'phone':self.qdict.get('phone'),
                'nick':self.qdict.get('nick','user_%s' % int(time.time())),
                'is_employee': 0,
                'user_pwd':self.qdict.get('password'),
                'photo':options.DEFAULT_USER_PHOTO
            }
            is_add_ok,info = user_service.create_user(**kargs)
            if not is_add_ok:
                rsp['info'] = info
                return self.write(ujson.dumps(rsp))

            if self.qdict.get('invite_code'): #存在邀请码
                pass

            user_info = user_service.get_user_by_phone(kargs['phone'])
            cookies = user_service.user_format_app(user_info)
            login_token = create_signed_value(self.application.settings["cookie_secret"], 'loginuser', ujson.dumps(cookies))

            rsp['stat'] = 'ok'
            rsp['data'] = {'login_token':login_token,'nick_name':user_info.Fnick_name,'photo_url':user_info.Fphoto_url}
            return self.write(ujson.dumps(rsp))

        except Exception,e:
            pass




    def check_phone_code(self):

        key = str(self.qdict.get('phone')+'_reg')
        code = self.mcache.get(key)
        if code:
            if code == self.qdict.get('phone_check_code', ''):
                return True,''
            else:
                return False,'短信验证码错误'
        else:
            return False,'短信验证码已过期'

    def check_params(self):
        if not self.qdict.get('phone'):
            return False,'电话不能为空'
        elif not Regular.check_phone(self.qdict.get('phone')):
            return False,'电话号码错误'
        if not self.qdict.get('password', '') or len(self.qdict.get('password', '').strip())<6 or len(self.qdict.get('password', '').strip())>12:
            return False,'密码设置应该在6－12位之间'
        return True,''

class MobileCodeHandler(MobileBaseHandler):

    def get(self,**kwargs):
        '''
        :发送手机验证码
        :param phone:
        :param code_type:   _reg:注册(登陆)验证码
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        phone = self.qdict.get('phone')
        code_type = self.qdict.get('code_type')
        if not phone or not code_type:
            data = {'stat':'error','info':'请求参数错误'}
        else:
            if not Regular.check_phone(phone):
                data = {'stat':'error','info':'手机格式错误'}
            else:
                cache_key = str(phone)+str(code_type)
                code = create_random_passwd(2)
                if self.mcache.get(cache_key):
                    self.mcache.set(cache_key,self.mcache.get(cache_key),180)
                    data = {'stat':'ok','info':'操作成功'}
                else:
                    is_ok = self.mcache.set(cache_key,code,180)
                    if code_type == '_reg':
                        content=PHONE_REG_TEMPLATE%(code)
                    elif code_type == '_login':
                        content=PHONE_LOGIN_TEMPLATE%(code)
                    else:
                        content=CHECK_CODE_TEMPLATE%(code)
                    if is_ok:
                        send_phone_msg(str(phone),content)
                        data={'stat':'ok','info':'发送成功'}
                    else:
                        data={'stat':'error','info':'memcache存储验证码失败'}
        self.write_json(data)

























