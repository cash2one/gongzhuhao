
#encoding:utf-8
__author__ = 'binpo'
from tornado.options import define, options
import tornado
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from utils.cache_manager import RedisManaher

mysql_engine = create_engine(options.ENGINE,encoding="utf-8",echo =False)
#mysql_engine = create_engine('mysql://root:111111@192.168.88.151:3306/decorate?charset=utf8',encoding = "utf-8",echo =True)



from utils.redis_cache import RedisUtils
ru = RedisUtils()
#锦囊、日记、案例、优惠、店铺、问答
rcache =  RedisManaher().cache_con()


#锦囊, 日记, 案例, 优惠 , 问答 
table_names=['UserPhotosShare']

class RewriteCacheDataToTable(object):

    def __init__(self):
        pass

    def update_data(self,table,object_id,count):
        try:
            Session = sessionmaker(bind=mysql_engine)
            session = Session()
            count_sql = 'select Fpage_view from {0} where Fid={1}'
            update_sql = 'update {0} set Fpage_view={2} where Fid={1}'
            results = session.execute(count_sql.format(table,object_id)).scalar()
            if not results:
                session.execute(update_sql.format(table,object_id,count))
            else:
                session.execute(update_sql.format(table,object_id,results+count))
            session.commit()
            session.close()
        except:
            try:session.close()
            except:pass
        finally:
            try:session.close()
            except:pass
        #session.query(eval(table)).filter_by(id=object_id)

    def count_cache_data(self):
        print table_names
        for name in table_names:
            cache_tables = rcache.hgetall(name)
            if cache_tables:
                for key,count in cache_tables.items() :
                    # print key,count
                    self.update_data(name,int(key),int(count))
                rcache.delete(name)
#
# if __name__=="__main__":
#     # rcache.hset('decoration_help', '1', '100')
#     # rcache.delete('product')
#     # print     rcache.get('product')
#
#     rcache.hset('product', '3', '100')
#     # print '------'
#     cache_tables = rcache.hgetall('product')
#     print cache_tables
#
#     # test = RewriteCacheDataToTable()
#     # test.count_cache_data()
    # for name in table_names:
    #     print ru.get_value(name)
    # sched.daemonic = False
# sched.add_cron_job(job_function,day_of_week='mon-fri', hour='*', minute='0-59',second='*/5')