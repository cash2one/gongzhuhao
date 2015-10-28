#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from models.company_do import Company
from models.user_do import Users
from models.product_do import WeddingPhotoProduct
from conf.work_conf import _WORK_TYPE,_WORK_STYLE,_SHOOTING_SCENE,_MODE_STYLE,_SHOOTING_SITE,_SHOOTING_SCENE_2
from services.work.work_services import WorkServices
import ujson
import sys

work_service = WorkServices()

class WorksListHandler(AdminBaseHandler):

    def get(self,code=0):
        work_service.set_db(self.db)
        self.get_paras_dict()
        self.qdict['code'] = code
        try:
            query = work_service.query_work(**self.qdict)
            page_data = self.get_page_data(query)
            self.echo('ops/works/works_list.html',
                      {
                        'page_data':page_data,
                        'page_html':page_data.render_page_html(),
                        'work_types':_WORK_TYPE,
                        'code':code
                      })
        except Exception,e:
            print e.message

            self.echo('ops/500.html')

class DeleteWorkHandler(AdminBaseHandler):

    def get(self,work_id):
        rsg = {'stat':'error','msg':''}
        work_service.set_db(self.db)
        try:
            work,work_images = work_service.get_product_by_id(work_id)
            work.Fdeleted = 1
            self.db.add(work)
            for image in work_images:
                image.Fdeleted = 1
                self.db.add(image)
            self.db.commit()
        except Exception,e:
            rsg['msg'] = e.message
            return self.write(ujson.dumps(rsg))
        rsg['stat'] = 'ok'
        self.write(ujson.dumps(rsg))










