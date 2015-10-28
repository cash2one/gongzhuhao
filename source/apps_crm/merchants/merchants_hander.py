# encoding:utf-8
import tornado
import ujson
from common.base import BaseHandler
from common.regular_param import CheckHandler
from utils.error_util import Error
from services.users.user_services import UserServices
from services.company.company_services import CompanyServices,\
    CompanyUserServices, CompanyAdditionInfoServices
from services.company.location_service import LocationServices
from services.permissions.permissions_service import PermissionsServices
from services.users.user_services import UserServices
from models.user_do import Users
from common.permission_control import company_permission_control

user_service = UserServices()
company_service = CompanyServices()

class CHandlerMerchantsEdit(BaseHandler, CheckHandler):
    @tornado.web.authenticated
    @company_permission_control('merchant_information_view')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        company_db = CompanyServices(self.db)
        company_info = company_db.get_company_by_uid(uid_mct)
        province_db = LocationServices(self.db)
        province = province_db.get_location_name_list('province')
        if not province:
            return self.write("t_province no data")
        if company_info:
            city, area = province_db.get_city_area_list(
                company_info.Fprovince, company_info.Fcity)
        else:
            city, area = province_db.get_city_area_list(province.first().Fid)
        return self.echo('crm/merchant/edit_info_py.html', {
            'company': company_info if company_info else {},
            'type_class': 'base_setting',
            'province': province,
            'city': city,
            'area': area
            }, layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('merchant_information_edit')
    def post(self):
        rsp = {'stat': 'err', 'msg': ''}
        uid_mct = self.get_current_user().get('Fmerchant_id')
        self.get_paras_dict()
        del self.qdict['_xsrf']
        company_db = CompanyServices(self.db)
        # status, info = self.get_valid_args()
        # if not status:
        #     rsp['msg'] = info
        #     return self.write(rsp)
        if 'desc' in self.qdict:
            self.qdict['Fdescription'] = self.qdict.get('desc')
            del self.qdict['Fdescription']
        if not company_db.get_company_by_uid(uid_mct):
            company_db.create_company(
                uid_mct,
                self.qdict.get('Fcompany_name',''),
                self.qdict.get('Fdetail_address',''),
                self.qdict.get('Fphone',''),
                self.qdict.get('Fmail',''),
                **self.qdict
                )
        else:
            company_db.update_company_by_uid(uid_mct, **self.qdict)
        rsp['stat'] = 'ok'
        rsp['id'] = uid_mct
        cookies = ujson.loads(self.get_secure_cookie('loginuser'))
        if cookies['Fcompany_name'] != self.qdict['Fcompany_name']:
            cookies['Fcompany_name'] = self.qdict['Fcompany_name']
            self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=1)
        return self.write(ujson.dumps(rsp))

    def get_valid_args(self):
        location_db = LocationServices(self.db)
        res = self.check_args(
            Fcontact='',
            Fqq='',
            Fmail='',
            Fdescription='',
            Fphoto_url=''
        )
        if res:
            raise Error(2000, res, "参数错误")

        self.qdict['Faddress'] = u""
        for key in ['Fprovince', 'Fcity', 'Farea']:
            if not self.qdict.get(key):
                return False, '地址不正确'
            else:
                ad = location_db.get_location_name_by_id(
                    key[1:], int(self.qdict[key]))
                self.qdict['Faddress'] += ad
        self.qdict['Faddress'] += self.qdict.get('Fdetail_address').decode("utf8")
        return True, ''


class CHandlerMerchantsEditProvince(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('merchant_information_edit')
    def get(self, father_id):
        lct_srv = LocationServices(self.db)
        citys, areas = [], []
        if str(father_id).strip() in (-1,'-1'):
            city, area = [],[]

        else:city, area = lct_srv.get_city_area_list(father_id)
        for c in city:
            data = {}
            data['Fid'] = c[0]
            data['Fcity_name'] = c[1]
            citys.append(data)
        for a in area:
            data = {}
            data['Fid'] = a[0]
            data['Farea_name'] = a[1]
            areas.append(data)
        return self.write({'stat': 'ok', 'city': citys, 'area': areas})


class CHandlerMerchantsEditCity(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('merchant_information_edit')
    def get(self, father_id):
        location_db = LocationServices(self.db)
        location_info = location_db.get_location_name_list("area", father_id)
        lists = []
        for location in location_info:
            data = {}
            data['Fid'] = location[0]
            data['Farea_name'] = location[1]
            lists.append(data)
        if not lists:
            return self.write({'stat': 'err', 'msg': '无城市信息！请联系管理员'})
        return self.write({'stat': 'ok', 'list': lists})


class CHandlerMerchantsListRole(BaseHandler):
    #用户管理
    @tornado.web.authenticated
    def get(self, code=None, **kargs):
        p_svr = PermissionsServices(self.db)
        permissions = p_svr.get_permissions().all()

        self.user_service = UserServices(self.db)
        roles = self.user_service.get_roles()
        users = self.get_users(code)
        # if self.page_data:
        #     page_html = self.page_data.render_page_html()
        context = {
            #'page_data': self.page_data,
            'users':users,
            # 'page_html': page_html,
            'roles': roles,
            'status': Users.STATUS,
            'permissions': permissions,
            'code': code}
        self.echo(
            'crm/system/member.html', context,
            layout='crm/common/base.html')

    @tornado.web.authenticated
    def post(self):
        pass

    def get_users(self, code=None):
        uid_mct = self.get_current_user().get('Fid')
        self.get_paras_dict()
        code_dict = {'3': 'Fcreate_date desc'}

        if code and code_dict.get(code, None) and code in code_dict.keys():
            self.qdict['order_by'] = code_dict[code]
        user_srv = CompanyUserServices(self.db)
        users = user_srv.query_users(uid_mct)
        return users
        # if not code:  # 非员工用户
        #     pass  # query = query.filter(Users)
        # elif code == '1':  # 商户
        #     query = query.filter(Users.Frole_codes.like('%merchant%'))
        # elif code == '2':  # 员工
        #     query = query.filter(Users.is_employee == 1)
        #self.page_data = self.get_page_data2(users,50)


class CHandlerMerchantsEditRole(BaseHandler):
    """编辑可登陆人员信息"""
    @tornado.web.authenticated
    def get(self, user_id):
        p_svr = PermissionsServices(self.db)
        permissions = p_svr.get_permissions()

        uid_mct = self.get_current_user().get('Fid')
        # user_srv = CompanyUserServices(self.db)
        user_service.set_db(self.db)
        user = user_service.get_user_by_id(user_id)
        # self.get_paras_dict()
        # query = user_srv.query_users(uid_mct)

        # info = query.filter(Users.Fid == user_id).first()
        self.echo(
            'crm/system/member_edit.html',
            {"user": user, "permissions": permissions},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    def post(self, user_id):
        uid_mct = self.get_current_user().get('Fid')
        pms = self.check_arg('permission', u'^[\d\w,]{1,512}$', '')
        kwargs = {
            'Fuser_mobi': self.check_arg('user_mobi', u'^\d{1,28}$'),
            'Fnick_name': self.check_arg('user_name', u'^[\u4e00-\u9fa5\d\w\s]{1,28}$'),
            # 'Fnick_name': self.check_arg('nick_name', u'^[\u4e00-\u9fa5\d\w\s]{1,28}$', ''),
            'Femail': self.check_arg('user_email', u'^[\w\d@.]{1,64}$', ''),
            "Fpermission": pms
        }
        pwd_srv = UserServices(self.db)
        _user_pwd = self.check_arg('user_pwd', u'^[\d\w]{1,28}$', '')
        if _user_pwd:
            _user = pwd_srv.get_user_by_id(user_id)
            kwargs['Fuser_pwd'] = pwd_srv.user_passed(_user_pwd, _user.Fuid)

        user_srv = CompanyUserServices(self.db)
        user_srv.edit_users(uid_mct, user_id, **kwargs)
        return self.write({'stat': 'ok', 'msg': ''})


class CHandlerMerchantsDeleteRole(BaseHandler):
    @tornado.web.authenticated
    def get(self, user_id):
        uid_mct = self.get_current_user().get('Fid')
        user_srv = CompanyUserServices(self.db)
        user_srv.delete_users(uid_mct, user_id)
        return self.write({'stat': 'ok', 'msg': ''})

    @tornado.web.authenticated
    def post(self, user_id):
        return self.get(user_id)


class CHandlerMerchantsAddRole(BaseHandler):
    """新增可登陆人员"""
    @tornado.web.authenticated
    def get(self):
        p_svr = PermissionsServices(self.db)
        permissions = p_svr.get_permissions().all()
        return self.echo(
            'crm/system/member_add.html',
            {'permissions': permissions},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    def post(self):
        uid_mct = self.get_current_user().get('Fid')
        pms = self.check_arg('permission', u'^[\d\w,]{1,512}$', '')
        kwargs = {
            'Fuser_mobi': self.check_arg('user_mobi', u'^\d{1,28}$'),
            'Fuser_name': self.check_arg('user_name', u'^[\u4e00-\u9fa5\d\w\s]{1,28}$'),
            'Fuser_pwd': self.check_arg('user_pwd', u'^[\d\w]{1,28}$'),
            'Femail': self.check_arg('user_email', u'^[\w\d@.]{1,64}$', ''),
            'Fcompany_id': self.get_current_user().get('Fcompany_id'),
            "Fpermission": pms
        }
        pwd_srv = UserServices(self.db)
        user_srv = CompanyUserServices(self.db)
        user = pwd_srv.query_user_by_phone(self.get_argument('user_mobi').strip())
        if user:
            if pwd_srv.query_company_user(uid_mct,user.Fid):
                return self.write(ujson.dumps({'stat':'error','msg':'账号已存在!'}))
            else:
                data = {}
                data['Fpermission'] = kwargs.get('Fpermission')
                pwd_srv.update_user(user.Fid,**data)
        else:
            kwargs['Fuid'] = pwd_srv.user_uid(phone=kwargs['Fuser_mobi'],email=kwargs['Femail'])
            kwargs['Fuser_pwd'] = pwd_srv.user_passed(kwargs['Fuser_pwd'], kwargs['Fuid'])
            user = user_srv.add_users(**kwargs)
        user_srv.add_company_user(user,uid_mct,**kwargs)
        return self.write(ujson.dumps({'stat': 'ok', 'msg': ''}))

class CHandlerShareExtendInfo(BaseHandler, CheckHandler):
    """设置分享推广信息"""
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        p_svr = CompanyAdditionInfoServices(self.db)
        info = p_svr.query_info(uid_mct, 'share_extend_info').first()
        return self.echo(
            'crm/system/share_extend_info.html',
            {'info': info},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        self.get_paras_dict()
        uid_mct = self.get_current_user().get('Fmerchant_id')
        res = self.check_args()
        if res:
            self.write(Error(2000, res, "参数错误").__dict__)

        self.qdict['Finfo_key'] = 'share_extend_info'
        del self.qdict['_xsrf']
        if self.qdict['Fid'] == '0':
            del self.qdict['Fid']
        srv = CompanyAdditionInfoServices(self.db)
        srv.update_info(uid_mct, **self.qdict)
        return self.write(Error(0).__dict__)


class CHandlerSharePrizeInfo(BaseHandler, CheckHandler):
    """设置分享奖励信息"""
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        p_svr = CompanyAdditionInfoServices(self.db)
        info = p_svr.query_info(uid_mct, 'share_prize_info').first()
        return self.echo(
            'crm/system/share_prize_info.html',
            {'info': info},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        self.get_paras_dict()
        uid_mct = self.get_current_user().get('Fmerchant_id')
        res = self.check_args()
        if res:
            self.write(Error(2000, res, "参数错误").__dict__)

        self.qdict['Finfo_key'] = 'share_prize_info'
        del self.qdict['_xsrf']
        if self.qdict['Fid'] == '0':
            del self.qdict['Fid']
        srv = CompanyAdditionInfoServices(self.db)
        srv.update_info(uid_mct, **self.qdict)
        return self.write(Error(0).__dict__)

class MerchantGiftHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self,type):
        merchant_id = self.get_current_user().get('Fmerchant_id')
        company_service.set_db(self.db)
        gift = company_service.get_gift(merchant_id,type).scalar()
        if type == '1':
            self.echo('crm/system/merchant_gift.html',{'gift':gift})
        else:
            self.echo('crm/system/order_gift.html',{'gift':gift})

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self,type):
        company_service.set_db(self.db)
        self.get_paras_dict()
        self.qdict['type'] = type
        self.qdict['merchant_id'] = self.get_current_user().get('Fmerchant_id')
        company_service.create_gift(**self.qdict)
        return self.write(ujson.dumps({'stat':'ok','data':{}}))














