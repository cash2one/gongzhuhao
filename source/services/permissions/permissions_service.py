#encoding:utf-8
__author__ = 'frank'

from models.user_do import Permission
from services.base_services import BaseService

class PermissionsServices(BaseService):
    def get_permissions(self):
        query = self.db.query(Permission).filter(Permission.Fdeleted == 0)
        return query
