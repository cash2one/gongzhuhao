# encoding:utf-8

from services.base_services import BaseService
from models.staffer_do import Department, Staffers
from utils.error_util import Error

class DepartmentService(BaseService):
    def get_dpt_list(self, uid_mct):
        dpt_entities = (
            Department.Fid,
            Department.Fname,
            Department.Fdepartment_level,
            Department.Ffull_department_name,
            Department.Fdepartment_father
            )
        return self.db.query(*dpt_entities).filter(
            Department.Fuid_mct == uid_mct,
            Department.Fdeleted == 0)

    def check_user_dpt(self, uid_mct, dpt_id):
        return self.db.query(Department).filter(
            Department.Fuid_mct == uid_mct,
            Department.Fid == dpt_id,
            Department.Fdeleted == 0).scalar()

    def get_dpt_by_id(self, uid_mct, depart_id):
        return self.db.query(Department).filter(Department.Fuid_mct == uid_mct,
            Department.Fid == depart_id, Department.Fdeleted == 0).first()

    def get_dpt_by_father_id(self, uid_mct, father_depart_id=None):
        '''
        根据父id查找父部门
        :param uid_mct:
        :param father_depart_id:
        :return:
        '''
        query = self.db.query(Department).filter(Department.Fuid_mct == uid_mct, Department.Fdeleted == 0)

        if father_depart_id:
            query = query.filter(Department.Fdepartment_father==father_depart_id)

        return query.all()

    def get_dpt_by_level(self, uid_mct, level):
        '''
        根据level查找部门
        :param uid_mct:
        :param father_depart_id:
        :return:
        '''
        query = self.db.query(Department).filter(Department.Fuid_mct == uid_mct, Department.Fdepartment_level == level, Department.Fdeleted == 0)

        return query.all()

    def get_child_dpts(self, uid_mct, depart_full_id):
        '''
        根据当前全路径id，查找所有子部门
        :param uid_mct:
        :param depart_id:
        :return:
        '''
        return self.db.query(Department).filter(Department.Fuid_mct == uid_mct, Department.Fdeleted == 0,
            Department.Ffull_departm_id.like(depart_full_id+'/%')).all()

    def get_children_by_parent_id(self,uid_mct, parent_id):
        '''
        :todo 获取子节点
        :param uid_mct:
        :param parent_id:
        :return:
        '''
        return self.db.query(Department).filter(Department.Fdeleted == 0,Department.Fuid_mct==uid_mct,Department.Fdepartment_father==parent_id)


    def get_dpt_list_by_id(self, uid_mct, depart_id=None):
        query = self.db.query(Department).filter(
            Department.Fuid_mct == uid_mct,
            Department.Fdeleted == 0)

        if depart_id:
            cur_dept = self.get_dpt_by_id(depart_id)
            query = query.filter(Department.Ffull_department_name.like("/" + cur_dept.Ffull_department_name))

        return query.all()

    def _check_owner(self, uid_mct, pre_id):
        return self.db.query(Department).filter(
            Department.Fid == pre_id,
            Department.Fuid_mct == uid_mct,
            Department.Fdeleted == 0).scalar()

    def add_dpt(self, uid_mct, name, pre_id):
        if pre_id == -1:    #根
            dpt = Department()
            dpt.Fuid_mct = uid_mct
            dpt.Fname = name
            dpt.Ffull_department_name = '/' + name
            dpt.Fdepartment_level = 0
            #dpt.Fdepartment_father = pre_id
            self.db.add(dpt)
            self.db.commit()

        else:
            pre_full_id = ""
            pre_full_name = ""
            if int(pre_id) != 0:  # not top dpt
                father_dept = self._check_owner(uid_mct, pre_id)
                pre_full_id = father_dept.Ffull_departm_id
                pre_full_name = father_dept.Ffull_department_name
                if not pre_full_id or not pre_full_name:
                    raise Error(1, 'pre_id not belong this uid')
            dpt = Department()
            dpt.Fuid_mct = uid_mct
            dpt.Fname = name
            dpt.Ffull_department_name = pre_full_name + '/' + name
            dpt.Fdepartment_level = pre_full_name.count('/')
            dpt.Fdepartment_father = pre_id
            self.db.add(dpt)
            self.db.commit()

            self.update_dpt(uid_mct, dpt.Fid, Ffull_departm_id=pre_full_id + '/' + str(dpt.Fid))

        return dpt

    def update_dpt(self, uid_mct, dpt_id, **kargs):
        '''
         :更新部门
        '''
        query=self.db.query(Department).filter(Department.Fid==dpt_id, Department.Fuid_mct==uid_mct,Department.Fdeleted==0)
        query.update(kargs)

        self.db.commit()

class DeleteServices(BaseService):
    def _check_have_leaf(self, uid_mct, dpt_id):
        dpts = self.db.query(Department.Fid).filter(
            Department.Fdepartment_father == dpt_id,
            Department.Fuid_mct == uid_mct,
            Department.Fdeleted == 0).all()
        if len(dpts) > 0:
            raise Error(1, "删除失败，请先删除子部门！")

    def _check_have_stfs(self, uid_mct, dpt_id):
        stfs = self.db.query(Staffers.Fid).filter(
            Staffers.Fdepartment_id == dpt_id,
            Staffers.Fuid_mct == uid_mct,
            Staffers.Fdeleted == 0).all()
        if len(stfs) > 0:
            raise Error(1, "删除失败，请先删除部门员工！")

    def delete_dpt(self, uid_mct, dpt_id):
        self._check_have_leaf(uid_mct, dpt_id)
        self._check_have_stfs(uid_mct, dpt_id)

        dpt = {"Fdeleted": 1}
        self.db.query(Department).filter(
            Department.Fid == dpt_id,
            Department.Fuid_mct == uid_mct,
            Department.Fdeleted == 0).update(dpt)
        self.db.commit()
