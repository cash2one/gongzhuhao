#encoding:utf-8
__author__ = 'wangjinkuan'

from tornado.web import url
from apps_mobile.favorites.favorites_handler import FavoritesHandler,UserFavoriteHandler

_handlers = [

    url(r'/api/json/create/favorite',FavoritesHandler,name='create_favorite'),
    url(r"/api/json/user/favorite",UserFavoriteHandler,name="user_favorite"),

]
