__author__ = 'morichounami'
from staffers_handler import CHandlerStaffersAdd, CHandlerStaffersList,\
    CHandlerStaffersEdit, CHandlerStaffersDelete

handlers = [
    (r'/merchant/staffers/', CHandlerStaffersList),
    (r'/merchant/staffers/([\d]{1,8})/', CHandlerStaffersList),

    (r'/merchant/staffers/add/', CHandlerStaffersAdd),
    (r'/merchant/staffers/edit/([\d]{1,8})/', CHandlerStaffersEdit),
    (r'/merchant/staffers/delete/([\d]{1,8})/', CHandlerStaffersDelete),
]
