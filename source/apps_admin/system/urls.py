#encoding:utf-8

__author__ = 'binpo'

from ..system.system_handler import SystemIndexHandler,SystemAppsUploadHandler,SystemAppsQueryHandler



'''
    <li id="system_apps"><a href="/admin/system/apps_crm/list">APPS<i class="icon-chevron-right"></i></a>
    </li>

    <li id="system_upload_apps"><a href="/admin/system/apps_crm/upload/">上传发布包<i class="icon-chevron-right"></i></a>
    </li>

'''

handlers=[

        (r'/admin/system/index.html', SystemIndexHandler),
        (r'/admin/system/apps/list.html', SystemAppsQueryHandler),
        (r'/admin/system/apps/upload.html', SystemAppsUploadHandler),

]
