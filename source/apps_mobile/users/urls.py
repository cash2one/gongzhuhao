#encoding:utf-8
__author__ = 'binpo'

from tornado.web import url

from apps_mobile.users.user_handler import *
from apps_mobile.users.photos_handler import AlbumPhotosDetailHandler, \
    WxAlbumPhotosHandler, AlbumPhotosListHandler
from apps_mobile.users.share_handler import ShareCreateHandler, \
    UserShareDetailHandler,WxPhotosShareHandler,ShareWishHandler,PotentialCustomerHandler
_handlers = [

    (r'/mobile/20151985112504291695293/([\w\W]*)', TopicUrlTransform),
    (r'/mobile/redirect/([\w\W]*)', TopicUrlTransform),

    (r'/mobile/user/index/', MobileUserIndexHandler),
    (r'/mobile/user/show/services/check/',ShowServicesHandler),
    (r'/weixin/user/index/', MobileUserIndexHandler),


    (r'/mobile/user/album/detail/([\d]{1,9})/', AlbumPhotosDetailHandler),
    (r'/mobile/user/album/list/([\d]{1,9})/', AlbumPhotosListHandler),
    (r'/weixin/user/photos/', WxAlbumPhotosHandler),  # 我的照片

    (r'/weixin/user/share/', WxPhotosShareHandler),  # 我的分享
    (r'/mobile/user/create/share/([\w\W]*)/', ShareCreateHandler),
    (r'/mobile/user/photos/share/([\d]{1,9})/', UserShareDetailHandler),
    (r'/mobile/create/share/comment',ShareWishHandler),
    (r'/mobile/create/potential/cust',PotentialCustomerHandler),

    (r'/mobile/user/change/password/',ChangePwdHandler),
    (r'/mobile/user/setup/',UserSetHandler),
    (r'/mobile/user/photo/upload/',UserPhotoUploadHandler),

]
