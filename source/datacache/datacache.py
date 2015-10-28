#encoding:utf-8

__author__ = 'binpo'

from sqlalchemy.orm import sessionmaker
from utils.cache_manager import MemcacheManager
import setting
from utils import wx_util
from utils import common_util
from services.users.user_services import UserServices
import ujson
from services.topics.topic_services import TopicServices

mcache = MemcacheManager().get_conn()

class PageDataCache(object):

    def __init__(self,db=None):
        if db:
            self.db = db
        self.key_func = {
        }

    def set_db(self,engine):
        session_factory = sessionmaker(bind=engine, autoflush=True, autocommit=False)
        self.db = session_factory()

    def refresh_cache(self,key=None):

        '''
        刷新缓存
        :param key: 缓存主键
        :return:异常信息 or 缓存结果
        '''
        if not key:
            return "Key Empty!"
        elif not self.key_func.has_key(key):
            return "Key Not Exists!"
        else:
            pass

        mcache.delete(key)  #清空
        return self.key_func[key]()  #刷新

    def get_access_token(self, app_id, app_secret):
        mcache_key = 'wx_access_token_'+str(app_id)
        access_token = mcache.get(mcache_key)
        if not access_token or access_token == '':
            dic_accessToken = wx_util.getAccessToken(app_id, app_secret)
            if dic_accessToken.has_key('errcode'):
                raise Exception("Get Access Token Error:" + dic_accessToken.get('errmsg'))

            access_token = dic_accessToken.get("access_token")
            mcache.set(mcache_key, access_token, 6600)

            if app_id == setting.WX_GZH_AppID:#怎么装
                #同时刷新ticket
                mcache_key = 'wx_jsapi_ticket'
                dic_jsapi_ticket = wx_util.get_jsapi_ticket(access_token)
                if dic_jsapi_ticket.has_key('errcode') and dic_jsapi_ticket.get('errcode') <> 0:
                    raise Exception("Get jsapi_ticket Error:" + dic_jsapi_ticket.get('errmsg'))

                jsapi_ticket = dic_jsapi_ticket.get("ticket")
                mcache.set(mcache_key, jsapi_ticket, 6600)

        return access_token

    def get_jsapi_ticket(self, access_token):
        mcache_key = 'wx_jsapi_ticket'
        jsapi_ticket = mcache.get(mcache_key)
        if not jsapi_ticket or jsapi_ticket == '':
            dic_jsapi_ticket = wx_util.get_jsapi_ticket(access_token)
            if dic_jsapi_ticket.has_key('errcode') and dic_jsapi_ticket.get('errcode') <> 0:
                raise Exception("Get jsapi_ticket Error:" + dic_jsapi_ticket.get('errmsg'))

            jsapi_ticket = dic_jsapi_ticket.get("ticket")
            mcache.set(mcache_key, jsapi_ticket, 6600)

        return jsapi_ticket



class UserMsgCache(object):

    def __init__(self, db=None):
        self.db = db

    def set_db(self, db):
        self.db = db

    def get_user_msg(self, id):
        '''
        根据用户id获取用户基础信息
        :param id : 用户id
        :return dict  keys: id ,nick ,photo
        '''
        mcache_key = 'user_msg_'+str(id)
        user = mcache.get(mcache_key)
        if not user:
            user_db = UserServices(self.db)
            user = user_db.get_user_cache_msg_by_id(id)
            user = user.__dict__ if user else {}
            if user.has_key('_labels'):
                del user['_labels']
            user = ujson.dumps(user)
            mcache.set(mcache_key, user, 7200)
        return ujson.loads(user)

    def refresh_user_msg(self, id):
        '''
        刷新用户头像缓存
        '''
        mcache_key = 'user_msg_'+str(id)
        mcache.delete(mcache_key)
        self.get_user_msg(id)


class RolePermissionCache(object):

    def __init__(self, db):
        self.db = db

    # def get_role_permission(self, code):
    #     '''
    #     根据用户id获取用户基础信息
    #     :param id : 用户id
    #     :return dict  keys: id ,nick ,photo
    #     '''
    #     mcache_key = 'role_permission_'+str(code)
    #     user = mcache.get(mcache_key)
    #     if user is None:
    #         user_db = UserServices(self.db)
    #         user = user_db.get_permissions_by_role_code(code)
    #         user = zip(*user)[0] if user else []
    #         user = ujson.dumps(user)
    #         mcache.set(mcache_key, user)
    #    return ujson.loads(user)

    def refresh_role_permission(self, code):
        '''
        刷新用户头像缓存
        '''
        mcache_key = 'role_permission_'+str(code)
        mcache.delete(mcache_key)
        self.get_role_permission(code)


class TopicUserSnsCache(object):

    def __init__(self, db=None):
        self.db = db

    def set_db(self, db):
        self.db = db

    def get_user_sns_msg(self, id):
        '''
        根据用户id获取用户基础信息
        :param id : 用户id
        :return dict  keys: id ,nick ,photo
        '''
        mcache_key = 'topic_user_'+str(id)
        user_sns_topic = mcache.get(mcache_key)
        if not user_sns_topic:
            topic_db = TopicServices(self.db)
            user_sns = topic_db.query_user_sns_topic(user_id=id)
            user_sns_topic = {}
            for s in user_sns:
                key = '%s_%s_%s' % (s.Ftopic_id,s.Fsns_type,s.Ftopic_type)
                user_sns_topic[key] = 1
            user_sns_topic = ujson.dumps(user_sns_topic)
            mcache.set(mcache_key, user_sns_topic, 7200)
        return ujson.loads(user_sns_topic)

    def refresh_user_sns_msg(self, id):
        '''
        刷新用户头像缓存
        '''
        mcache_key = 'topic_user_'+str(id)
        mcache.delete(mcache_key)
        self.get_user_sns_msg(id)