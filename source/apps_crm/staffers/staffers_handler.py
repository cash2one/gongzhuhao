# encoding:utf-8

__author__ = 'morichounami'

import tornado
import ujson
from common.base import BaseHandler
from common.permission_control import company_permission_control
from tornado.web import MissingArgumentError
from utils.error_util import Error
from services.departments.department_services import DepartmentService as DptShowServices
from services.staffers.staffer_services import *
from conf.merchant import _MERCHANG_DEPARTMENT_TITLES
import sys

class CHandlerStaffersList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self, dpt_id=None):
        staffer_service = StafferServices(self.db)
        staffers = staffer_service.get_staffers_by_department_id(
            self.get_current_user().get('Fmerchant_id'),
            dpt_id)
        svr_dpt = DptShowServices(self.db)
        departments = svr_dpt.get_dpt_list(
            self.get_current_user().get('Fmerchant_id'))

        self.echo('crm/member/staffers_list_py.html', {
            'staffers': staffers,
            'departments': departments,
            '_MERCHANG_DEPARTMENT_TITLES': _MERCHANG_DEPARTMENT_TITLES
        })

    @tornado.web.authenticated
    def post(self):
        pass


class CHandlerStaffersAdd(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.echo('crm/404.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        try:
            #dpt_id = self.check_arg('dpt_id', u'^\d{1,2}$')
            dpt_id = self.get_argument('dpt_id')
            staf_name = self.check_arg('name', u'^[\u4e00-\u9fa5\w\s]{1,16}$')
            staf_email = self.check_arg('email', u'^[\w\d@.]{1,64}$', '')
            staf_phone = self.check_arg('mobi', u'^[0-9_-]{4,16}$', '')
            staf_job = self.check_arg('title', u'^[\u4e00-\u9fa5\w\s]{1,16}$', '')

            svr_dpt = DptShowServices(self.db)
            department = svr_dpt.check_user_dpt(
                self.get_current_user().get('Fmerchant_id'),
                dpt_id)
            if not department:
                raise Error(1, "dpt not exist")

            staffer_service = StafferServices(self.db)
            staffer_service.add_department_staff(
                self.get_current_user().get('Fmerchant_id'),
                department,
                staf_name,
                staf_phone,
                staf_email,
                staf_job)
            self.write(Error(0, 'succ').__dict__)

        except MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)


class CHandlerStaffersEdit(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self, stf_id=None):
        dic_result = {}
        dic_result['stat'] = 'succ'
        dic_result['msg'] = ''

        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')
            #基础表
            dpts = DptShowServices(self.db).get_dpt_list(uid_mct)
            items = [dpt._asdict() for dpt in dpts]
            dic_result['dpt_items'] = items
            dic_result['_MERCHANG_DEPARTMENT_TITLES'] = _MERCHANG_DEPARTMENT_TITLES

            if stf_id:  #编辑时
                stf = StafferServices(self.db).get_staffer_by_id(uid_mct, stf_id)
                dic_result['Fid'] = stf.Fid
                dic_result['Fname'] = stf.Fname
                dic_result['Fdepartment_id'] = stf.Fdepartment_id
                dic_result['Ftitle'] = stf.Ftitle
                dic_result['Femail'] = stf.Femail
                dic_result['Fmobi'] = stf.Fmobi
            else:   #新增时
                dic_result['Fid'] = '0'
                dic_result['Fname'] = ''
                dic_result['Fdepartment_id'] = ''
                dic_result['Ftitle'] = ''
                dic_result['Femail'] = ''
                dic_result['Fmobi'] = ''
        except Exception, e:
            dic_result['stat'] = 'fail'
            dic_result['msg'] = '获取员工信息失败'

        self.write(ujson.dumps(dic_result))

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self, stf_id):
        try:
            stf_id = int(stf_id)
            uid_mct = self.get_current_user().get('Fmerchant_id')
            dpt_id = self.get_argument('dpt_id')
            staf_name = self.check_arg('name', u'^[\u4e00-\u9fa5\w\s]{1,16}$')
            staf_email = self.check_arg('email', u'^[\w\d@.]{1,64}$', '')
            staf_phone = self.check_arg('mobi', u'^[0-9_-]{4,16}$', '')
            staf_job = self.check_arg('title', u'^[\u4e00-\u9fa5\w\s]{1,16}$', '')

            if stf_id:  #编辑
                data = {}
                data['Fname'] = staf_name
                data['Fdepartment_id'] = dpt_id
                data['Ftitle'] = staf_job
                data['Femail'] = staf_email
                data['Fmobi'] = staf_phone

                svr_dpt = DptShowServices(self.db)
                svr_stf = StafferServices(self.db)
                department = svr_dpt.check_user_dpt(uid_mct, data['Fdepartment_id'])
                staffer = svr_stf.get_staffer_by_id(uid_mct, stf_id)
                if not department or not staffer:
                    raise Error(1, "dpt/staffer not exist")

                data['Fdepartment_name'] = department.Ffull_department_name

                if 'staffer_img' in self.request.files:
                    is_ok, filenames = svr_stf.upload_to_server(
                        self,
                        param_name='staffer_img',
                        file_prex='staffers')
                    if is_ok:
                        data['staffer_img_url'] = '/'+filenames[0]['full_name']  # 存数据库的时候在前面要加‘/’

                svr_stf.update_staffer_by_id(stf_id, **data)

            else:   #新增
                svr_dpt = DptShowServices(self.db)
                department = svr_dpt.check_user_dpt(
                    self.get_current_user().get('Fmerchant_id'),
                    dpt_id)
                if not department:
                    raise Error(1, "dpt not exist")

                staffer_service = StafferServices(self.db)
                staffer_service.add_department_staff(
                    self.get_current_user().get('Fmerchant_id'),
                    department,
                    staf_name,
                    staf_phone,
                    staf_email,
                    staf_job)

            self.write(Error(0, 'succ').__dict__)

        except MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)


class CHandlerStaffersDelete(BaseHandler):
    @tornado.web.authenticated
    def get(self, stf_id):
        self.echo('crm/404.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self, stf_id):
        data={'state':'ok','info':'删除成功'}
        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')
            svr_stf = StafferServices(self.db)
            svr_stf.delete_staffer_by_id(uid_mct, stf_id)
            # return self.write(ujson.dumps(data))
        except Exception,e:
            data={'state':'ok','info':'删除失败 失败原因:'+e.message}
            
        return self.write(ujson.dumps(data))

class CHandlerStafferCreate(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        pass


class StafferHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, department_id=None):
        pass


