#encoding:utf-8
__author__ = 'binpo'

from ..base_services import BaseService
from models.app_do import AppVersion

class AppsServices(BaseService):

    def create_apps_version(self,files,qdict):

        '''
            data['error']=is_ok
            data['message']=message
            data['url']=request_url
        '''
        #print qdict
        #if not files.get('error'):
        app_version = AppVersion()
        app_version.app_type = qdict.get('apps_type')
        # app_version.ttid = qdict.get('')
        app_version.app_version = qdict.get('version')
        app_version.app_url = files.get('url')
        app_version.file_name = files.get('file_name')
        app_version.app_size = files.get('size')
        app_version.app_desc = qdict.get('desc')
        self.db.add(app_version)
        self.db.commit()
        return app_version
        #return False

    def query_all(self):
        return self.db.query(AppVersion).order_by('gmt_created desc')