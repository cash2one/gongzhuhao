#encoding:utf-8
__author__ = 'wangjinkuan'

from common.cache_base import CacheBaseHandler
from apps_mobile.mobile_base import MobileBaseHandler
from services.work.work_services import WorkServices
from services.company.company_services import CompanyServices
from models.company_do import Company
from models.location_do import Area
from conf.work_conf import _WORK_STYLE_WX,_SHOOTING_SCENE_WX,PAGE_SIZE,_WORK_STYLE_APP,_SHOOTING_SCENE_APP,PAGE_SIZE_APP,WORK_KEYS
import sys
import ujson

work_service = WorkServices()
company_service = CompanyServices()


class WorksHandler(MobileBaseHandler,CacheBaseHandler):

    def get(self,page=1,merchant_id=0):
        '''
        todo:作品列表
        :param page:页码
        :return:
        '''
        work_service.set_db(self.db)
        company_service.set_db(self.db)
        if int(page) < 1:
            page = 1
        try:
            self.get_paras_dict()
            if merchant_id and int(merchant_id):
                self.qdict['merchant_id'] = merchant_id
            query = work_service.query_work(**self.qdict)

            if self.request.uri.startswith('/api/json/'):

                works = self.get_page_data(query,page_size=PAGE_SIZE_APP,page=page)

                has_next = self.is_page(works.page_num,page=page)

                lst_work = []
                for work in works.result:
                    work_dict = self.obj_to_dict(work,WORK_KEYS)
                    work_dict['work_company'] = company_service.get_company_by_uid(work.Fmerchant_id).Fcompany_name
                    lst_work.append(work_dict)
                if int(page) > 1:
                    data = {
                            'works':lst_work,
                            'has_next':has_next
                           }
                else:
                    data = {
                            'works':lst_work,
                            'work_style':_WORK_STYLE_APP,
                            'shot_scene':_SHOOTING_SCENE_APP,
                            'has_next':has_next
                           }
                self.write_json({'stat':'ok','data':data,'info':''})
            else:

                works = self.get_page_data(query,page_size=PAGE_SIZE,page=page)

                has_next = self.is_page(works.page_num,page=page)

                if int(page) > 1:
                    return self.others_page(works,has_next,merchant_id)
                else:
                    if merchant_id and int(merchant_id):
                        self.echo('views/merchant/merchant_works_page.html',
                                  {'works':works,
                                   'has_next':has_next,
                                   'merchant_id':merchant_id
                                  },layout='views/merchant/merchant_works.html')
                    else:
                        self.echo('views/work/work_page.html',
                                  {'works':works,
                                   'work_style':_WORK_STYLE_WX,
                                   'work_scene':_SHOOTING_SCENE_WX,
                                   'has_next':has_next,
                                   'work_style_code':self.qdict.get('style',''),
                                   'work_scene_code':self.qdict.get('scene','')
                                  },layout='views/work/works.html')
        except Exception,e:
            pass
            self.echo('views/500.html')

    def others_page(self,works,has_next,merchant_id):
        if merchant_id:
            _html = self.render('views/merchant/merchant_works_page.html',{'works':works})
        else:
            _html = self.render('views/work/work_page.html',{'works':works})
        self.write(ujson.dumps({'html':_html,'has_next':has_next}))

    def get_company(self,merchant_id):
        '''
        todo:获取公司
        :param merchant_id:
        :return:
        '''
        return self.db.query(Company).filter(Company.Fuser_id == merchant_id,Company.Fdeleted == 0).scalar()

class WorkHandler(MobileBaseHandler):

    def get(self,work_id):
        '''
        todo:作品detail
        :param work_id:
        :return:
        '''
        work_service.set_db(self.db)
        company_service.set_db(self.db)
        try:
            work = work_service.query_work(id=work_id).scalar()
            work_images = work_service.get_work_iamges_by_id(work_id)
            company = company_service.get_company_by_uid(work.Fmerchant_id)
            if self.request.uri.startswith('/api/json'):
                images = [image.Furl for image in work_images]
                data = {
                        'company_name':company.Fcompany_name,
                        'work_name':work.Fname,
                        'work_style':work.Fstyle_name,
                        'sale_price':work.Fsale_price,
                        'shot_scene_name':work.Fshot_scene_name,
                        'mode_style_name':work.Fmode_style_name,
                        'Fmerchant_id':work.Fmerchant_id,
                        'work_images':images,
                        'Fid':work.Fid
                        }
                self.write_json({'stat':'ok','data':data,'info':''})
            else:
                data = {
                        'work':work,
                        'work_images':work_images,
                        'company':company
                       }
                url = 'views/work/work.html'
                self.echo(url,data)
        except Exception,e:
            print e.message
            pass
            self.echo('views/500.html')




