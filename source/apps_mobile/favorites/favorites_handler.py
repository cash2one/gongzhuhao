#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.mobile_base import MobileBaseHandler
from services.favorites.favorites_services import FavoritesService
from common.cache_base import AppCacheHandler
from common.permission_control import Mobile_login_control
import sys
import ujson

favorites_service = FavoritesService()

class FavoritesHandler(MobileBaseHandler,AppCacheHandler):

    @Mobile_login_control()
    def post(self, *args, **kwargs):

        '''
        :param args:
        :param kwargs:
        :param Ffavorites_type:收藏类型
        :param Ffavorites_id:收藏id
        :return:
        '''

        try:

            favorites_service.set_db(self.db)
            self.get_paras_dict()
            user_id = self.get_current_user().get('Fid')
            self.qdict['user_id'] = user_id
            m_key = 'user_favorite_'+str(user_id)+str(self.qdict.get('favorite_type'))+str(self.qdict.get('favorite_id'))
            value = self.mcache.get(m_key)
            if not value:
                favorites_service.create_favorite(**self.qdict)
                self.mcache.set(m_key,'ok')
                is_favorite = 1
            else:
                favorites_service.update_favorite(**self.qdict)
                self.mcache.delete(m_key)
                is_favorite = 0
            self.delete_user_favorite(user_id,self.qdict.get('favorite_type'))
            return self.write(ujson.dumps({'stat':'ok','is_favorite':is_favorite,'data':{},'info':''}))

        except Exception,e:
            pass

class UserFavoriteHandler(MobileBaseHandler,AppCacheHandler):

    @Mobile_login_control()
    def get(self, *args, **kwargs):
        '''
        :param favorite_type:收藏类型
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        user_id = self.get_current_user().get('Fid')
        favorite_type = self.qdict.get('favorite_type')
        try:
            lst_data = self.get_favorites_info(user_id,favorite_type)
            self.write_json({'stat':'ok','data':lst_data,'has_content':len(lst_data) > 0 and 1 or 0,'info':''})
        except Exception,e:
            pass
            










