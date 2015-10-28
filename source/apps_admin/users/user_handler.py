#encoding:utf-8
__author__ = 'binpo'

from common.base import AdminBaseHandler
import ujson
from services.users.user_services import UserServices
from services.company.company_services import CompanyServices
from services.locations.location_services import LocationServices2
from models.user_do import Users
from models.company_do import CompanyUsers,Company
import logging
from models.user_do import Roles
import tornado.web
from utils.regular import Regular
import sys

user_service = UserServices()
company_service = CompanyServices()
location_service = LocationServices2()

class UserQueryHandler(AdminBaseHandler):

    def get(self,code=None,**kargs):

        # import pdb
        # pdb.set_trace()

        self.user_service = UserServices(self.db)
        roles = self.user_service.get_roles()
        self.get_users(code)
        page_html=''
        if self.page_data:
            page_html = self.page_data.render_page_html()
        context={'page_data':self.page_data,'page_html':page_html,'code':code,'status':Users.STATUS,'roles':roles}
        self.echo('ops/users/user_list.html',context)

    def post(self,operation,code=None, **kwargs):
        if operation=='new':
            self.get_argument('','')
            self.write('OK')

    def get_users(self,code=None):

        # import pdb
        # pdb.set_trace()
        self.get_paras_dict()
        code_dict={}
        code_dict={'3':'Fcreate_time desc','4':'coin desc'}

        if code and code_dict.get(code,None) and code in code_dict.keys():
            self.qdict['order_by'] = code_dict[code]
        query = self.user_service.query_users(**self.qdict)
        if not code: #非员工用户
            pass
        elif code=='1': #商户
            query = query.filter(Users.Frole_codes.like('%merchant%'))
        elif code=='2': #员工
             query = query.filter(Users.is_employee==1)
        self.page_data = self.get_page_data(query)

    def get_company(self,user):

        try:
            company_service.set_db(self.db)
            company = self.db.query(Company).filter(Company.Fdeleted == 0,Company.Fuser_id == user.Fid).scalar()
            if not company:
                company_user = self.db.query(CompanyUsers).filter(CompanyUsers.Fdeleted == 0,CompanyUsers.Fuser_id == user.Fid).scalar()
                company = self.db.query(Company).filter(Company.Fdeleted == 0,Company.Fuser_id == company_user.Fuid_mct).scalar()
        except Exception,e:

            company=''
        return company


class AuthorizeHandler(AdminBaseHandler):
    def get(self,user_id):
        user_service = UserServices(self.db)
        roles = user_service.get_roles()
        user = self.db.query(Users).filter(Users.Fdeleted == 0,Users.Fid == user_id).scalar()
        self.echo('ops/users/authorize.html',{'roles':roles,'user':user})

    def post(self,user_id):
        rsg = {
            'stat':'error',
            'msg':'',
        }
        self.get_paras_dict()
        data = {}
        data['Frole_codes'] = self.qdict.get('Frole_codes')
        try:
            query = self.db.query(Users).filter(Users.Fdeleted == 0,Users.Fid == user_id)
            query.update(data)
            self.db.commit()

        except Exception,e:
            print e
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))


class UserEditHandler(AdminBaseHandler):
    '''
    编辑用户
    '''
    @tornado.web.authenticated
    def get(self,user_id,operation = None, *args, **kwargs):
        user_service.set_db(self.db)
        company_service.set_db(self.db)
        user = user_service.get_user_by_id(user_id)
        roles = user_service.get_roles()
        if 'merchant' in user.Frole_codes:
            company = company_service.get_company_by_uid(user.Fid)
            if not company:
                company_user = self.db.query(CompanyUsers).filter(CompanyUsers.Fdeleted == 0,CompanyUsers.Fuser_id == user_id).scalar()
                company = company_service.get_company_by_id(company_user.Fcompany_id)
            self.echo('ops/users/edit.html',{'user':user,'roles':roles,'company':company})
        else:
            self.echo('ops/users/edit.html',{'user':user,'roles':roles})

    @tornado.web.authenticated
    def post(self,user_id,operation,*args, **kwargs):
        self.get_paras_dict()
        self.qdict.pop('_xsrf')
        user_service.set_db(self.db)
        company_service.set_db(self.db)
        if operation=='reeze':
            self.operation_name='冻结用户'
            user_service.set_user_reeze(user_id)
        elif operation=='permission':
            # print self.qdict.get('roles')
            # print type(self.qdict.get('roles'))
            self.operation_name='用户授权'
            user_service.set_user_roles(user_id,self.qdict.get('roles'))
        else:
            data = {}
            if self.qdict.get('Fcompany_name') or self.qdict.get('Faddress'):
                data['Fcompany_name'] = self.qdict.get('Fcompany_name',None)
                data['Faddress'] = self.qdict.get('Faddress',None)
                data['Fphone'] = self.qdict.get('Fuser_mobi',None)
                company_service.update_company_by_uid(user_id,**data)
                self.qdict.pop('Fcompany_name')
                self.qdict.pop('Faddress')
            user_service.update_user(user_id,**self.qdict)
        return self.write(ujson.dumps({'status':'success','info':'更新成功'}))



class UserDeleteHandler(AdminBaseHandler):
    '''
        删除用户用户
    '''
    def get(self,user_id, *args, **kwargs):
        Users.set_attr(self.db,user_id,'Fdeleted',1)
        self.operation_name='删除用户'
        return self.write(ujson.dumps({'status':'success','info':'删除成功'}))

class UserCreateHandler(AdminBaseHandler):

    def get(self):
        self.user_service = UserServices(self.db)
        location_service.set_db(self.db)
        provinces = location_service.get_location_name_list('province')
        roles = self.user_service.get_roles()
        self.echo('ops/users/create.html',{'roles':roles,'provinces':provinces})

    def post(self, *args, **kwargs):
        data = {'status':'success','info':'创建成功'}
        user_service.set_db(self.db)
        self.get_paras_dict()
        self.qdict.pop('_xsrf')
        if not self.qdict.get('user_name','').strip() and not self.qdict.get('phone','').strip():
            return self.write(ujson.dumps({'stat':'error','info':'账号或手机必须有一项不能为空'}))
        if (self.qdict.get('phone') and user_service.query_user_by_phone(self.qdict.get('phone'))) or (self.qdict.get('user_name') and user_service.query_user_by_userName(self.qdict.get('user_name'))): #检测重复账号
            return self.write(ujson.dumps({'stat':'error','info':'账号已存在'}))

        user_roles = self.db.query(Roles).filter(Roles.Fid.in_(self.qdict.get('roles',''))).all()
        Frole_codes=''
        if user_roles:
            Frole_codes = ','.join([r.Fcode for r in user_roles])
        if 'merchant' in Frole_codes:
            if not self.qdict.get('merchant_name'):
                data['status']='error'
                data['info'] = '公司信息不能为空'
                return self.write(ujson.dumps(data))
            else:
                is_success,info = user_service.create_user(**self.qdict)
        else:
            is_success,info = user_service.create_user(**self.qdict)
        if not is_success:
            data['status']='error'
            data['info'] = info
        self.write(ujson.dumps(data))

    def get_valid_args(self):
        if not self.qdict.get('phone') or not Regular.check_phone(self.qdict['phone']):
            return False,'手机格式不正确'
        return True,''

class UserResetPasswd(AdminBaseHandler):

    def get(self,user_id=None):
        self.echo('ops/users/reset_passwd.html',{'user_id':user_id})

    def post(self,user_id=None):
        self.get_paras_dict()
        #if
        #user_id = self.qdict.get('user_id')
        password = self.qdict.get('user_pwd')
        user_service.set_db(self.db)
        self.operation_name='重置用户密码'
        user_service.reset_passwd(user_id,password)
        self.write('OK')

class ProvinceChangeHandler(AdminBaseHandler):
    def get(self,province_id):
        rsg = {
            'stat':'error',
            'msg':'',
        }
        location_service.set_db(self.db)
        try:
            query_city = location_service.get_city_by_province_id(province_id)
            query_area = location_service.get_area_by_city_id(query_city[0].Fid)
        except Exception,e:
            if self.settings.get('debug'):
                raise
            self.write('apps_crm/404.html')
        cities = []
        areas = []
        for city in query_city:
            data = {}
            data['Fid'] = city.Fid
            data['Fcity_name'] = city.Fcity_name
            cities.append(data)
        for area in query_area:
            data = {}
            data['Fid'] = area.Fid
            data['Farea_name'] = area.Farea_name
            areas.append(data)
        rsg['stat'] = 'success'
        rsg['city'] = cities
        rsg['area'] = areas
        self.write(ujson.dumps(rsg))

class CityChangeHandler(AdminBaseHandler):
    def get(self,city_id):
        rsg = {
            'stat':'error',
            'msg':''
        }
        location_service.set_db(self.db)
        try:
            query_area = location_service.get_area_by_city_id(city_id)
            areas = []
            for area in query_area:
                data = {}
                data['Fid'] = area.Fid
                data['Farea_name'] = area.Farea_name
                areas.append(data)
        except Exception,e:
            if self.settings.get('debug'):
                raise
            self.write('apps_crm/404.html')
        rsg['stat'] = 'success'
        rsg['area'] = areas
        self.write(ujson.dumps(rsg))













