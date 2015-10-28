#encoding:utf-8
__author__ = 'morichounami'

from services.base_services import *
from models.user_do import *

class RoleServices(BaseService):
    @classmethod
    def role_format(cls,db,role_codes):
        if role_codes:
            role = db.query(Roles.Fname).filter(Roles.Fcode.in_(role_codes.split(','))) #取出所有结果集行,Roles.Fname代表一个结果集行
            return ','.join([r.Fname for r in role])
        else:
            return ''

