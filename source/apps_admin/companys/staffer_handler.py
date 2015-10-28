__author__ = 'frank'

from common.base import AdminBaseHandler
from services.staffers.staffer_services import StafferServices
from conf.merchant import _MERCHANG_DEPARTMENT_TITLES

staffer_service = StafferServices()

class StafferListHandler(AdminBaseHandler):
    def get(self,merchant_id):
        self.get_paras_dict()
        staffer_service.set_db(self.db)
        query = staffer_service.query_staffers(merchant_id = merchant_id,**self.qdict)
        page_data = self.get_page_data(query)
        self.echo('ops/company/staffers_list.html',
                  {'page_data':page_data,'page_html':page_data.render_page_html(),'staffer_title':_MERCHANG_DEPARTMENT_TITLES})

class StafferListByDepartmentHandler(AdminBaseHandler):
    def get(self,merchant_id,dept_id):
        self.get_paras_dict()
        staffer_service.set_db(self.db)
        query = staffer_service.query_staffers(merchant_id,dept_id,**self.qdict)
        page_data = self.get_page_data(query)
        self.echo('ops/company/staffers_list.html',
                  {'page_data':page_data,'page_html':page_data.render_page_html(),'staffer_title':_MERCHANG_DEPARTMENT_TITLES})
