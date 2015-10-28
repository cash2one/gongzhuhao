#!/usr/bin/env python2.7
#encoding:utf-8
from __future__ import absolute_import

from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app
from utils.cache_manager import RedisManaher

from utils.redis_cache import RedisUtils
import datetime
from utils.datetime_util import datetime_format
ru = RedisUtils()
#锦囊、日记、案例、优惠、店铺、问答
# rcache =  RedisManaher().cache_con()

#锦囊, 日记, 案例, 优惠 , 问答
table_names=['t_user_photos_share','t_topics']

@app.task(base=DatabaseTasks)
def update_view_count():
    try:
        for name in table_names:
            cache_tables = update_view_count.rcache.hgetall(name)
            if cache_tables:
                for key,count in cache_tables.items():
                    count_sql = 'select Fpage_view from {0} where Fid={1}'
                    update_sql = 'update {0} set Fpage_view={2} where Fid={1}'
                    object_id = int(key)
                    results = update_view_count.db.execute(count_sql.format(name,object_id)).scalar()
                    if not results:
                        update_view_count.db.execute(update_sql.format(name,object_id,int(count)))
                    else:
                        update_view_count.db.execute(update_sql.format(name,object_id,int(results)+int(count)))
                    update_view_count.db.commit()
            update_view_count.rcache.delete(name)
    except:
        try:update_view_count.db.close()
        except:pass
    finally:
        try:update_view_count.db.close()
        except:pass


#总回复数据/评论数
reply_topic_tables=['t_topics']

@app.task(base=DatabaseTasks)
def update_reply_count():
    try:
        for name in reply_topic_tables:
            cache_name = name+'_count_reply'
            print 'cache_name',cache_name
            cache_tables = update_reply_count.rcache.hgetall(cache_name)
            #Ftotal_assess= Column(Integer,default=0)                #评论数
            #Fpraise = Column(Integer,default=0)                     #点赞数

            if cache_tables:
                for key,count in cache_tables.items():
                    count_sql = 'select Ftotal_assess from {0} where Fid={1}'
                    update_sql = 'update {0} set Ftotal_assess={2} where Fid={1}'
                    object_id = int(key)
                    results = update_reply_count.db.execute(count_sql.format(name,object_id)).scalar()
                    if not results:
                        update_reply_count.db.execute(update_sql.format(name,object_id,count))
                    else:
                        update_reply_count.db.execute(update_sql.format(name,object_id,int(results)+int(count)))
            update_reply_count.db.commit()
            update_reply_count.rcache.delete(cache_name)
    except:
        try:update_reply_count.db.close()
        except:pass
    finally:
        try:update_reply_count.db.close()
        except:pass

#大板块的浏览数
@app.task(base=DatabaseTasks)
def update_topic_category_views():
    try:
        category_sql = 'select Fid from t_topic_category'
        sum_sql = 'update t_topic_category set Fpage_view=(select sum(Fpage_view) from t_topics where Fcotegory_id={0}) where Fid={1}'
        for c_id in update_topic_category_views.db.execute(category_sql):
            update_topic_category_views.db.execute(sum_sql.format(str(c_id[0]),str(c_id[0])))
        update_topic_category_views.db.commit()
    except:
        try:update_topic_category_views.db.close()
        except:pass
    finally:
        try:update_topic_category_views.db.close()
        except:pass

@app.task(base=DatabaseTasks)
def update_order_status():
    n = datetime.datetime.now()
    y = n-datetime.timedelta(hours=1)
    start = datetime_format(n)
    end = datetime_format(y)
    update_order_sql = 'update t_orders set Fstatus=2 where Fstatus!=2 and Fid in (select Forder_id from t_orders_schedule where Fid=4 and Fdatetime between %s and %s)'
    update_order_status.db.execute(update_order_sql%(start,end))
    update_order_status.db.commit()


from models.order_do import Orders
from models.schedule_do import OrdersSchedule

# @app.task(base=DatabaseTasks)
#def order_schedule_backup():
    #order
    #档期
    #


# @app.task(base=DatabaseTasks)
# def send_shot_notify():
#     #end_shot_notify.db.query(OrdersSchedule).filter(OrdersSchedule.Fshot_date==)
#     orders_schedules = send_shot_notify.db.query(OrdersSchedule).filter(OrdersSchedule.Fdeleted==0,OrdersSchedule.Fshot_date==datetime_format('%Y-%m-%d',datetime.datetime.now()+ datetime.timedelta(days=1)))
#     template = WEIXIN_TEMPLATES.get('shot_confirm')
#     page_cache = PageDataCache()
#     access_token = page_cache.get_access_token(setting.WX_GZH_AppID, setting.WX_GZH_AppSecret)
#
#     for o in orders_schedules:
#         user = send_shot_notify.db.query(Users).filter(Users.Fdeleted==0,Users.Fid==o.Fcustomer_id,Users.Forder_id==o.Fid).scalar()
#         send_msg_to_owner(access_token,
#                                   user.Fweixin,
#                                   template.get('jsonText'),
#                                   link=str('http://m.gongzhuhao.com/mobile/schedule/detail/'+str(o.Forder_id)+'/'),
#                                   template_id=template.get('TEMPLATE_ID'),
#                                   first=str('尊敬的{0}，您在“{1}”拍摄照片时间如下:'.format(user.Fnick_name,'')),
#                                   keyword1=str(_SCHEDULE_TYPE[o.Fid]),
#                                   keyword2=datetime_format(o.Fdatetime),
#                                   keyword3=str(o.Fsite),
#                                   remark='祝您在拍摄期间心情愉快，准备的详情信息请点击‘详情’')
#
#         # 王先生，您好，您明天的拍摄服务信息如下
#         # 拍摄事项：试衣
#         # 服务时间：2015-1-1 10
#         # 服务地点：上海市人民南路9号2楼
#         # 祝您在拍摄期间心情愉快，准备的详情信息请点击‘详情’