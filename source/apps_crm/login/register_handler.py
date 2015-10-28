#encoding:utf-8
__author__ = 'morichounami'
from common.base import *
from utils.regular import *
from models.user_do import *
from services.users.merchants_services import *
from common.regular_param import CheckHandler
from services.users.user_services import UserServices

class RegisterHandler(BaseHandler):
    def get(self):
        return self.echo('')

    def post(self):
        self.get_paras_dict()
        merchant_services = MerchantsServices(self.db)
        rsp = {
            'stat': 'err',
            'msg': ''
        }
        try:
            is_ok,info = self.check_params() #验证手机和密码
            if not is_ok:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            is_ok,info = self.check_user_name() #验证用户名
            if not is_ok:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            is_ok,info = self.registe_check_exist()#验证手机和用户名是否被占用
            if not is_ok:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            is_ok,info = self.check_mct_name()
            if not is_ok:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            is_ok,info = self.check_mct_address()
            if not is_ok:
                rsp['msg'] = info
                return self.write(ujson.dumps(rsp))

            mct = Merchants()
            mct.Fuser_name = self.qdict.get('user_name')
            mct.Fuser_pwd = self.qdict.get('user_pwd')
            mct.Fuser_mobi = self.qdict.get('user_mobi')
            mct.Fmct_name = self.qdict.get('mct_name')
            mct.Fmct_address = self.qdict.get('mct_address')
            self.db.add(mct)
            self.db.commit()
            data = {}
            data['Fuid'] = "%07d"%mct.Fid
            merchant_services.update_fuid_by_fid(mct.Fid,**data)

            cookies = merchant_services.merchant_format(merchant_services.get_merchant_by_fid(mct.Fid))
            self.set_secure_cookie('loginuser',ujson.dumps(cookies))
            rsp['stat'] = 'ok'
        except Exception,e:
            print e
        return self.write(ujson.dumps(rsp))

    def check_params(self):
        if not self.qdict.get('Fuser_mobi').strip():
            return False,'电话不能为空'
        elif not Regular.check_phone(self.qdict.get('Fuser_mobi')):
            phone = self.qdict.get('Fuser_mobi')
            return False,'电话号码错误'
        if (not self.qdict.get('Fuser_pwd', '').strip()) or len(self.qdict.get('Fuser_pwd', '').strip())<6 or len(self.qdict.get('Fuser_pwd', '').strip())>12:
            return False,'密码设置应该在6－12位之间'
        return True,''

    def check_user_name(self):
        try:
            if not self.qdict.get('Fuser_name').strip():
                return False,'用户名不能为空'
        except Exception,e:
            print e
        return True,''

    def registe_check_exist(self):
        """
        注册检测  用户名手机是否已经被占用
        """
        if self.qdict.get('Fuser_name') and self.db.query(Merchants).filter(Merchants.Fuser_name == self.qdict.get('Fuser_name'),Merchants.Fdeleted == False).count()>0:
            return False, '用户名已被占用'
        if self.qdict.get('Fuser_mobi') and self.db.query(Merchants).filter(Merchants.Fuser_mobi == self.qdict.get('Fuser_mobi'),Merchants.Fdeleted == False).count()>0:
            return False, '手机号码已被占用'
        return True, ''

    def check_mct_name(self):
        if not self.qdict.get('Fmct_name').strip():
            return False, '商户名不能为空'
        return True, ''

    def check_mct_address(self):
        if not self.qdict.get('Fmct_address').strip():
            return False, '商户地址不能为空'
        return True, ''


class ResetInfoHandler(BaseHandler, CheckHandler):
    @tornado.web.authenticated
    def get(self):
        Fid = self.get_current_user().get('Fid')
        u_svr = UserServices(self.db)
        user = u_svr.get_user_by_id(Fid)
        return self.echo(
            'crm/login/user_info_edit.html',
            {'user': user},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    def post(self):
        res = self.check_args(
            Fbirthday='',
            Femail='',
            Fweixin='',
            Fweibo='',
            Fqq='',
            Fuser_pwd='',
        )
        if res:
            return self.write(Error(2000, res, "参数错误").__dict__)

        Fid = self.get_current_user().get('Fid')
        self.get_paras_dict()
        del self.qdict['_xsrf']
        user_srv = UserServices(self.db)
        if self.qdict['Fuser_pwd']:
            _user = user_srv.get_user_by_id(Fid)
            self.qdict['Fuser_pwd'] = user_srv.user_passed(
                self.qdict['Fuser_pwd'],
                _user.Fuid)
        user_srv.update_user(Fid, **self.qdict)
        return self.write({'stat': 'ok', 'msg': ''})