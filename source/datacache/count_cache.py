#encoding:utf-8
__author__ = 'binpo'

from utils.cache_manager import RedisManaher
import threading
from celery_tasks.tasks_cache import cache_view_set,count_reply_set,count_category_topics_set
rcache =  RedisManaher().cache_con()

def cache_views(table_name,object_id,count=0,session=None):
    cache_view_set.apply_async(args=[table_name, object_id,count])

def cache_replys(table_name,object_id,count=0,session=None):
    count_reply_set.apply_async(args=[table_name, object_id,count])

def count_category_tipics(table_name,object_id,count=0):
    count_category_topics_set
    # cdc = CountDataCache(table_name,object_id,session)
    # cdc.start()

# from utils.redis_cache import RedisUtils
# ru = RedisUtils()


class CountDataCache(threading.Thread):
    '''
        :param table_name:
        :param object_id:
        :return:
    '''
    def __init__(self,table_name,object_id,session=None):

        threading.Thread.__init__(self)
        self.table_name = table_name
        self.object_id = object_id
        self.session = session

    def run(self):
        '''  异步存储 存放缓存 '''
        count = rcache.hget(self.table_name, self.object_id)
        rcache.hset(self.table_name, self.object_id, int(count)+1 if count else 1)

        view_count = rcache.hget(self.table_name+'_v',self.object_id)
        if view_count:
            rcache.hset(self.table_name+'_v', self.object_id, int(view_count)+1)

        # try:
        #     count_sql = 'select view_times from {0} where id={1}'
        #     update_sql = 'update {0} set view_times={2} where id={1}'
        #     #print count_sql.format(table,object_id)
        #     #print count_sql,update_sql
        #     results = self.session.execute(count_sql.format(table,object_id)).scalar()
        #     #print dir(results)
        #     print results
        #     print update_sql.format(table,object_id,view_count[0]+count)
        #     if not results:
        #         self.session.execute(update_sql.format(table,object_id,count))
        #     else:
        #         self.session.execute(update_sql.format(table,object_id,results+count))
        # except:
        #     pass

        #print rcache.hget('decoration_help',1)

        # if ru.r.exists(self.table_name):
        #     count_data = ru.get_value(self.table_name)
        #     #if count_data:
        #     if count_data.has_key(str(self.object_id)):
        #         count_data[str(self.object_id)] = count_data[str(self.object_id)]+1
        #     else:
        #         count_data[str(self.object_id)]=1
        #     ru.set_value(self.table_name,count_data)
        # else:
        #     data={str(self.object_id):1}
        #     ru.set_value(self.table_name,data)

# def cache_views(table_name,object_id):
#     cdc = CountDataCache(table_name,object_id)
# #     cdc.start()
# if __name__ == '__main__':
#     # rcache.delete('decoration_help')
#     # for l in range(10):
#     #     cache_views('decoration_help', l)
#     rcache.hset('decoration_help',1,10,5)
#
#     import time
#     time.sleep(10)
#     rcache.hget('decoration_help',1)






