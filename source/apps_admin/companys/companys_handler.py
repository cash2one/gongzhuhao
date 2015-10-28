#encoding:utf-8
__author__ = 'frank'
from common.base import AdminBaseHandler
from services.company.company_services import CompanyServices
from services.users.user_services import UserServices
from services.permissions.permissions_service import PermissionsServices
from services.schedules.schedules_service import ScheduleService
from models.user_do import Users
from models.company_do import Company
from utils.regular import Regular
import ujson
import sys

schedule_service = ScheduleService()
company_service = CompanyServices()


class CompanyHandlerList(AdminBaseHandler):

    def get(self,code = None,*args, **kwargs):
        self.company_service = CompanyServices(self.db)
        self.get_companys(code)
        page_html = ''
        if self.page_data:
            page_html = self.page_data.render_page_html()
        context={'page_data':self.page_data,'page_html':page_html,'code':code}
        if code == 'recommend':
            self.echo('ops/home/companys.html',context)
        else:
            self.echo('ops/company/company_list.html',context)

    def get_companys(self,code = None):
        self.get_paras_dict()
        if code == '1':
            query = self.db.query(Company).filter(Company.Fdeleted == 1)
        else:
            query = self.company_service.get_companys(**self.qdict)
        self.page_data = self.get_page_data(query)

    def get_user_by_id(self,user_id):
        query = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fid==user_id).scalar()
        return query

class CompanyEditHandler(AdminBaseHandler):

    def get(self,company_id,*args,**kwargs):

        company_service = CompanyServices(self.db)
        user_services = UserServices(self.db)
        company = company_service.get_company_by_id(company_id)
        user = user_services.get_user_by_id(company.Fuser_id)
        self.echo('ops/company/company_edit.html',{'company':company,'user':user})

    def post(self, company_id,*args, **kwargs):
        rsg = {
            'stat':'err',
            'msg':''
        }
        self.get_paras_dict()
        if not self.qdict.get('Fcompany_name') or not self.qdict.get('Fdetail_address') or not self.qdict.get('nick_name') \
                or not self.qdict.get('user_mobi'):
            rsg['msg'] = '不能为空!'
            return self.write(ujson.dumps(rsg))
        company_service = CompanyServices(self.db)
        company_service.update_company_by_id(company_id,**self.qdict)
        rsg['stat'] = 'ok'
        return self.write(ujson.dumps(rsg))

class CompanyDeleteHandler(AdminBaseHandler):
    def get(self,company_id):
        rsg = {
            'stat':'err',
            'msg':''
        }
        try:
            company_service = CompanyServices(self.db)
            company_service.delete_company_by_id(company_id)
            rsg['stat'] = 'ok'
            return self.write(ujson.dumps(rsg))
        except Exception,e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            self.echo('apps_crm/404.html')

class CreateCompanyAccountHandler(AdminBaseHandler):

    def get(self,mct_id):
        permission_service = PermissionsServices(self.db)
        company_service = CompanyServices(self.db)
        permissions = permission_service.get_permissions()
        company_name = company_service.get_company_by_uid(mct_id).Fcompany_name
        self.echo('ops/company/accountable_create.html',{'permissions':permissions,'company_name':company_name})

    def post(self,mct_id):
        rsg = {'stat':'error','info':''}
        try:
            self.get_paras_dict()
            is_success,info = self.get_valid_args()
            if not is_success:
                rsg['info'] = info
                return self.write(ujson.dumps(rsg))
            company_service = CompanyServices(self.db)
            is_ok = company_service.create_login_account(mct_id,**self.qdict)
            if not is_ok:
                rsg['info'] = '添加不成功'
                return self.write(ujson.dumps(rsg))
        except Exception,e:
            print e
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))

    def get_valid_args(self):
        if not self.qdict.get('phone') or not Regular.check_phone(self.qdict['phone']):
            return False,'手机格式不正确'
        if not self.qdict.get('user_name'):
            return False,'用户名不能为空'
        if not self.qdict.get('user_pwd'):
            return False,'密码不能为空'
        return True,''

class CompanyActivityHandler(AdminBaseHandler):

    def post(self,user_id,code):

        rsp = {'stat':'error','info':''}

        data = {}
        data['Fis_activity'] = code

        try:
            company_service.set_db(self.db)
            company_service.update_company_by_uid(user_id,**data)
        except Exception,e:

            rsp['info'] = '添加活动失败'
            self.write(ujson.dumps(rsp))

        rsp['stat'] = 'ok'
        self.write(ujson.dumps(rsp))










