#encoding:utf-8
__author__ = 'binpo'

from models.schedule_do import SchedulePlan,ScheduleAttentionTemplate,OrdersSchedule,ShotScheduleCategory
from models.staffer_do import Staffers
from services.base_services import BaseService
from utils.datetime_util import datetime_format,get_month_last_day,getdayofday,get_month_first_day,get_month_day
import datetime
from conf.order_conf import _SCHEDULE_REMINDER_MSG
from conf.merchant import _MERCHANG_DEPARTMENT_TITLES
from sqlalchemy import between,select
from models.order_do import EvaluationCategory,OrderEvaluation,Orders,EvaluationImages

class ScheduleService(BaseService):

    def get_merchant_schedule_plan(self,merchant_id,month=None):
        '''
        获取商户档期
        :param merchant_id:
        :return:
        '''
        start_date = datetime.datetime.strptime(month, "%Y-%m")

        start = get_month_first_day(month=start_date.month,year=start_date.year)
        end = datetime_format("%Y-%m-%d",get_month_last_day(month=start_date.month,year=start_date.year))+' 23:59:59'

        return self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,SchedulePlan.Fuser_id==merchant_id,SchedulePlan.Fschedule_day>=start,SchedulePlan.Fschedule_day<=end).order_by('Fschedule_day')

    def get_merchant_schedule_plan_by_month(self,merchant_id,month):

        month_date = datetime.datetime.strptime(month, "%Y-%m")
        start = get_month_first_day(month_date.month)
        end = datetime_format("%Y-%m-%d",get_month_last_day(month_date.month))+' 23:59:59'
        return self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,SchedulePlan.Fuser_id==merchant_id,SchedulePlan.Fschedule_day>=start,SchedulePlan.Fschedule_day<=end).order_by('Fschedule_day')

    def query_month_scheduls(self,merchant_user_id,input_date=None):
        '''
        获取当前一周档期
        :param merchant_user_id:
        :return:
        '''
        sql = "select count(*),date_format(Fdatetime,'%Y-%c-%d')as shot_plan from t_orders_schedule where Fid=2 AND Fmerchant_id={0} AND Fdatetime between '{1}' and '{2}' group by shot_plan"
        #weekend = getdayofday(7)
        if input_date:
            format_date = datetime.datetime.strptime(input_date, "%Y-%m")
            start_date = datetime_format(format="%Y-%m-%d",input_date=format_date)
        else:
            start_date = datetime_format(format="%Y-%m-%d")
        start = start_date+' 00:00:01'
        end = datetime_format("%Y-%m-%d",get_month_last_day())+' 23:59:59'
        result = self.db.execute(sql.format(str(merchant_user_id),start,end))
        return result

    def query_schedule_by_input_time_and_category_ids(self,category_ids,merchant_id,start,end):
        '''
        :todo 根据时间和类型查询档期
        :param merchant_id:
        :param start:
        :param end:
        :param category:
        :return:
        '''
        if len(end)<=10:
            end=end+' 23:59:59'
        index=1
        query_start_date = datetime.datetime.strptime(start,'%Y-%m-%d')
        start_date,end_date = datetime.datetime.strptime(start,'%Y-%m-%d'),datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        results = self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,
                                               SchedulePlan.Fuser_id==merchant_id,
                                               SchedulePlan.Fschedule_day>=query_start_date,SchedulePlan.Fschedule_day<=end_date)#.scalar()
        if category_ids:
            results = results.filter(SchedulePlan.Fschedule_category_id.in_(category_ids))

        if category_ids:
            #if results.count()-1!=(end_date-start_date).days:
            while True:
                for category_id in category_ids:
                    schedule_plan = self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,
                                                   SchedulePlan.Fuser_id==merchant_id,
                                                   SchedulePlan.Fschedule_category_id==category_id,
                                                   SchedulePlan.Fschedule_day==start_date).scalar()
                    if not schedule_plan:
                        schedule = SchedulePlan()
                        schedule.Fuser_id = merchant_id
                        schedule.Fschedule_category_id = category_id
                        schedule.Ftotal_per_day = 0
                        schedule.Fschedule_day = start_date
                        self.db.add(schedule)
                        self.db.commit()
                start_date = query_start_date+datetime.timedelta(days=index)
                index+=1
                if start_date>end_date:
                    break
        return results.order_by('Fschedule_day')



    def query_schedule_by_input_time_and_category(self,category_id,merchant_id,start,end):
        '''
        :todo 根据时间和类型查询档期
        :param merchant_id:
        :param start:
        :param end:
        :param category:
        :return:
        '''
        if len(end)<=10:
            end=end+' 23:59:59'
        index=1
        query_start_date = datetime.datetime.strptime(start,'%Y-%m-%d')
        start_date,end_date = datetime.datetime.strptime(start,'%Y-%m-%d'),datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')
        results = self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,
                                               SchedulePlan.Fuser_id==merchant_id,
                                               SchedulePlan.Fschedule_day>=query_start_date,SchedulePlan.Fschedule_day<=end_date)#.scalar()
        if category_id:
            results = results.filter(SchedulePlan.Fschedule_category_id==category_id)

        if category_id:
            if results.count()-1!=(end_date-start_date).days:
                while True:
                    schedule_plan = self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,
                                                       SchedulePlan.Fuser_id==merchant_id,
                                                       SchedulePlan.Fschedule_category_id==category_id,
                                                       SchedulePlan.Fschedule_day==start_date).scalar()
                    if not schedule_plan:
                        schedule = SchedulePlan()
                        schedule.Fuser_id = merchant_id
                        schedule.Fschedule_category_id = category_id
                        schedule.Ftotal_per_day = 0
                        schedule.Fschedule_day = start_date
                        self.db.add(schedule)
                        self.db.commit()
                    start_date = query_start_date+datetime.timedelta(days=index)
                    index+=1
                    if start_date>end_date:
                        break
        return results.order_by('Fschedule_day')


        # query_sql = 'select * from t_schedule_plan where Fschedule_category_id=%s and Fuser_id=%s and Fschedule_day between "%s" and "%s"'
        # _query_sql = query_sql%(str(category_id),str(merchant_id),start,end)
        # results = self.db.execute(_query_sql).fetchall()
        # if len(results)＝＝0:

    def query_available_schedule_by_input_time_and_category(self,category_id,merchant_id,start,end):
        '''
        :todo 查询可用排期
        :param category_id:
        :param merchant_id:
        :param start:
        :param end:
        :return:
        '''
        if len(end)<=10:
            end=end+' 23:59:59'
        query_start_date = datetime.datetime.strptime(start,'%Y-%m-%d')
        start_date,end_date = datetime.datetime.strptime(start,'%Y-%m-%d'),datetime.datetime.strptime(end,'%Y-%m-%d %H:%M:%S')

        results = self.db.query(SchedulePlan.Fschedule_day,SchedulePlan.Ftotal_per_day).filter(SchedulePlan.Fdeleted==0,
                                               SchedulePlan.Fuser_id==merchant_id,
                                               SchedulePlan.Fschedule_category_id==category_id,
                                               SchedulePlan.Fschedule_day>=query_start_date,SchedulePlan.Fschedule_day<=end_date)#.scalar()

        schedule_sql ='select count(*),Fshot_date from t_orders_schedule where Fmerchant_id={0} and Fschedule_category_id={1} group by Fshot_date;'
        #print 'results.count()',results.count()
        if results.count()==0:
            return []
        else:
            '''
            根据时间查询可用排期
            '''
            exist_schedules = self.db.execute(schedule_sql.format(str(merchant_id),str(category_id))).fetchall()

            # for d in exist_schedules:
            #     print d[0], d[1]
            available_schedules=[]
            for r in results:
                _exist_=False
                for d in exist_schedules:
                    if r[0]==d[1]:
                        _exist_ = True
                        if r[1]>d[0]:
                            available_schedules.append((r[0],r[1],r[1]-d[0]))
                        else:
                            available_schedules.append((r[0],r[1],r[1]))
                        #exist_schedules.pop(d)
                        break
                if not _exist_:
                    available_schedules.append((r[0],r[1],r[1]))
            return available_schedules

    def query_avalible_schedule_by_day_and_category(self,category_id,merchant_id,start,end):
        pass


    def query_input_date_schedule(self,merchant_id,month):

        start_date = datetime.datetime.strptime(month, "%Y-%m")
        result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        if not result.count():
            ok,message = self.create_schedule_plan(merchant_id,start_date.month,0)
            result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        return result

    def __query_input_date_schedule(self,merchant_id,month):
        '''
        :todo 废弃
        :param merchant_id:
        :param month:
        :return:
        '''
        start_date = datetime.datetime.strptime(month, "%Y-%m")
        result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        if not result.count():
            ok,message = self.create_schedule_plan(merchant_id,start_date.month,0)
            # print 'ok,message:',ok,message
            result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        return result

    def __query_input_date_schedule(self,merchant_id,month):
        '''
        :todo 废弃
        :param merchant_id:
        :param month:
        :return:
        '''
        # sql = "select count(*),date_format(Fdatetime,'%Y-%c-%d')as shot_plan from t_orders_schedule where Fid=2 AND Fmerchant_id={0} AND Fdatetime between '{1}' and '{2}' group by shot_plan"
        # #weekend = getdayofday(7)
        #start_date = datetime_format(format="%Y-%m",input_date=month)
        start_date = datetime.datetime.strptime(month, "%Y-%m")

        # start = start_date+' 00:00:01'
        # end = datetime_format("%Y-%m-%d",get_month_last_day())+' 23:59:59'
        # result = self.db.execute(sql.format(str(merchant_id),start,end))
        result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        #result = self.query_month_scheduls(merchant_id,month)
        # print 'result.count:',result.count()
        # print 'start_date.month',start_date.month
        if not result.count():
            ok,message = self.create_schedule_plan(merchant_id,start_date.month,0)
            # print 'ok,message:',ok,message
            result = self.get_merchant_schedule_plan_by_month(merchant_id,month)
        return result

    def create_schedule_plan(self,merchant_id,month,times):
        '''
        创建档期计划
        :param merchant_id:
        :param month:
        :param times:
        :return:
        '''
        today = datetime.datetime.today()
        set_month = datetime.datetime.today()

        # this_start_date = datetime_format(format="%Y-%m-%d")
        # this_date_end = datetime_format("%Y-%m-%d",get_month_last_day())+' 23:59:59'
        # print this_start_date,this_date_end
        # if int(month)<today.month:
        #     return False,'月份选择错误'

        #start_date = datetime_format(format="%Y-%m-%d",input_date=set_month)
        start = get_month_first_day(int(month))
        end = datetime_format("%Y-%m-%d",get_month_last_day(month))+' 23:59:59'
        #print 'start_date,end',start_date,end
        schedules = self.db.query(SchedulePlan).filter(SchedulePlan.Fdeleted==0,SchedulePlan.Fuser_id==merchant_id,
                                                       SchedulePlan.Fschedule_day>=start,SchedulePlan.Fschedule_day<=end)
        if schedules.count()>0:
            for schedule in schedules:
                schedule.Ftotal_per_day=times
                self.db.add(schedule)
            self.db.commit()
        else:
            for num in xrange((get_month_last_day(int(month))-get_month_first_day(int(month))).days+1):
                schedule = SchedulePlan()
                schedule.Fuser_id = merchant_id
                schedule.Ftotal_per_day = times
                schedule.Fschedule_day = get_month_day(get_month_first_day(int(month)),num)
                self.db.add(schedule)
            self.db.commit()
        return True,'ok'

    def update_schedule_by_schedule_id(self,order_id,**kwargs):
        '''
        todo:更新排期
        :param order_id:排期所对应的订单id
        :param kwargs:
        :return:
        '''
        i = 0
        try:
            query = self.db.query(OrdersSchedule).filter(OrdersSchedule.Fdeleted == 0,OrdersSchedule.Forder_id == order_id)
            for order_schedule in query.all():
                # import pdb
                # pdb.set_trace()
                data = {}
                data['Fnotified_num'] = 0
                data['Fdatetime'] = kwargs.get('sch_date_'+str(i),'')
                data['Fshot_date'] = kwargs.get('sch_date_'+str(i)).split(' ')[0]
                data['Fsite'] = kwargs.get('sch_site_'+str(i),'')
                data['Fuid_stf'] = kwargs.get('sch_uid_stf_'+str(i),'')
                if '$' in kwargs.get('sch_uid_stf_'+str(i)):
                    lst_uid_stf = kwargs.get('sch_uid_stf_'+str(i)).split('$')
                    stf_name_1 = self.db.query(Staffers).filter(Staffers.Fid == lst_uid_stf[0]).scalar().Fname
                    stf_name_2 = self.db.query(Staffers).filter(Staffers.Fid == lst_uid_stf[1]).scalar().Fname
                    data['Fname_stf'] = stf_name_1+'$'+stf_name_2
                else:
                    data['Fname_stf'] = self.db.query(Staffers).filter(Staffers.Fid == kwargs.get('sch_uid_stf_'+str(i))).scalar().Fname
                if '$' in kwargs.get('sch_title_stf_'+str(i)):
                    lstdata = kwargs.get('sch_title_stf_'+str(i)).split('$')
                    stf_title_1 = _MERCHANG_DEPARTMENT_TITLES[int(lstdata[0])]
                    stf_title_2 = _MERCHANG_DEPARTMENT_TITLES[int(lstdata[1])]
                    data['Ftitle_stf'] = stf_title_1+'$'+stf_title_2
                else:
                    data['Ftitle_stf'] = _MERCHANG_DEPARTMENT_TITLES[int(kwargs.get('sch_title_stf_'+str(i)))]
                data['Freminder'] = kwargs.get('sch_reminder_'+str(i),'')
                order_schedule.set_attrs2(self.db,order_schedule.Fid,order_id,**data)
                i+=1
        except Exception,e:
            print e


    def get_oneday_plan(self,merchant_id,input_date,schedule_category_id = None):
        if schedule_category_id:
            sql = "select count(*) from t_orders_schedule where Fid=1 and Fmerchant_id={0} AND Fshot_date='{1}' AND Fschedule_category_id={2}"
            result = self.db.execute(sql.format(str(merchant_id),input_date,int(schedule_category_id)))
        else:
            sql = "select count(*) from t_orders_schedule where Fid=1 and Fmerchant_id={0} AND Fshot_date='{1}'"
            result = self.db.execute(sql.format(str(merchant_id),input_date))
        # #weekend = getdayofday(7)
        # start_date = datetime_format(format="%Y-%m-%d")
        # start = start_date+' 00:00:01'
        # end = datetime_format("%Y-%m-%d",get_month_last_day())+' 23:59:59'
        # print result,'result--'
        # for r in result:
        #     print r
        if result:
            for r in result:
                return r[0]
                break
        return 0
    #select count(*),date_format(Fdatetime,'%Y-%c-%d') as plan from t_orders_schedule where Fid=1 AND Fmerchant_id=1 AND Fdatetime between '2015-02-10 00:00:01' and '2015-02-28 23:59:59' group by shot_plan

    def get_attention_by_mct_id(self,uid_mct):
        query = self.db.query(ScheduleAttentionTemplate).\
            filter(ScheduleAttentionTemplate.Fdeleted == 0,ScheduleAttentionTemplate.Fmerchant_id == uid_mct)
        return query

    def update_attention(self,user_id,schedule_type,lstdata):
        # import pdb
        # pdb.set_trace()
        i = 0
        for lst in lstdata:
            query = self.db.query(ScheduleAttentionTemplate).\
                filter(ScheduleAttentionTemplate.Fdeleted == 0,ScheduleAttentionTemplate.Fmerchant_id == user_id,
                       ScheduleAttentionTemplate.Fschedule_type_id == i)
            #print query.Fdescription
            data = {}
            data['Fdescription'] = lst
            query.update(data)
            self.db.commit()
            i+=1

    def create_order_schedule(self,order_id,user_id):
        # order_schedule = OrdersSchedule()
        # order_schedule.Forder_id = order_id
        # order_schedule.Fmerchant_id = user_id
        schedule_attentions = self.db.query(ScheduleAttentionTemplate).\
            filter(ScheduleAttentionTemplate.Fdeleted == 0,ScheduleAttentionTemplate.Fmerchant_id == user_id)
        if schedule_attentions and schedule_attentions.count()>0:
            for schedule_attention in schedule_attentions:
                order_schedule = OrdersSchedule()
                order_schedule.Fid = schedule_attention.Fschedule_type_id
                order_schedule.Forder_id = order_id
                order_schedule.Fmerchant_id = user_id
                order_schedule.Freminder = schedule_attention.Fdescription
                self.db.add(order_schedule)
                self.db.commit()
        else:
            i = 0
            for reminder in _SCHEDULE_REMINDER_MSG:
                order_schedule = OrdersSchedule()
                order_schedule.Fid = i
                order_schedule.Forder_id = order_id
                order_schedule.Fmerchant_id = user_id
                order_schedule.Freminder = _SCHEDULE_REMINDER_MSG[i]
                self.db.add(order_schedule)
                self.db.commit()
                i+=1



    def update_schedules(self,merchant_id,ids,count):
        '''
        更新档期数量
        :param ids:
        :param count:
        :return:
        '''
        self.db.query(SchedulePlan).filter(SchedulePlan.Fuser_id==merchant_id,SchedulePlan.Fid.in_(ids)).update({'Ftotal_per_day':int(count)},synchronize_session=False)
        self.db.commit()

    def create_schedule_category(self,**kwargs):
        '''
        todo:新增档期分类
        :param kwargs: 参数
        :return:
        '''
        schedule_category = ShotScheduleCategory()
        schedule_category.Fmerchant_id = kwargs.get('uid_mct','')
        schedule_category.Fname = kwargs.get('schedule_category_name','')
        self.db.add(schedule_category)
        self.db.commit()

    def query_schedule_category(self,uid_mct):
        '''
        todo:根据商家id查询档期分类
        :param uid_mct: 商户id
        :return:
        '''
        query = self.db.query(ShotScheduleCategory).\
            filter(ShotScheduleCategory.Fdeleted == 0,ShotScheduleCategory.Fmerchant_id == uid_mct).order_by('Fcreate_time desc')
        return query

    def query_default_category(self,uid_mct,category_id=None):
        '''
        todo:根据商家id查询档期分类
        :param uid_mct: 商户id
        :return:
        '''
        query = self.db.query(ShotScheduleCategory).\
            filter(ShotScheduleCategory.Fdeleted == 0,ShotScheduleCategory.Fmerchant_id == uid_mct)#.order_by('Fcreate_time desc')

        if category_id:
            query = query.filter(ShotScheduleCategory.Fid==category_id)
        return query

    def query_schedule_category_by_id(self,merchant_id,sc_id):
        '''
        todo:根据id查询档期分类
        :param sc_id: 档期分类id
        :return:
        '''
        if sc_id:
            return self.db.query(ShotScheduleCategory).\
                filter(ShotScheduleCategory.Fdeleted == 0,ShotScheduleCategory.Fmerchant_id==merchant_id,ShotScheduleCategory.Fid == sc_id).scalar()
        return None

    def update_schedule_category(self,sc_id,**kwargs):
        '''
        todo:更新档期分类
        :param sc_id: 档期分类id
        :param kwargs: 更新参数
        :return:
        '''
        query = self.db.query(ShotScheduleCategory).filter(ShotScheduleCategory.Fdeleted == 0,ShotScheduleCategory.Fid == sc_id)
        data = {}
        data['Fname'] = kwargs.get('schedule_category_name','')
        query.update(data)
        self.db.commit()

    def delete_schedule_category(self,sc_id):
        '''
        todo:删除档期分类
        :param sc_id: 档期分类id
        :return:
        '''
        query = self.db.query(ShotScheduleCategory).filter(ShotScheduleCategory.Fdeleted == 0,ShotScheduleCategory.Fid == sc_id)
        data = {}
        data['Fdeleted'] = 1
        query.update(data)
        self.db.commit()

    def get_schedule_plan_by_day(self,uid_mct,schedule_category_id,schedule_day):
        '''
        todo:获取给定日期的档期
        :param uid_mct:商户id
        :param schedule_category_id:档期分类
        :param schedule_day:给定时间
        :return:
        '''
        result = self.db.query(SchedulePlan).\
            filter(SchedulePlan.Fuser_id == uid_mct,SchedulePlan.Fschedule_category_id == schedule_category_id,
                   SchedulePlan.Fschedule_day == schedule_day,SchedulePlan.Fdeleted == 0).scalar()
        if result:
            return result
        else:
            return 0

    def get_order_schedule_by_id(self,order_schedule_id):
        '''
        todo:废弃
        :param order_schedule_id:
        :return:
        '''
        return self.db.query(OrdersSchedule).filter(OrdersSchedule.Fdeleted == 0,OrdersSchedule.id == order_schedule_id).scalar()

    def update_order_schedule(self,order_schedule_id,type_id,uid_mct,**kwargs):
        '''
        todo:更新每一条的排期
        :param order_schedule_id:排期id
        :param type_id:排期类型
        :param uid_mct:商户id
        :param kwargs:
        :return:
        '''
        query = self.db.query(OrdersSchedule).\
            filter(OrdersSchedule.Fdeleted == 0,OrdersSchedule.id == order_schedule_id,
                   OrdersSchedule.Fid == type_id,OrdersSchedule.Fmerchant_id == uid_mct)
        query.update(kwargs)
        self.db.commit()

    def get_order_schedule(self,order_schedule_id,type_id,uid_mct):
        '''
        todo:获取单个类型排期
        :param order_schedule_id:排期id
        :param type_id:排期类型
        :param uid_mct:商户id
        :return:
        '''
        return self.db.query(OrdersSchedule)\
            .filter(OrdersSchedule.Fdeleted == 0,OrdersSchedule.id == order_schedule_id,
                    OrdersSchedule.Fid == type_id,OrdersSchedule.Fmerchant_id == uid_mct).scalar()

    def get_order_schedule_by_order_id(self,order_id,type_id):
        '''
        todo:根据订单ID和类型ID获取单个排气
        :param order_id:
        :param type_id:
        :return:
        '''
        return self.db.query(OrdersSchedule).\
            filter(OrdersSchedule.Fdeleted == 0,
                   OrdersSchedule.Fid == type_id,OrdersSchedule.Forder_id == order_id).scalar()


    def get_evaluation_by_typeCode(self,schedule_type_code):
        '''
        todo:根据排期类型id获取评论分类
        :param schedule_type_id:档期id
        :return:
        '''
        return self.db.query(EvaluationCategory).\
            filter(EvaluationCategory.Fdeleted == 0,EvaluationCategory.Fschedule_type_id == int(schedule_type_code))

    def create_order_evaluation(self,**kwargs):
        '''
        todo:创建用户评价
        :param kwargs:
        :return:
        '''
        merchant_id = self.db.query(Orders.Fuid_mct).filter(Orders.Fdeleted == 0,Orders.Fid == kwargs.get('order_id')).scalar()
        order_evaluation = OrderEvaluation()
        order_evaluation.Fuser_id = int(kwargs.get('user_id',''))
        order_evaluation.Fmerchant_id = merchant_id
        order_evaluation.Fcategory_name = kwargs.get('category_name','')
        order_evaluation.Forder_id = int(kwargs.get('order_id',''))
        order_evaluation.Fscore = kwargs.get('Fscore','')
        order_evaluation.Fcontent = kwargs.get('Fcontent','')
        order_evaluation.Fstaffer_name = kwargs.get('staffer_name','')
        order_evaluation.Fschedule_type_code = kwargs.get('schedule_type_code','')
        self.db.add(order_evaluation)
        self.db.commit()
        return order_evaluation

    def create_evaluation_images(self,evaluation_id,url):
        '''
        todo:创建评价图片
        :param evaluation_id:
        :param url:
        :return:
        '''
        image = EvaluationImages()
        image.Forder_evaluation_id = evaluation_id
        image.Fimg_url = url
        self.db.add(image)
        self.db.commit()



    def query_order_evaluations(self,**kwargs):
        '''
        todo:获取评价信息
        :return:
        '''
        query = self.db.query(OrderEvaluation).filter(OrderEvaluation.Fdeleted == 0)
        if kwargs.get('id'):
            query = query.filter(OrderEvaluation.Fid == kwargs.get('id'))
        if kwargs.get('order_id'):
            query = query.filter(OrderEvaluation.Forder_id == kwargs.get('order_id'))
        if kwargs.get('schedule_type_code') or kwargs.get('schedule_type_code') == 0:
            query = query.filter(OrderEvaluation.Fschedule_type_code == kwargs.get('schedule_type_code'))
        return query

    def update_order_evaluation(self,order_evaluation_id,**kwargs):
        '''
        todo:更新评价
        :param order_evaluation_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(OrderEvaluation).filter(OrderEvaluation.Fdeleted == 0,OrderEvaluation.Fid == order_evaluation_id)
        query.update(kwargs)
        self.db.commit()

    def get_evaluation_images(self,evaluation_id):
        '''
        todo:获取评价图片
        :param evaluation_id:
        :return:
        '''
        query = self.db.query(EvaluationImages).\
            filter(EvaluationImages.Fdeleted == 0,EvaluationImages.Forder_evaluation_id == evaluation_id)
        return query




