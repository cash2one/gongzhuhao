#encoding:utf-8

from utils.cache_manager import RedisManaher
import cPickle as pickle
import logging as log

cache_mgr = RedisManaher()
r = cache_mgr.cache_con()

class RedisUtils(object):

    def __init__(self):
        self.r = r

    def set_value(self, key, value,expire=None):
        if expire:
            self.r.set(key, pickle.dumps(value),expire)
        else:
            self.r.set(key, pickle.dumps(value))

    def get_value(self,key):
        pickled_value = self.r.get(key)
        if pickled_value is None:
            return None
        return pickle.loads(pickled_value)


def set_value(redis, key, value):
    redis.set(key, pickle.dumps(value))


def get_value(redis, key):
    pickled_value = redis.get(key)
    if pickled_value is None:
        return None
    return pickle.loads(pickled_value)



class CacheEntry(object):

    def __init__(self,cache_item):
        self.cache_item = cache_item

def refresh_simple_cache(con=r, key='', expire_time=3*60, name_space='cache_default'):
    pass
def simpleCache(con=r, key='', expire_time=3*60, name_space='cache_default'):
    """
    An simple object cache wrap
    """
    def wrap(func):
        def func_wrapper(*args, **kwargs):
            if not kwargs.has_key('key'):
                if args or kwargs:
                    key = make_cache_key(name_space, args, kwargs)
                else:
                    raise 'Can not find cache key'
            cache_value = r.get(key)
            if cache_value:
                print 'success cached, for key : %s' % key
                cacheEntry = pickle.loads(cache_value)
                return cacheEntry.cache_item
            res = func(*args, **kwargs)
            if not res:
                log.error("result is none ,can't cached")
                return
            cacheEntry = CacheEntry(res)
            con.set(key, pickle.dumps(cacheEntry))
            con.expire(key, expire_time)
            return res
        return func_wrapper
    return wrap


def objectCache(con=r, key='', expire_time=3*60, name_space='cache_default'):
    """
    An simple object cache wrap
    """
    def wrap(func):
        def func_wrapper(*args, **kwargs):
            if not kwargs.has_key('key'):
                if args or kwargs:
                    key = make_object_cache_key(name_space, args, kwargs)
                else:
                    raise 'Can not find cache key'
            cache_value = r.get(key)
            #print r,type(r),'-----------cache data-----------'
            if cache_value:
                print 'success cached, for key : %s' % key
                cacheEntry = pickle.loads(cache_value)
                return cacheEntry.cache_item
            res = func(*args, **kwargs)
            if not res:
                log.error("result is none ,can't cached")
                return
            cacheEntry = CacheEntry(res)
            if cacheEntry:
                con.set(key, pickle.dumps(cacheEntry))
                con.expire(key, expire_time)
            return res
        return func_wrapper
    return wrap


def make_cache_key(name_space, *args, **kwargs):
    """
    default cache key make
    """
    key = ''
    key_make = lambda x, y: str(x) + '_' + str(y)
    if args and kwargs:
        key1 = reduce(key_make, args[1:])
        key2 = reduce(key_make, kwargs.values())
        key = key1 + key2
    if args and not kwargs:
        key = reduce(key_make, args[1:])
    if kwargs:
        key = reduce(key_make, kwargs.values())
    return '%s_%s' % (name_space, key)


def make_object_cache_key(name_space, *args, **kwargs):
    """
    default cache key make
    """
    key = ''
    key_make = lambda x, y: str(x) + '_' + str(y)
    if args and kwargs:
        key1 = reduce(key_make, args[0][1:])
        key2 = reduce(key_make, kwargs.values())
        key = key1 + key2
    if args and not kwargs:
        key = reduce(key_make, args[0][1:])
    if kwargs:
        key = reduce(key_make, kwargs.values())
    return '%s_%s' % (name_space, key)


# class Friend():
#     def __init__(self, name):
#         self.name = name
#
#
#     def __str__(self):
#         return self.name
#
# @simpleCache(con=r, expire_time=1*60)

if __name__=='__main__':
    re = RedisUtils()
    print re.get_value('decoration_help')



    cache_mgr = RedisManaher()
    r = cache_mgr.cache_con()
    re = r
    a = re.hset('mytable','1','wawaaa')
    b = re.hget('mytable', '1')
    a = re.hset('mytable', 2, 2222)
    c = re.hget('mytable',2)
    print a
    print b
    print c
    print type(c)
    c = re.hgetall('mytable')
    print c
    c = re.hget('mytable', 5)
    print c
    print 's'



    # re.set_value('product',{'1':10,'2':200})
    # d = re.get_value('product')
    # print type(d)
    # print d.get('1')
    #
    # re.set_value('list',[1,2,3,4,5,6,7,8,9])
    # print re.get_value('list')
    # print type(re.get_value('list'))