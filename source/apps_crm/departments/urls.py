__author__ = 'morichounami'
from departments_handler import *

handlers = [
    (r'/merchant/departments/(\d*)', CHandlerDepartmentsList),
    (r'/merchant/departments/add/', CHandlerDepartmentsAdd),
    (r'/merchant/departments/get/depart/(\d*)', CHandlerGetDepartList),
    (r'/merchant/departments/delete/([\d]{1,8})/', CHandlerDepartmentsDelete),
    (r'/merchant/departments/rename/', CHandlerDepartmentRename),
    (r'/merchant/all/departments/', DepartmentQueryHandler),
    (r'/merchant/department/staffers/([\d]{1,8})', DepartmentStaffers),

]

