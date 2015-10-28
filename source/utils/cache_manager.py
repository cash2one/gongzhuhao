#encoding:utf-8
__author__ = 'binpo'

import redis
import sys
from setting import REDIS_HOST,REDIS_PORT,MEMCACHE_HOST,OCS_ACCESS_URL,OCS_ACCESS_ID,OCS_ACCESS_PASS

import logging
import traceback
from utils.singleton import Singleton
DEFAULT_EXPIRY = 60 * 60 * 24

class RedisManaher(object):

    def __init__(self):
        print "Redis connection start.........."
        self.host = REDIS_HOST#'localhost'
        self.port = REDIS_PORT#6379
        self.pool = redis.ConnectionPool(host=self.host, port=self.port)
        self.r = redis.Redis(connection_pool=self.pool)

    def cache_con(self):
        return self.r

    def get_pool(self):
        return self.pool

class MemcacheManager(Singleton):

    def __init__(self):
        try:
            import bmemcached
            #,,OCS_ACCESS_PASS
            self.client = bmemcached.Client((OCS_ACCESS_URL),OCS_ACCESS_ID,OCS_ACCESS_PASS)
            self.client.set('cache_conn','OK')
            if not self.client.get('cache_conn') or self.client.get('cache_conn')!='OK':
                raise
            print 'aliyun ocs is connection...'
        except Exception:
            try:
                import memcache
                self.client = memcache.Client([MEMCACHE_HOST])
                print 'local memcache is connection...'
            except Exception:
                e = sys.exc_info()[0](traceback.format_exc())


    def get_conn(self):
        return self.client

if __name__=='__main__':
    # client = MemcacheManager().client
    #
    # print client
    # print client.get('cache_conn')

    # print dir(client)
    # # print client.stats()
    # print client.set('key', 'value11111111111')
    # print client.get('key')
    # rcache = RedisManaher()
    # p = rcache.cache_con()
    # #p.get('decoration_help')
    # # print dir(rcache.r)
    # # print type(rcache.r.set)
    # # print type(p)
    # # print dir(p)
    # # p.set('key','value')
    # # #print rcache.r.get('key')
    # # print p.get('index_role_cache_name')
    # # reg key:ip_reg
    # # common/image_code/login  key:ip_log
    # #
    pool = redis.ConnectionPool(host='10.251.253.241',port=6379)
    # # import ujson
    # # data=[(10L, 10L, u'http://zenmez.oss-cn-hangzhou.aliyuncs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/clock-desc-d.png', u'http://zenmez.oss-cn-hangzhou.aliyuncs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/clock-desc-d.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/002\u526f\u672c2.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/002.png', 1L, None), (8L, 8L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/001.png', 1L, None), (4L, 4L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/2.jpg', 1L, None), (4L, 4L, None, u'http://image.python-libs.com/album/member/508d4265-4e71-3170-b247-2369ea589ba6/\u9ed8\u8ba4\u76f8\u518c/3.jpg', 1L, None)]
    # #
    # # client.set('preend',ujson.dumps(data),126)
    # # dd = client.get('preend')
    # # print dd
    # # client.set('key','value)
    # # print client.get('key')
    # '''
    # ['RESPONSE_CALLBACKS', '__class__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__format__', '__getattribute__',
    # '__getitem__', '__hash__', '__init__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__',
    # '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_use_lua_lock', '_zaggregate', 'append', 'bgrewriteaof', 'bgsave', 'bitcount',
    # 'bitop', 'bitpos', 'blpop', 'brpop', 'brpoplpush', 'client_getname', 'client_kill', 'client_list', 'client_setname', 'config_get',
    # 'config_resetstat', 'config_rewrite', 'config_set', 'connection_pool', 'dbsize', 'debug_object', 'decr', 'delete', 'dump', 'echo',
    # 'eval', 'evalsha', 'execute_command', 'exists', 'expire', 'expireat', 'flushall', 'flushdb', 'from_url', 'get', 'getbit', 'getrange',
    # 'getset', 'hdel', 'hexists', 'hget', 'hgetall', 'hincrby', 'hincrbyfloat', 'hkeys', 'hlen', 'hmget', 'hmset', 'hscan', 'hscan_iter',
    # 'hset', 'hsetnx', 'hvals', 'incr', 'incrby', 'incrbyfloat', 'info', 'keys', 'lastsave', 'lindex', 'linsert', 'llen', 'lock', 'lpop',
    # 'lpush', 'lpushx', 'lrange', 'lrem', 'lset', 'ltrim', 'mget', 'move', 'mset', 'msetnx', 'object', 'parse_response', 'persist',
    # 'pexpire', 'pexpireat', 'pfadd', 'pfcount', 'pfmerge', 'ping', 'pipeline', 'psetex', 'pttl', 'publish', 'pubsub', 'randomkey',
    # 'register_script', 'rename', 'renamenx', 'response_callbacks', 'restore', 'rpop', 'rpoplpush', 'rpush', 'rpushx', 'sadd', 'save',
    # 'scan', 'scan_iter', 'scard', 'script_exists', 'script_flush', 'script_kill', 'script_load', 'sdiff', 'sdiffstore', 'sentinel',
    # 'sentinel_get_master_addr_by_name', 'sentinel_master', 'sentinel_masters', 'sentinel_monitor', 'sentinel_remove', 'sentinel_sentinels',
    # 'sentinel_set', 'sentinel_slaves', 'set', 'set_response_callback', 'setbit', 'setex', 'setnx', 'setrange', 'shutdown', 'sinter',
    # 'sinterstore', 'sismember', 'slaveof', 'slowlog_get', 'slowlog_len', 'slowlog_reset', 'smembers', 'smove', 'sort', 'spop', 'srandmember',
    # 'srem', 'sscan', 'sscan_iter', 'strlen', 'substr', 'sunion', 'sunionstore', 'time', 'transaction', 'ttl', 'type', 'unwatch', 'watch',
    # 'zadd', 'zcard', 'zcount', 'zincrby', 'zinterstore', 'zlexcount', 'zrange', 'zrangebylex', 'zrangebyscore', 'zrank', 'zrem',
    # 'zremrangebylex', 'zremrangebyrank', 'zremrangebyscore',
    # 'zrevrange', 'zrevrangebyscore', 'zrevrank', 'zscan', 'zscan_iter', 'zscore', 'zunionstore']
    # '''
    # #print dir(p)
    # product = {'1':100}
    # daries = [1,2,3,4,5]
    # p.set('dairy',daries)
    # print type(p.get('dairy')),p.get('dairy')
    # print 'exist',p.exists('dairy')
    # print 'exist',p.exists('dairies')

    # p.set('product',product)
    # print type(p.get('product')),p.get('product')
    # p.setex('product',3600,product)
    # print type(p.get('product')),p.get('product')

    # from utils.cache_manager import SimpleCache
    # from libs.redis_cache.rediscache import cache_it
    # cache = SimpleCache()
    # print dir(cache)
    # print cache.connection