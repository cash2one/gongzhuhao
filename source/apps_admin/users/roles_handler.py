#encoding:utf-8
__author__ = 'binpo'

from common.base import AdminBaseHandler
from models.user_do import *
import tornado.web

class RolesHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self,*args,**kargs):
        self.echo('ops/users/roles.html',{'roles':Roles.get_all(self.db)})

class MerchantPermissionHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self):
        permissions = self.db.query(Permission).filter(Permission.Fdeleted == 0)
        self.echo('ops/users/permission.html',{'permissions':permissions})
