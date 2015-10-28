#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from models.staffer_do import Department

class LevelOneDepartmentHandler(AdminBaseHandler):
    def get(self,merchant_id):
        query = self.db.query(Department).\
            filter(Department.Fdeleted == 0,Department.Fuid_mct == merchant_id,Department.Fdepartment_level == 1)
        page_data = self.get_page_data(query)
        self.echo('ops/company/department_list.html',{'page_data':page_data,'page_html':page_data.render_page_html()})



class DepartmentChildHandler(AdminBaseHandler):
    def get(self,merchant_id,dept_id,dept_level):
        query = self.db.query(Department).\
            filter(Department.Fuid_mct == merchant_id,
                   Department.Fdepartment_father == dept_id,Department.Fdepartment_level == int(dept_level)+1)
        page_data = self.get_page_data(query)
        self.echo('ops/company/department_list.html',{'page_data':page_data,'page_html':page_data.render_page_html()})


def get_child_dept(self,merchant_id,dept_id):
        query = self.db.query(Department).\
            filter(Department.Fdeleted == 0,Department.Fdepartment_father == dept_id,Department.Fuid_mct == merchant_id)
        return query