# encoding:utf-8

import tornado
import ujson

from common.base import BaseHandler
from common.permission_control import company_permission_control
from tornado.web import MissingArgumentError
from services.staffers.staffer_services import StafferServices
from utils.error_util import Error
from services.departments.department_services import DepartmentService, DeleteServices
from conf.merchant import _MERCHANG_DEPARTMENT_TITLES

class CHandlerDepartmentsList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self, dpt_id=None):
        """ 获取当前用户的所有部门 """
        try:
            staffer_service = StafferServices(self.db)
            if dpt_id == '0':
                dpt_id = None
            staffers = staffer_service.get_staffers_by_department_id(
                self.get_current_user().get('Fmerchant_id'),
                dpt_id)
            svr_dpt = DepartmentService(self.db)
            departments = svr_dpt.get_dpt_list(
                self.get_current_user().get('Fmerchant_id'))

            if not dpt_id:
                dpt_id = ''

            self.echo('crm/department/department_list_py.html', {
                'staffers': staffers,
                'departments': departments,
                '_MERCHANG_DEPARTMENT_TITLES': _MERCHANG_DEPARTMENT_TITLES,
                'dpt_id' : dpt_id,
                })
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            self.echo('crm/404.html')

    @tornado.web.authenticated
    def post(self):
        pass

class CHandlerGetDepartList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self, depart_id = None):
        """ 获取当前部门下的所有子部门 """
        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')
            db_dpt = DepartmentService(self.db)

            #整理成json
            lst_dept = []   #所有部门
            #根，即检索level 0的部门
            Level0_dpt = db_dpt.get_dpt_by_level(uid_mct, 0)
            if Level0_dpt:
                Level0_dpt = Level0_dpt[0]
                dic_dept = {}
                dic_dept['id'] = Level0_dpt.Fid
                dic_dept['text'] = str(Level0_dpt.Fname)
                dic_dept['type'] = 'root'
                dic_dept_state = {}
                dic_dept_state['opened'] = 'true'
                if depart_id == dic_dept.get('id') or depart_id == '':
                    depart_id = Level0_dpt.Fid
                    dic_dept_state['selected'] = 'true'
                dic_dept['state'] = dic_dept_state
                children = []
                #检索level 1的部门
                Level1_dpts = db_dpt.get_dpt_by_level(uid_mct, 1)
                for L1 in Level1_dpts:
                    dpts = self.getAllDeparts(uid_mct, depart_id, L1.Fid)
                    children.append(dpts)
                dic_dept['children'] = children
                lst_dept.append(dic_dept)
            else:#第一次，没有任何部门，直接创建根部门
                db_ds = DepartmentService(self.db)
                cur_dept = db_ds.add_dpt(uid_mct, '公司名称', -1)
                db_ds.update_dpt(uid_mct, cur_dept.Fid, Ffull_departm_id='/' +str(cur_dept.Fid))

                dic_dept = {}
                dic_dept['id'] = cur_dept.Fid
                dic_dept['text'] = str(cur_dept.Fname)
                dic_dept['type'] = 'root'

                lst_dept.append(dic_dept)

            result = ujson.dumps(lst_dept)
            self.write(result)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            self.write('')

    def getAllDeparts(self, uid_mct, L1_depart_id, depart_id):
        db_dpt = DepartmentService(self.db)
        dpt = db_dpt.get_dpt_by_id(uid_mct, depart_id)

        dic_dept = {}
        dic_dept['id'] = dpt.Fid
        dic_dept['text'] = str(dpt.Fname)
        dic_dept_state = {}
        dic_dept_state['opened'] = 'true'
        if L1_depart_id == str(dic_dept.get('id')):
            dic_dept_state['selected'] = 'true'
        dic_dept['state'] = dic_dept_state

        child_dpts = db_dpt.get_dpt_by_father_id(uid_mct, dpt.Fid)
        if child_dpts:  #存在子
            lst_c_dpts = []
            for c_dpt in child_dpts:
                lst_c_dpts.append(self.getAllDeparts(uid_mct, L1_depart_id, c_dpt.Fid))
            dic_dept['children'] = lst_c_dpts

        return  dic_dept

class CHandlerDepartmentsAdd(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        pass

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        """ 添加部门 """
        dic_result = {}
        dic_result['stat'] = 'succ'
        dic_result['msg'] = ''

        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')
            name = self.check_arg('dpt_name', u'^[\u4e00-\u9fa5\w\s]{1,21}$')
            dpt_id = self.get_argument('dpt_pre_id', '0')
            if dpt_id == 'NaN':
                pre_id = 0
            else:
                pre_id = self.check_arg('dpt_pre_id', u'^\d{1,8}$')

            db_orders = DepartmentService(self.db)
            dpt = db_orders.add_dpt(uid_mct, name, pre_id)
            dic_result['id'] = dpt.Fid
            self.write(ujson.dumps(dic_result))

        except MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)

class CHandlerDepartmentRename(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        pass

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        """ 修改部门名称 """
        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')
            name = self.check_arg('dpt_name', u'^[\u4e00-\u9fa5\w\s]{1,21}$')   #要更新的名称
            dpt_id = self.check_arg('dpt_id', u'^\d{1,8}$')

            #检索当前对象
            db_orders = DepartmentService(self.db)
            cur_dept = db_orders.get_dpt_by_id(uid_mct, dpt_id)
            if not cur_dept:
                if int(dpt_id) == 0:#根，直接新建
                    cur_dept = db_orders.add_dpt(uid_mct, name, -1)

                    db_orders.update_dpt(uid_mct, cur_dept.Fid, Ffull_departm_id='/' +str(cur_dept.Fid))
                else:#其他子部门
                    raise '部门不存在！'

            #准备全路径名称
            old_name = cur_dept.Fname
            new_full_depart_name = ''
            old_full_depart_name = cur_dept.Ffull_department_name
            if old_full_depart_name[-(len(old_name)+1):] == ('/' + old_name):    #首，结尾匹配
                new_full_depart_name = old_full_depart_name[:-(len(old_name)+1)] + ('/' + name)
            elif old_full_depart_name.find('/' + old_name + '/') > -1:   #中间匹配
                new_full_depart_name = old_full_depart_name.replace('/' + old_name + '/', ('/' + name + '/'))
            else:   #未匹配到时，根据父的全路径重建？？？
                pass

            #更新
            db_orders.update_dpt(uid_mct, cur_dept.Fid, Fname=name, Ffull_department_name=new_full_depart_name)

            #更新子的全路径名称
            staffer_service = StafferServices(self.db)
            child_dpts = db_orders.get_child_dpts(uid_mct, cur_dept.Ffull_departm_id)
            for c_dpt in child_dpts:
                c_new_full_depart_name = c_dpt.Ffull_department_name
                c_new_full_depart_name = new_full_depart_name + c_new_full_depart_name[len(old_full_depart_name):]
                db_orders.update_dpt(uid_mct, c_dpt.Fid, Ffull_department_name=c_new_full_depart_name)

                #更新员工表中的部门全路径
                staffer_service.update_staffer_full_depart_name(c_dpt.Fid, c_new_full_depart_name)

            #更新员工表中的部门全路径
            staffer_service.update_staffer_full_depart_name(cur_dept.Fid, new_full_depart_name)


            self.write(Error(0, 'succ').__dict__)

        except MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)

class CHandlerDepartmentsDelete(BaseHandler):
    """ 删除部门 非叶子部门不能删除 """
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        return self.echo('crm/404.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self, dpt_id):
        try:
            uid_mct = self.get_current_user().get('Fid')
            db_orders = DeleteServices(self.db)
            db_orders.delete_dpt(uid_mct, dpt_id)
            self.write(Error(0, 'succ').__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)


class DepartmentQueryHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        self.get_paras_dict()
        _id = self.qdict.get('id')
        data=[]

        department_service = DepartmentService(self.db)
        if not _id:
            departments = department_service.get_dpt_by_level(self.get_current_user().get('Fmerchant_id'),0)
            for d in departments:
                dept={'id':d.Fid, 'pId':d.Fdepartment_father, 'name':d.Fname,'isParent':True}

                #dept={'id':d[0], 'pId':d[4], 'name':d[1],'isParent':True}
                data.append(dept)

        else:
            departments = department_service.get_children_by_parent_id(self.get_current_user().get('Fmerchant_id'),_id)
            for d in departments:
                dept={'id':d.Fid, 'pId':d.Fdepartment_father, 'name':d.Fname}
                data.append(dept)
            #departments = department_service.get_dpt_list(self.get_current_user().get('Fmerchant_id'))
        self.write(ujson.dumps(data))

class DepartmentStaffers(BaseHandler):
    '''
    根据部门ID获取员工
    '''
    @tornado.web.authenticated
    def get(self,department_id):
        staffer_service = StafferServices(self.db)
        staffes = staffer_service.get_staffers_by_department_id(self.get_current_user().get('Fmerchant_id'),department_id)
        data=[]
        for s in staffes:
            data.append({'id':s.Fid,'name':s.Fname})
        self.write(ujson.dumps(data))
