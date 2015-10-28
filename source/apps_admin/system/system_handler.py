#encoding:utf-8
__author__ = 'binpo'

from common.base import AdminBaseHandler

from utils.datetime_util import datetime_format
from setting import *
from utils.upload_utile import upload_to_oss
from tornado.options import options
#import ujson

from services.system.apps_service import AppsServices

app_service = AppsServices()

class SystemIndexHandler(AdminBaseHandler):

    def get(self):
        self.echo('ops/system/index.html')


class SystemAppsUploadHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        self.echo('ops/system/upload_apps.html')

    def post(self, *args, **kwargs):

        self.get_paras_dict()
        #print self.qdict
        #file_metas=self.request.files.get('appszip')       #提取表单中‘name’为‘file’的文件元数据
        data = {}
        size = 0
        try:
            file_prex = 'apps_crm/'+datetime_format(format="%Y%m%d%H%M")
            is_ok,filenames = upload_to_oss(self,options.APPS_BUCKET,param_name='appzip',file_type=None,file_prex=file_prex,is_apps=True)
            if is_ok:
                request_url = filenames[0].get('full_name')
                size = filenames[0].get('size')
            else:
                message = filenames

        except Exception,e:
            data['error']=1
            data['message']=e.message
            data['url']=''

        data['error'] = is_ok
        data['message'] = '发功成功'
        data['url'] = request_url
        data['size'] = size
        data['file_name'] = filenames[0].get('file_name')
        app_service.set_db(self.db)
        app = app_service.create_apps_version(data,self.qdict)
        if app:
            self.write('upload success')
        else:
            self.write('upload fail')

class SystemAppsQueryHandler(AdminBaseHandler):

    def get(self, *args, **kwargs):
        app_service.set_db(self.db)
        apps = app_service.query_all()
        self.echo('ops/system/apps_list.html',
            {'apps':apps}
        )

    def post(self, *args, **kwargs):
        pass
