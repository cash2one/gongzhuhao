#encoding:utf-8
__author__ = 'binpo'


class CommonMemCache(object):
    '''
        通用memcache类
    '''
    def __init__(self,client=None):
        self.client=None

    def set_cache_client(self,client):
        self.client = client

    def delete_key(self,key):
        if self.client.get(key):
            self.client.delete(key)

    def set_cache(self,key,data,expire=60*60*24):
        '''
            设置缓存数据
        '''
        self.client.set(key,data,expire)


class CommonRedisCache(object):
    '''
        通用rediscache
    '''
    def __init__(self,client=None):
        self.client = client

    def set_redis_client(self,client):
        if not self.client:
            self.client = client
