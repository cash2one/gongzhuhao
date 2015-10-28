#encoding:utf-8
__author__ = 'morichounami'
from common.base import BaseHandler
import tornado
from services.users.user_services import UserServices
from services.orders.order_services import OrderServices
from services.shares.shares_service import ShareServices
from services.ablums.photos_service import PhotosServices
from utils.upload_utile import upload_to_oss
from tornado.options import options
from models.company_do import *
from models.order_do import *
from apps_mobile.mobile_base import MobileBaseHandler
from common.permission_control import Mobile_login_control
from common.cache_base import AppCacheHandler
import ujson
import sys


user_service = UserServices()
order_service = OrderServices()
share_service = ShareServices()
photo_service = PhotosServices()


class MobileUserIndexHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self):
        self.echo('index.html')

    def get_schedule_title(self,order_id):
        order = self.db.query(Orders).filter(Orders.Fid==order_id).scalar()
        if order:
            company = self.db.query(Company).filter(
                Company.Fuser_id == order.Fuid_mct,
                Company.Fdeleted == 0).scalar()
        name = order.Fuser_name
        if order and order.Fuser_name_ex:
            name = order.Fuser_name+'&'+order.Fuser_name_ex
        return company.Fcompany_name,name

class ChangePwdHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self, *args, **kwargs):
        pass

    @Mobile_login_control()
    def post(self, *args, **kwargs):
        user_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        user = user_service.get_user_by_id(user_id)
        user_agent = self.request.headers.get('Request-Type')
        if user_agent and user_agent == 'apicloud':
            self.get_paras_dict()
            body = self.qdict
        else:
            body = ujson.loads(self.request.body)

        old_pwd = body.get('old_pwd')
        new_pwd = body.get('new_pwd')
        confirm_pwd = body.get('confirm_pwd')
        update_pwd = body.get('update_pwd')

        try:
            data = {}

            if update_pwd:
                phone, code_type, code = body.get('phone'), body.get('code_type'), body.get('code')
                cache_key = str(phone)+str(code_type)

                if not code or self.mcache.get(cache_key) != code:
                    return self.write_json({'stat':'1004','info':'验证码错误'})
                if len(update_pwd) < 6:
                    return self.write_json({'stat':'1004','info':'密码长度不能小于6位'})

                new_pwd = update_pwd
            else:
                if not old_pwd or not new_pwd or not confirm_pwd:
                    return self.write_json({'stat':'1004','info':'密码不能为空'})
                if len(new_pwd) <6 or len(confirm_pwd) < 6:
                    return self.write_json({'stat':'1004','info':'密码长度不能小于6位'})
                if new_pwd != confirm_pwd:
                    return self.write_json({'stat':'1004','info':'新密码两次输入不相同'})

                is_ok,msg = user_service.check_user_login_pwd(user.Fuser_mobi,old_pwd)
                if not is_ok:
                    return self.write_json({'stat':'1004','info':'原密码错误'})

            data['Fuser_pwd'] = user_service.user_passed(new_pwd,user.Fuid)
            user_service.update_user(user_id,**data)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'An exception occured,caused:'+e.message})

        self.write_json({'stat':'1000','info':''})

class UserSetHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self):
        user_id = self.get_current_user().get('Fid')
        user_service.set_db(self.db)
        try:
            user = user_service.get_user_by_id(user_id)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})

        print 'data:',{
                         'stat':'1000',
                         'Fuser_name':user.Fuser_name,
                         'Fnick_name':user.Fnick_name,
                         'Faddress':user.Faddress,
                         'Fsign_text':user.Fsign_text,
                         'head_photo':user.Fphoto_url
                        }

        self.write_json({
                         'stat':'1000',
                         'Fuser_name':user.Fuser_name,
                         'Fnick_name':user.Fnick_name,
                         'Faddress':user.Faddress,
                         'Fsign_text':user.Fsign_text,
                         'head_photo':user.Fphoto_url
                        })

    @Mobile_login_control()
    def post(self):
        user_id = self.get_current_user().get('Fid')
        user_service.set_db(self.db)
        body = ujson.loads(self.request.body)
        if not body.get('Fnick_name'):
            return self.write_json({'stat':'1006','info':'昵称不能为空'})
        try:
            user_service.update_user(user_id,**body)
            self.delete_user_info(str(user_id))
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})
        self.write_json({'stat':'1000'})

class UserPhotoUploadHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self):
        pass

    @Mobile_login_control()
    def post(self):
        user_id = self.get_current_user().get('Fid')
        try:
            file_prefix = '/'.join([str(user_id),'head_photo'])
            is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET,file_prex=file_prefix,param_name='user_img',file_type='img')
            if is_ok:
                for file in filenames:
                    head_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                    data = {}
                    data['Fphoto_url'] = head_url
                    user_service.update_user(user_id,**data)
                    self.delete_user_info(str(user_id))
            else:
                return self.write_json({'stat':'1005','info':'图片上传失败'})
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})
        self.write_json({'stat':'1000'})

class ShowServicesHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self):
        user_id = self.get_current_user().get('Fid')
        user_service.set_db(self.db)
        try:
            user = user_service.get_user_by_id(user_id)
            if user.Frole_codes or 'orders_view' in user.Fpermission:
                is_ok = '1'
            else:
                is_ok = '0'
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'An exception occurred,causes:'+e.message})
        head_photo_url = '/static/images/images.png' if not user.Fphoto_url else user.Fphoto_url
        self.write_json({'stat':is_ok,'head_photo_url':head_photo_url,'user_mobi':user.Fuser_mobi,'nick_name':user.Fnick_name})


class TopicUrlTransform(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self,aim,**kwargs):
        redirect_url = '/mobile/user/index/#/'+aim
        self.redirect(redirect_url)





