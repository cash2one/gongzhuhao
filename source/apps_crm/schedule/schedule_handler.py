#encoding:utf-8
import tornado
from common.base import BaseHandler
from services.orders.orders import ShowServices as OrderShowServices
from services.schedules.schedules import ShowServices, UpdateServices, \
    TemplateServer
from services.staffers.staffer_services import StafferServices
from common.permission_control import company_permission_control
from utils.error_util import Error
from conf.order_conf import _TYPE_ORDER, _SCHEDULE_TYPE
from services.schedules.schedules_service import ScheduleService
import ujson
# from tenjin_base import ym_engine
from tornado import template
from utils.datetime_util import datetime_format
from services.departments.department_services import DepartmentService
from services.orders.order_services import OrderServices
from services.shares.shares_service import ShareServices
from services.users.user_services import UserServices
import datetime
from conf.order_conf import _SCHEDULE_TYPE
from conf.order_conf import _TYPE_ORDER as ORDER_TYPES
from models.staffer_do import *
from models.order_do import *
from conf.msg_conf import WEIXIN_TEMPLATES
from utils.wx_util import send_msg_to_owner
from datacache.datacache import PageDataCache
import setting
import csv,time
import xlwt
user_service = UserServices()
order_serice = OrderServices()
schedule_service = ScheduleService()
share_service = ShareServices()

week_day_dict = {
    0: '星期一',
    1: '星期二',
    2: '星期三',
    3: '星期四',
    4: '星期五',
    5: '星期六',
    6: '星期天',
}
order_schedule_dict = {
            0:'Ffitting_time',
            1:'Fshot_time',
            2:'Fselect_time',
            3:'Fcertain_time',
            4:'Fabtain_time'
        }

get_content_filed = template.Template(u'''
    <table class="table">
    <thead>
        <tr>
            <th width="8%"><a id='download' href="/merchant/schedule/export/{{schedule_category}}/{{start_date}}/{{end_date}}">下载</a> <input type="checkbox" id="all_schedule" name="all_schedule">全选</th>
            <th>日期</th>
            <th>可拍摄量</th>
            <th>已排期量</th>
            <th>可排期量</th>
        </tr>
    </thead>
    <tbody>
        {% for s in schedule_plans %}
                <tr>
                    <td><input type="checkbox" value="{{s.Fid}}" name="schedule_check"></td>
                    <td>{{s.Fschedule_day}}{{s.weekday}}</td>
                    <td>{{s.Ftotal_per_day}}</td>
                    <td>{% raw s.plan_count %}</td>
                    <td>{{s._plan_count}}</td>
                </tr>
        {%end%}
        </tbody>
    </table>
    ''')


_content_filed = template.Template(u'''
    <table class="table">
    <thead>
        <tr>
            <th width="8%"><input type="checkbox" id="all_schedule" name="all_schedule">全选</th>
            <th>日期</th>
            <th>分类</th>
            <th>可拍摄量</th>
            <th>已排期量</th>
            <th>可排期量</th>
        </tr>
    </thead>
    <tbody>
        {% for s in schedule_plans %}
                <tr>
                    <td><input type="checkbox" value="{{s.Fid}}" name="schedule_check"></td>
                    <td>{{s.Fschedule_day}}{{s.weekday}}</td>
                    <td>{{s.category_name}}</td>
                    <td>{{s.Ftotal_per_day}}</td>
                    <td>{% raw s.plan_count %}</td>
                    <td>{{s._plan_count}}</td>
                </tr>
        {%end%}
        </tbody>
    </table>
    ''')
class CHandlerScheduleList(BaseHandler):
    #查看排期 (制定排期和修改)
    @tornado.web.authenticated
    @company_permission_control('schedule_view_edit')
    def get(self, order_id):
        try:
            uid_mct = self.get_current_user().get('Fmerchant_id')

            db_schedule = ShowServices(self.db)
            db_schedule.check_order_owner(uid_mct, order_id)
            schedules = db_schedule.get_schedule(order_id)

            db_staffers = StafferServices(self.db)
            staffers = db_staffers.get_staffers(uid_mct)

            db_site = TemplateServer(self.db)
            sites = db_site.get_site_template(uid_mct)

            department_service = DepartmentService(self.db)
            departments = department_service.get_dpt_list(uid_mct)
            data = []
            for d in departments:
                dept = {'id': d[0], 'pId': d[4] and d[4] or 0, 'name': d[1]}
                data.append(dept)

            db_order = OrderShowServices(self.db)
            db_order.check_order_owner(uid_mct, order_id)
            order, stf = db_order.get_order_info(order_id,uid_mct)
            order.Forder_type_str = _TYPE_ORDER[int(order.Forder_type)]

            schedule_service.set_db(self.db)
            schedule_categorys = schedule_service.query_schedule_category(uid_mct)

            self.echo(
                'crm/order/schedule_list_py.html', {
                    'items': schedules, 'order': order,
                    'order_id': order_id, 'stfs': staffers,
                    'schedule_categorys':schedule_categorys,
                    'sites': sites,
                    'data': data
                    }
                )

        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            self.echo("crm/404.html")

    @tornado.web.authenticated
    def post(self, order_id):
        # self.get_paras_dict()
        # print self.qdict
        self.write('ok')


class CHandlerScheduleUpdate(BaseHandler):
    @tornado.web.authenticated
    def get(self, order_id):
        self.echo('404.html')

    @tornado.web.authenticated
    @company_permission_control('schedule_view_edit')
    def post(self, order_id):
        """更新排期 保存"""
        try:
            kargs = {'items': []}
            kargs['order_id'] = order_id
            kargs['uid_mct'] = self.get_current_user().get('Fmerchant_id')
            for i in range(5):
                p = [
                    "shd_date_", "shd_site_", "shd_tips_",
                    "shd_stff_id_", "shd_stff_tt_", "shd_stff_nm_",
                    "ismodify_"]
                p = [val+str(i) for val in p]
                arg_item = {
                    p[0]: self.check_arg(p[0], u'^[\d: -]{8,28}$', ''),
                    p[1]: self.check_arg(p[1], u'[^|&\'\"\\$;=]{0,128}', ''),
                    p[2]: self.check_arg(p[2], u'[^|&\'\"\\$;=]{0,128}', ''),
                    p[3]: self.check_arg(p[3], u'^[\d|&]{1,16}$', ''),  # 多个stff用|&合并提交
                    p[4]: self.check_arg(p[4], u'^[\u4e00-\u9fa5\w\s|&]{1,64}$', ''),  # 多个stff用|&合并提交
                    p[5]: self.check_arg(p[5], u'^[\u4e00-\u9fa5\w\s|&]{1,64}$', ''),  # 多个stff用|&合并提交
                    p[6]: self.check_arg(p[6], u'^[01]$', '1'),  # 本行是否有修改 必填
                    }
                kargs['items'].append(arg_item)

            db_shd = UpdateServices(self.db)
            db_shd.update_schedule(**kargs)
            self.write(Error(0, 'succ').__dict__)
        except tornado.web.MissingArgumentError, e:
            err_msg = "lack param[%s]" % e.arg_name
            return self.write(Error(1, err_msg).__dict__)
        except Error, e:
            return self.write(e.__dict__)
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise e
            err_msg = "post failed"
            self.write(Error(2, err_msg).__dict__)


class ScheduleOperationHandler(BaseHandler):

    '''查询当月档期'''
    @tornado.web.authenticated
    @company_permission_control('plans_view')
    def get(self, *args, **kwargs):

        date_time = self.get_argument('month_date',None)
        input_category_id = self.get_argument('input_category_id','')

        merchant_id = self.get_current_user().get('Fmerchant_id')
        schedule_service.set_db(self.db)
        if not date_time:
            start_date,end_date = datetime_format("%Y-%m-%d"),datetime_format("%Y-%m-%d",datetime.datetime.now()+datetime.timedelta(days=30))
        else:
            start_date,tmp,end_date = date_time.split()
        if input_category_id:
            try:
                int(input_category_id)
                category = schedule_service.query_default_category(merchant_id,category_id=input_category_id)
            except:
                category = schedule_service.query_default_category(merchant_id)
        else:
            category = schedule_service.query_default_category(merchant_id)
        category_name=""
        category_dict={}
        for c in category:
            category_dict[c.Fid] = c.Fname
        if category:
            category_ids = [c.Fid for c in category]
            if category_ids:
                schedule_plans = schedule_service.query_schedule_by_input_time_and_category_ids(category_ids,merchant_id,start_date,end_date)
            else:
                schedule_plans=[]
                #category_name = category.Fname
        else:
            schedule_plans=None
        schedule_category=schedule_service.query_schedule_category(merchant_id)

        self.echo('crm/schedules/shot_schedule.html',{'input_category_id':input_category_id,'category_dict':category_dict,'category_name':category_name,'schedule_plans':schedule_plans,'start_date':start_date,'end_date':end_date,'week_day_dict':week_day_dict,'schedule_category':schedule_category},layout='crm/common/base.html')

    def get_complete_plan(self,date,count,category_id):
        plan_count = schedule_service.get_oneday_plan(self.get_current_user().get('Fmerchant_id'),date,category_id)
        if plan_count>count:
            return "<p class='red'>%s"%(plan_count),0
        else:
            return plan_count,count-plan_count


class SchedulePlanHandler(BaseHandler):

    '''设置档期'''
    @tornado.web.authenticated
    @company_permission_control('plans_edit')
    def get(self, *args, **kwargs):

        data={'stat':'ok','info':''}
        schedules = self.get_argument('update_schedule_ids',None)
        times = self.get_argument('times',None)
        is_validate = True
        try:
            int(times)
            shedule_ids = [int(sid) for sid in schedules.split(',') if sid ]
            schedule_service.set_db(self.db)
            try:
                schedule_service.update_schedules(self.get_current_user().get('Fmerchant_id'),shedule_ids,times)
            except Exception,e:
                data={'stat':'ok','info':e.message}
        except:
            data={'stat':'ok','info':'档期次数参数设置错误'}

        self.write(ujson.dumps(data))

class UpdateSchedulePlanHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        data={'stat':'ok','info':''}

        self.write(ujson.dumps(data))


class CHandlerTemplateAttention(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        items = tmp_srv.get_attention_msg_template(uid_mct)
        return self.echo(
            'crm/system/attention_py.html',
            {'items': items if items else []},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        param = []
        for i in range(5):
            param.append(self.get_argument("tip%d" % i))
        tmp_srv.update_attention_msg_template(uid_mct, *param)
        self.write(Error(0, 'succ').__dict__)


class CHandlerTemplateSiteUpdate(BaseHandler):
    """更新默认服务地址模板"""
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        items = tmp_srv.get_site_template(uid_mct)
        return self.echo(
            'crm/system/site_py.html',
            {'items': items if items else [],
                '_SCHEDULE_TYPE': _SCHEDULE_TYPE},
            layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        tmp_srv.update_site_template(
            uid_mct,
            Fid=self.get_argument('Fid', '0'),
            Ftype_id=int(self.get_argument('Ftype_id')),
            Fsite=self.get_argument('Fsite')
        )
        self.write(Error(0, 'succ').__dict__)


class CHandlerTemplateSiteSetDefualt(BaseHandler):
    """设置默认服务地址模板"""
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        tmp_srv.set_default_site_template(
            uid_mct,
            Fid=self.get_argument('Fid', '0'),
            Ftype_id=int(self.get_argument('Ftype_id'))
        )
        self.write(Error(0, 'succ').__dict__)


class CHandlerTemplateSiteDelete(BaseHandler):
    """删除服务地址模板"""
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        tmp_srv = TemplateServer(self.db)
        tmp_srv.delete_site_template(
            uid_mct,
            Fid=self.get_argument('Fid', '0')
        )
        self.write(Error(0, 'succ').__dict__)


class ScheduleQueryHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('plans_view')
    def get(self, *args, **kwargs):
        # import pdb
        # pdb.set_trace()

        date_time = self.get_argument('date_time',None)
        category_id = self.get_argument('category',None)
        start,tmp,end = date_time.split()
        schedule_service.set_db(self.db)
        merchant_id = self.get_current_user().get('Fmerchant_id')

        category_dic={}
        if not category_id:
            query = schedule_service.query_default_category(merchant_id)
            for c in query:
                category_dic[str(c.Fid)] = c.Fname
        else:
            category_name = schedule_service.query_schedule_category_by_id(merchant_id,category_id).Fname
            category_dic = {category_id:category_name}
        #results = schedule_service.query_schedule_by_input_time_and_category(category_id,merchant_id,start,end)
        results = schedule_service.query_schedule_by_input_time_and_category_ids(category_dic.keys(),merchant_id,start,end)
        _results=[]
        # if category_id:
        #     category_name = schedule_service.query_schedule_category_by_id(merchant_id,category_id).Fname
        for r in results:
            # if not category_id:
            #     t_category_id = r.Fschedule_category_id
            #     tmp_schedule = schedule_service.query_schedule_category_by_id(merchant_id,t_category_id)
            #     if not tmp_schedule:
            #         continue
            #     else:category_name = tmp_schedule.Fname
            # else:
            #     t_category_id=category_id
            r.category_name = category_dic[str(r.Fschedule_category_id)]
            r.plan_count,r._plan_count = self.get_complete_plan(r.Fschedule_day,r.Ftotal_per_day,r.Fschedule_category_id)
            r.weekday = week_day_dict[r.Fschedule_day.weekday()] #星期几
            _results.append(r)

        html = _content_filed.generate(schedule_plans=_results,category_name='')
        self.write(html)

    def get_complete_plan(self,date,count,input_category_id):
        plan_count = schedule_service.get_oneday_plan(self.get_current_user().get('Fmerchant_id'),date,input_category_id) #一个商户每一天的排期量
        if plan_count>count:
            return "<p class='red'>%s"%(plan_count),0 #如果已排期的数量大于一天可排期的数量，那么剩下排期数量为0
        else:
            return plan_count,count-plan_count


    #     pass
    #
    # def get_week_day(date):
    #     week_day_dict = {
    #         0 : '星期一',
    #         1 : '星期二',
    #         2 : '星期三',
    #         3 : '星期四',
    #         4 : '星期五',
    #         5 : '星期六',
    #         6 : '星期天',
    #     }
    #     day = date.weekday()
    #     return week_day_dict[day]

class ScheduleCategoryAddHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        uid_mct = self.get_current_user().get('Fmerchant_id')
        self.echo('crm/system/schedule_category_create.html',{'uid_mct':uid_mct},layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        rsg = {
            'stat':'error',
            'msg':''
        }
        schedule_service.set_db(self.db)
        self.get_paras_dict()
        schedule_service.create_schedule_category(**self.qdict)
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))

class ScheduleCategoryListHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        schedule_service.set_db(self.db)
        uid_mct = self.get_current_user().get('Fmerchant_id')
        query = schedule_service.query_schedule_category(uid_mct)
        page_data = self.get_page_data(query)
        self.echo('crm/system/schedule_category.html',
                  {'page_data':page_data,'page_html':page_data.render_page_html()},layout='crm/common/base.html')

class ScheduleCategoryEditHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self,sc_id):
        schedule_service.set_db(self.db)
        schedule_category = schedule_service.query_schedule_category_by_id(self.get_current_user().get('Fmerchant_id'),sc_id)
        self.echo('crm/system/schedule_category_edit.html',
                  {'schedule_category':schedule_category},layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self,sc_id):
        self.get_paras_dict()
        self.qdict.pop('_xsrf')
        schedule_service.set_db(self.db)
        schedule_service.update_schedule_category(sc_id,**self.qdict)
        self.write(ujson.dumps({'stat':'success','msg':''}))

class DeleteScheduleCategoryHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self,sc_id):
        schedule_service.set_db(self.db)
        schedule_service.delete_schedule_category(sc_id)
        self.write(ujson.dumps({'stat':'success','msg':''}))


class ScheduleSearchHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        merchant_id = self.get_current_user().get('Fmerchant_id')

        input_date = self.get_argument('input_date',datetime_format(format='%Y-%m-%d'))
        _category = self.get_argument('schedule_categeory',None)
        schedule_type = self.get_argument('schedule_type',0)

        schedule_service.set_db(self.db)
        schedule_category=schedule_service.query_schedule_category(merchant_id)
        query=OrderServices(self.db).query_orders_by_schedule_date(merchant_id,schedule_type,input_date,schedule_category=_category)
        orders = self.get_page_data(query)
        self.echo('crm/schedules/shot_schedule_detail.html',{'ORDER_TYPES':ORDER_TYPES,
                                                             "input_date":input_date,
                                                             "schedule_category":schedule_category,
                                                             'orders':orders,
                                                             '_category':_category,
                                                             'schedule_type':schedule_type,
                                                             'SCHEDULE_TYPE':_SCHEDULE_TYPE},layout='crm/common/base.html')

    def get_order_schedules(self,order_id):
        order_serice.set_db(self.db)
        if order_serice.check_order_permission(self.get_current_user().get('Fmerchant_id'),order_id):
            #query = order_serice.get_schedule_by_order_id(order_id)
            return order_serice.get_schedule_by_order_id(order_id)
        else:
            return []

class OrdersScheduleUpdateHandler(BaseHandler):
    #每条排期更新
    @tornado.web.authenticated
    def get(self):
        pass

    @tornado.web.authenticated
    @company_permission_control('schedule_view_edit')
    def post(self):
        self.get_paras_dict()
        uid_mct = self.get_current_user().get('Fmerchant_id')
        user_id = self.get_current_user().get('Fid')
        order_schedule_id = self.qdict.get('order_schedule_id')
        type_id = self.qdict.get('type_id')
        # if not self.qdict.get('date') or not self.qdict.get('site'):
        #     return self.write(ujson.dumps({'stat':'error','msg':'请填写时间和地点'}))
        arguments = {'date':u'^[\d: -]{8,28}$','site':u'[^|&\'\"\\$;=]{0,128}'}
        # for arg in arguments: #检测时间和地点
        #     is_ok,msg = self.check_arg_2(arg,arguments.get(arg))
        #     if not is_ok:
        #         return self.write(ujson.dumps({'stat':'error','msg':msg}))

        schedule_service.set_db(self.db)
        order_schedule = schedule_service.get_order_schedule(order_schedule_id,type_id,uid_mct)
        data = {}
        data['Foperation_id'] = user_id
        data['Fnotified_num'] = order_schedule.Fnotified_num+1
        data['Fdatetime'] = self.qdict.get('date') and self.qdict.get('date') or None
        data['Fshot_date'] = self.qdict.get('date') and self.qdict.get('date').split(' ')[0] or None
        data['Fsite'] = self.qdict.get('site','')
        data['Fuid_stf'] = self.qdict.get('staffer_1','')
        data['Ftitle_stf'] = self.qdict.get('staffer_title')
        data['Fname_stf'] = self.qdict.get('staffer_name','')
        data['Freminder'] = self.qdict.get('reminder','')
        if type_id == '1': #摄影
            schedule_category_name = self.qdict.get('schedule_category_name')
            if not schedule_category_name:
                return self.write(ujson.dumps({'stat':'error','msg':'请选择档期分类'}))
            is_ok,msg = self.check_arg_2('schedule_category_name',u'^[\u4e00-\u9fa5\w ]{1,64}$')
            if not is_ok:
                return self.write(ujson.dumps({'stat':'error','msg':msg}))
            data['Fschedule_category_id'] = self.qdict.get('schedule_category')
            data['Fschedule_category_name'] = schedule_category_name
            data['Fuid_stf'] += '&'+self.qdict.get('staffer_2','')
            data['Ftitle_stf'] += '&'+self.qdict.get('staffer_title_2')
            data['Fname_stf'] += '&'+self.qdict.get('staffer_name_2','')
            #当没有排期时间、更新的排期时间和原来的排期时间不一致、更新的档期分类和原来的档期分类不一致时，验证档期
            if not str(order_schedule.Fshot_date) \
                    or str(order_schedule.Fshot_date) != data['Fshot_date'] \
                        or str(order_schedule.Fschedule_category_id) != data['Fschedule_category_id']:
                if data['Fshot_date']:
                    is_ok,msg = self.check_schedule_plan(uid_mct,data['Fshot_date'],data['Fschedule_category_id']) #检测档期
                    if not is_ok:
                        return self.write(ujson.dumps({'stat':'error','msg':msg}))
        schedule_service.update_order_schedule(order_schedule_id,type_id,uid_mct,**data)
        order_id = self.qdict.get('order_id')

        #----------更新订单日期------------
        order_update_param={}
        key = order_schedule_dict[int(type_id)]
        order_update_param[key] = self.qdict.get('date') and self.qdict.get('date') or None
        t_order = _order = self.db.query(Orders).filter(Orders.Fid == order_id,Orders.Fuid_mct==uid_mct)#.scalar()
        order_update_param['Fstatus']=1
        _order.update(order_update_param)
        self.db.commit()

        template = WEIXIN_TEMPLATES.get('shot_confirm')
        page_cache = PageDataCache(self.db)
        access_token = page_cache.get_access_token(setting.WX_GZH_AppID, setting.WX_GZH_AppSecret)

        user_service.set_db(self.db)
        user = user_service.get_user_by_id(order_schedule.Fcustomer_id)
        #access_token,open_id,jsonText,**kargs
        if user:
            '''
            王先生，您好，您明天的拍摄服务信息如下
            拍摄事项：试衣
            服务时间：2015-1-1 10
            服务地点：上海市人民南路9号2楼
            祝您在拍摄期间心情愉快，准备的详情信息请点击‘详情’
            '''

            schedule_name = _SCHEDULE_TYPE[int(type_id)]
            send_msg_to_owner(access_token,
                          user.Fweixin,
                          template.get('jsonText'),
                          link=str('http://m.gongzhuhao.com/mobile/20151985112504291695293/detail/'+str(t_order.scalar().Fid)+'/'+str(type_id)),
                          template_id=template.get('TEMPLATE_ID'),
                          first=str('尊敬的{0}，您在“{1}”的{2}排期时间已经发送给你,详细信息如下:'.format(user.Fnick_name,self.get_current_user().get('Fcompany_name',''),schedule_name)),
                          keyword1=str(schedule_name),
                          keyword2=data['Fdatetime'] and str(data['Fdatetime']) or '待定',
                          keyword3=str(self.qdict.get('site','')),
                          remark='你可以通过点击详情,查看排期信息')

        self.write(ujson.dumps({'stat':'ok','msg':'','notified_num':data['Fnotified_num']}))

    def check_schedule_plan(self,uid_mct,schedule_day,schedule_category_id):
        schedule_day = datetime.datetime.strptime(schedule_day,'%Y-%m-%d')
        schedule_service.set_db(self.db)
        count = schedule_service.get_oneday_plan(uid_mct,schedule_day,schedule_category_id) #已排期
        plan_count = schedule_service.get_schedule_plan_by_day(uid_mct,schedule_category_id,schedule_day) #设置的档期
        if plan_count == 0 or plan_count.Ftotal_per_day == 0:
            return False,'请先设置档期'
        elif plan_count.Ftotal_per_day - count <= 0:
            return False,'已无档期'
        else:
            return True,''

class MerchantWishesHandler(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self):
        share_service.set_db(self.db)
        uid_mct = self.get_current_user().get('Fmerchant_id')
        merchant_wishes = share_service.get_merchant_wishes(uid_mct)
        self.echo('crm/system/merchant_wishes.html',
                  {'merchant_wishes_types':_TYPE_ORDER,'merchant_wishes':merchant_wishes},layout='crm/common/base.html')

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def post(self):
        self.get_paras_dict()
        share_service.set_db(self.db)
        if len(self.qdict.get('Fwishes_content')) > 54:
            return self.write(ujson.dumps({'stat':'error','msg':'祝福不能超过18个字数'}))
        try:
            if not self.qdict.get('merchant_wishes_id'): #新增
                self.qdict['Fuid_mct'] = self.get_current_user().get('Fmerchant_id')
                self.qdict['Foperation_id'] = self.get_current_user().get('Fid')
                share_service.create_merchant_wishes(**self.qdict)
            else: #编辑
                merchant_wishes_id = self.qdict.get('merchant_wishes_id')
                self.qdict.pop('_xsrf')
                self.qdict.pop('merchant_wishes_id')
                share_service.update_merchant_wishes(merchant_wishes_id,**self.qdict)
        except Exception,e:
            if self.settings.get('debug'):
                self.write(str(e.message))
            msg = '添加错误'
            self.write(Error(2, msg).__dict__)
        self.write(ujson.dumps({'stat':'ok','msg':''}))

class DeleteMerchantWishesHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('system_operation')
    def get(self,merchant_wishes_id):
        data = {}
        data['Fdeleted'] = 1
        share_service.set_db(self.db)
        try:
            share_service.update_merchant_wishes(merchant_wishes_id,**data)
        except Exception,e:
            if self.settings.get('debug'):
                self.write(str(e.message))
            return self.write(ujson.dumps({'stat':'error','msg':'删除失败'}))
        self.write(ujson.dumps({'stat':'ok','msg':''}))

class ScheduleExport(BaseHandler):

    @tornado.web.authenticated
    def get(self,category_id,start_date,end_date,**kwargs):
        # category_id = self.get_argument('schedule_categery_id','')
        # start_date = self.get_argument('start_date','')
        # end_date = self.get_argument('end_date','')
        if not category_id or not start_date or not end_date:
            return self.write('<h1>查询参数不全</h1>')
        start_time = datetime.datetime.strptime(start_date,"%Y-%m-%d")
        end_time = datetime.datetime.strptime(end_date,"%Y-%m-%d")

        if (end_time-start_time).days>31:
            return self.write('<h1>只能下载最近一个月的数据</h1>')

            # file_name = 'readme.txt'
            # self.set_header ('Content-Type', 'application/octet-stream')
            # self.set_header ('Content-Disposition', 'attachment; filename='+file_name)
            # with open(file_name, 'rb') as f:
            #     data = f.read('职能查询')
            #     self.write(data)
            # self.finish()

        if len(end_date)<=10:
            end_date = end_date+' 23:59:00'
        merchant_id = self.current_user.get('Fmerchant_id')
        file_name = time.time()+'.csv'
        #dsw_server_data=[]
        schedule_export_sql = 'select Fschedule_category_name,Fshot_date,Fname_stf t_orders_schedule where Fmerchant_id={0} and Fschedule_category_id={1} and Fshot_date between {2} and {3}'
        print 'schedule_export_sql:',schedule_export_sql
        execute_sql = schedule_export_sql.format(merchant_id,category_id,start_date,end_date)
        schedule_data = self.db.execute(execute_sql).fetchall()

        with open(file_name,'wb') as csvfile:
            spamwriter = csv.writer(csvfile)#, delimiter='',quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for d in schedule_data:
                spamwriter.writerow(d)

        # #读取的模式需要根据实际情况进行修改
        # with open(filename, 'rb') as f:
        #     while True:
        #         data = f.read(buf_size)
        #         if not data:
        #             break
        #         self.write(data)
        #记得有finish哦
        self.finish()


class ScheduleExportByType(BaseHandler):

    def get(self,schedule_type,input_date,**kwargs):

        merchant_id = self.current_user.get('Fmerchant_id')
        schedule_service.set_db(self.db)
        orders=OrderServices(self.db).query_orders_by_schedule_date(merchant_id,schedule_type,input_date)
        name = u'档期明细导出'
        type_name = _SCHEDULE_TYPE[int(schedule_type)]
        file_name = datetime_format(format='%Y%m%d%H%M%S')+str(type_name)+u'档期明细导出'+'.xls'
        clumns = (u'订单号码',u'客户姓名',u'客户手机',u'订单类型',u'订单余额',u'订单时间',u'排期时间')
        file = xlwt.Workbook(encoding='utf-8') #注意这里的Workbook首字母是大写，无语吧
        table = file.add_sheet(name)

        table.write_merge(0, 0, 0, 6,name)
        for c in clumns:
            table.write(1,clumns.index(c),c)
        index=2
        for i in xrange(7):
            table.col(i).width = 5000
        for order in orders:
            table.write(index,0,order.Forder_id_user)
            table.write(index,1,order.Fuser_name)
            table.write(index,2,order.Fuser_mobi)
            table.write(index,3,ORDER_TYPES[order.Forder_type])
            table.write(index,4,str(order.Famount))
            table.write(index,5,datetime_format(format='%Y-%m-%d',input_date=order.Fcreate_time))
            table.write(index,6,input_date)

            index+=1
        file.save(file_name)
        self.set_header ('Content-Type', 'application/octet-stream')
        self.set_header ('Content-Disposition', 'attachment; filename='+file_name)
        with open(file_name, 'rb') as f:
            data = f.read()
            self.write(data)
        self.finish()










    

