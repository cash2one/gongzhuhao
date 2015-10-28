#encoding:utf-8
__author__ = 'binpo'
import xlrd
import time
from models.album_do import *
from models.app_do import *
from models.company_do import *
from models.location_do import *
from models.order_do import *
from models.product_do import *
from models.schedule_do import *
from models.share_do import *
from models.staffer_do import *
from models.user_do import *
from models.topic_do import *

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base
from sqlalchemy import create_engine
mysql_engine = create_engine('mysql://root:1qazxsw2@121.41.100.80:3306/db_gongzhuhao?charset=utf8', encoding='utf-8', echo=False)
Session = sessionmaker(bind=mysql_engine)
session = Session()
from services.users.user_services import UserServices
from utils.random_utils import create_random_passwd

class ExcelDataImport(object):

    def import_orders_from_excel(self):
        data = xlrd.open_workbook('asjr.xls') # 打开demo.xls
        data.sheet_names()        # 获取xls文件中所有sheet的名称
        #table = data.sheets()[0]  # 获取xls文件第一个工作表
        #table = data.sheet_by_index(0)        # 通过索引获取xls文件第0个sheet
        #table = data.sheet_by_name(u'Sheet1') # 通过工作表名获取 sheet
        # 获取行数和列数
        #nrows = table.nrows
        #ncols = table.ncols
        # 获取整行和整列的值（数组）
        #table.row_values(1)
        #table.col_values(1)
        # 循环行,得到索引的列表
        def insert_data(index,merchant_id,table):
            for rownum in range(table.nrows):
                if index<=0:
                    index+=1
                    continue
                #订单号	先生	小姐	先生电话	小姐电话	套系	定金	门市	摄影师	化妆师	备注	档期分类	档期时间
                order = table.row_values(rownum)
                order_id = order[0]
                try:
                    user1,user2 = [order[1],order[3] and str(int(order[3])) or ''],[order[2],order[4] and str(int(order[4])) or '']
                    if not user1[0] and not user2[0]:
                        raise
                    if not user1[1] and not user2[1]:
                        raise
                    if isinstance(order[1],float):
                        raise
                    if isinstance(order[2],float):
                        raise
                except Exception,e:
                    #print e.message,'raise message'
                    print order
                    continue
                try:
                    if not order[5]:
                        amount=0
                    else:
                        amount=int(order[5])
                except Exception,e:
                    #print e.message,'金额'
                    amount=eval(order[5])
                try:
                    if not order[6]:
                        pre_amount=0
                    else:pre_amount = int(order[6])
                except Exception,e:
                    #print e.message,'定金'
                    pre_amount = eval(order[6])

                sign_users = order[7].split('/')
                shot_user = order[8]
                paint_user = order[9]
                remark = order[10]
                schedule_type_name = order[11]
                shot_date = order[12]
                #print order

                _shot_date = None
                import datetime
                #print shot_date,type(shot_date)
                #exit(0)
                if shot_date:
                    _shot_date = datetime.datetime.strptime(shot_date,'%Y/%m/%d')
                if shot_user:
                    _shot_user = session.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==merchant_id,Staffers.Fname==shot_user).scalar()
                else:
                    _shot_user = None
                if paint_user:
                    _paint_user = session.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==merchant_id,Staffers.Fname==paint_user).scalar()
                else:
                    _paint_user = None
                #print '创建用户--------------------------'
                user_phone = user2[1] or user1[1]
                user_name = user2[0] or user1[0]

                ok,user = self.create_user(user_name,user_phone)
                if not ok:
                    print order
                    continue
                #print '创建订单--------------------------'
                order,is_order_exist = self.create_order(user,merchant_id,sign_users,amount,pre_amount,remark,user1,user2,order_id,shot_date)
                #print '加签认---------------------------'
                #self.create_sign_user(order.Fid,merchant_id,sign_users)
                #print '#创建排期-------------------------'
                if is_order_exist:
                    print order.Forder_id_user
                self.create_shcedule(merchant_id,1,order,user,schedule_type_name,shot_date,schedule_type_name,_shot_user,_paint_user)
                #print '创建相册--------------------------'
                ablum_name=''
                if user1[0] and user2[0]:
                    ablum_name='&'.join([user1[0],user2[0]])
                elif user2[0] :
                    ablum_name=user2[0]
                elif user1[0]:
                    ablum_name=user1[0]
                if not is_order_exist:
                    ablum = self.create_ablum(order.Fid, merchant_id, ablum_name)
                    index+=1
                #print index,'-------------------------'

        table = data.sheet_by_index(0)
        index = 0
        merchant_id=7
        insert_data(0,9,data.sheet_by_index(0))

        # index = 0
        # merchant_id=7
        # insert_data(0,9,data.sheet_by_index(0))

            # index +=1;
            # if index>1:
            #     exit(0)


    #--------------创建账号------------------------
    def create_user(self,user_name,mobile):
        user_service = UserServices(session)
        is_ok,info = user_service.registe_check_exist(phone=mobile)
        if not is_ok:
            user = session.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi == mobile).scalar()
            return True,user

        user = Users()
        user.Fuid = user_service.user_uid(user_name=mobile)
        user.Fuser_mobi = mobile
        user.Fnick_name = user_name
        user.Fstatus = 'normal'
        user.Fuser_pwd = user_service.user_passed(create_random_passwd(3),user.Fuid)
        user.is_employee = 0
        user_service.db.add(user)
        user_service.db.commit()
        return True,user

    #--------------创建订单信息-------------
    def create_order(self,user,merchant_id,sign_users,amount,deposit,comment,user1,user2,order_id,shot_date):

        starffs = []
        for name in sign_users:
            starff = session.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==merchant_id,Staffers.Fname==name).first()
            if starff:
                starffs.append(starff)
        if starffs:
            _stfs = '&'.join([str(s.Fid) for s in starffs if s])
        else:_stfs=None
        exist_order = session.query(Orders).filter(Orders.Forder_id_user==order_id).first()
        is_order_exist=False
        if exist_order:
            order = exist_order
            is_order_exist=True
        else:
            order = Orders()
        order.Forder_id = str(user.Fid)+str(int(time.time()*1000))
        order.Forder_id_user = order_id
        order.Fuid = user.Fid       #订单对应的用户ID
        order.Fuid_mct = merchant_id       #订单对应的商户ID
        order.Foperation_id = merchant_id                         #操作人ID
        order.Forder_from = 'apps_crm'        #apps_crm mobile  录入订单
        order.Forder_type = 1 #订单类型

        order.Fuser_name = user2[0]  #用户姓名
        order.Fuser_name_ex = user1[0]  #客户第二姓名（如新郎）
        order.Fuser_mobi = user2[1]  #客户手机号
        order.Fuser_mobi_ex = user1[1] #客户第二手机号

        order.Fuid_stf = _stfs    #商户员工ID 接单人
        order.Famount = amount      #订单金额
        order.Fdeposit = deposit     #订单金额
        if shot_date:
            order.Fstatus = 1     #订单状态 conf.order_conf._ORDERS_STATUS
        else:
            order.Fstatus = 0
        order.Fcomment = comment #备注信息
        session.add(order)
        session.commit()
        return order,is_order_exist

    def create_sign_user(self,order_id,merchant_id,sign_users,operation='add'):
        '''
        :todo 创建接单人
        :param order_id:
        :param staff_id:
        :return:
        '''
        starffs = []
        for name in sign_users:
            starff = session.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==merchant_id,Staffers.Fname==name).first()
            if starff:
                starffs.append(starff)
        _stfs = '&'.join([str(s.Fid) for s in starffs])

        for sid in [str(s.Fid) for s in starffs]:
            staff = session.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fid==sid,Staffers.Fuid_mct==merchant_id).scalar()
            if staff:
                order_sign_user=OrderSignUser()
                order_sign_user.Forder_id = order_id       #订单号(对内) 21位
                order_sign_user.Fstaff_id = staff.Fid
                order_sign_user.Fstaff_name = staff.Fname
                session.add(order_sign_user)
        session.commit()

    #----------创建相册-----------
    def create_ablum(self,order_id, uid_mct, ablum_name,album_type=1):
        abm = Albums()
        abm.Forder_id = order_id
        abm.Fuid_mct = uid_mct
        abm.Fablum_name = ablum_name
        if album_type:
            abm.Falbum_type = album_type
        session.add(abm)
        session.commit()
        return abm

    #-------------创建排期--------------
    def create_shcedule(self,merchant_id,order_type_id,order,user,schedule_type_id,schedule_date,schedule_type_name,_shot_user,_paint_user):

        #获取排期消息模板
        for x in xrange(5):
            schedule_attention = session.query(ScheduleAttentionTemplate).filter(
                    ScheduleAttentionTemplate.Fmerchant_id == merchant_id,
                    ScheduleAttentionTemplate.Fdeleted == 0,
                    ScheduleAttentionTemplate.Fschedule_type_id==x
                    ).first()

            schedule_site = session.query(ScheduleSiteTemplate).filter(
                    ScheduleSiteTemplate.Fmerchant_id == merchant_id,
                    ScheduleSiteTemplate.Fdeleted == 0,
                    ScheduleSiteTemplate.Fisdefault==1,
                    ScheduleSiteTemplate.Fschedule_type_id==x
                    ).first()

            schedule_category = session.query(ShotScheduleCategory).filter(ShotScheduleCategory.Fdeleted==0,ShotScheduleCategory.Fmerchant_id==merchant_id,ShotScheduleCategory.Fname==schedule_type_name).first()
            exist_order_schedule = session.query(OrdersSchedule).filter(OrdersSchedule.Fid==x,OrdersSchedule.Forder_id==order.Fid).scalar()
            if exist_order_schedule:
                order_schedule= exist_order_schedule
            else:order_schedule = OrdersSchedule()
            order_schedule.Fid = x
            order_schedule.Forder_id = order.Fid                   # 对应orders表中的order_id
            order_schedule.Fmerchant_id = merchant_id                                #商户ID
            order_schedule.Fcustomer_id = user.Fid                                #用户ID
            order_schedule.Foperation_id = merchant_id                              #操作人ID
            order_schedule.Fnotified_num = 0                             # 此排期已通知用户次数0未通知
            if schedule_category:
                order_schedule.Fschedule_category_id = schedule_category.Fid         #档期分类id
                order_schedule.Fschedule_category_name = schedule_category.Fname   #档期分类name
            print schedule_date
            if x==1 and schedule_date:
                order_schedule.Fdatetime = schedule_date                                              # 此排期时间
                order_schedule.Fshot_date = schedule_date                                                   # 此排期时间  精确到某一天
                order.Fshot_time = schedule_date
            fuser_ids=''
            Fuser_names=''
            if _shot_user and _paint_user:
                fuser_ids = str(_shot_user.Fid)+'&'+str(_paint_user.Fid)
                Fuser_names = str(_shot_user.Fname)+'&'+str(_paint_user.Fname)
            elif _shot_user and not _paint_user:
                fuser_ids = str(_shot_user.Fid)
                Fuser_names = str(_shot_user.Fname)
            elif not _shot_user and _paint_user:
                fuser_ids = str(_paint_user.Fid)
                Fuser_names = str(_paint_user.Fname)
            else:
                pass
            order_schedule.Fuid_stf = fuser_ids                          # 排期中参与的员工ID
            order_schedule.Fname_stf = Fuser_names                        # 排期中参与的员工姓名
            try:
                if schedule_site:
                    order_schedule.Fsite = schedule_site.Fsite                                          # 服务地点
                if schedule_attention:
                    order_schedule.Freminder = schedule_attention.Fdescription                         # 温馨提示
            except:
                pass

            session.add(order_schedule)
            session.add(order)
            session.commit()



ExcelDataImport().import_orders_from_excel()