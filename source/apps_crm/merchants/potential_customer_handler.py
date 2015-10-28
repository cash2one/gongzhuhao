#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseHandler
from services.potential_customer.potential_customer_services import PotentialCustomerServices
from common.permission_control import company_permission_control
import tornado
import ujson

pc_services = PotentialCustomerServices()
from tornado import template

get_content_filed = template.Template(u'''<table class="table table-striped table-bordered bootstrap-datatable">
                <thead>
                    <tr>
                        <th class="ml-avatar">回访时间</th>
                        <th class="ml-mobile">意向</th>
                        <th class="ml-group">备注</th>
                        <th class="ml-lastlogin">回访人</th>
                    </tr>
                </thead>

                <tbody>
                    {%for v in visit_info%}
                    <tr>

                        <td class="ml-group">
                            {{v.Fcreate_time}}
                        </td>
                        <td class="ml-group">
                        {{v.Fintention}}
                        </td>
                        <td class="ml-lastlogin">
                        {{v.Fdesc}}
                        </td>
                        <td class="ml-role">
                        {{v.Fvistor}}
                        </td>

                    </tr>
                    {%end%}
                </tbody>
                </table>
    ''')


class PotentialCustomerQuery(BaseHandler):
    #潜客查看
    @tornado.web.authenticated
    @company_permission_control('potential_view')
    def get(self, *args, **kwargs):
        print 'potential_customer_query','hello world'
        pc_services.set_db(self.db)
        query = pc_services.query_potential_customer_list(self.get_current_user().get('Fmerchant_id'))
        page_data = self.get_page_data(query)
        page_html = page_data.render_page_html()
        self.echo('crm/potentialcustomer/_list.html',{'page_data':page_data,'page_html':page_html},layout='crm/common/base.html')

    def post(self, *args, **kwargs):
        pass


class PotentialCustomerVisitorQuery(BaseHandler):
    #潜客回访
    @tornado.web.authenticated
    @company_permission_control('potential_return')
    def get(self,pid, *args, **kwargs):

        pc_services.set_db(self.db)
        visit_info = pc_services.query_potential_customer_visits(self.get_current_user().get('Fmerchant_id'),pid)
        try:
            html = get_content_filed.generate(visit_info=visit_info)
        except:
            html=''
        self.write(html)

class PotentialCustomerVisitorCreate(BaseHandler):
    #潜客添加
    @tornado.web.authenticated
    def post(self,*args, **kwargs):
        data={'status':'ok','info':'添加成功'}
        pc_services.set_db(self.db)
        self.get_paras_dict()
        print self.qdict,':self.qdict'
        # is_access	3
        # potential_customer_id	2
        # remark	wqwq
        # visitor_user	qwqw

        try:
            pc_services.create_potential_customer_visits(self.get_current_user().get('Fmerchant_id'),**self.qdict)
        except Exception,e:
            data={'status':'error','info':'添加失败:'+e.message}

        self.write(ujson.dumps(data))

