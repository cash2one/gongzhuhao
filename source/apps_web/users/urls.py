#encoding:utf-8
__author__ = 'binpo'
from apps_web.users.user_handler import UserHandler,PhoneCodeHandler,UserSnsHandler,UserTopicHandler,\
    UserTopicsReplyHandler,UserInfoHandler,UserNotifyHandler,UserTopicsHandler,UserOrdersHandler
# from apps_web.users.acount_bind_handler import AccountBindHandler

_handlers = [
    (r'/api/user/([\w\W]*)',UserHandler),                    #用户操作

    (r'/api/phone/code/([\w\W]*)/([\w\W]*)',PhoneCodeHandler), #手机验证码

    # (r'/account/bind/([\w\W]*)/',AccountBindHandler), #账号绑定

    ('/api/user/topics/([\d]*)',UserTopicHandler),
    ('/api/user/replies/([\d]*)',UserTopicsReplyHandler),

    ('/api/sns/topics/([\d]*)',UserSnsHandler),

    ('/user/profile',UserInfoHandler),
    ('/user/notify',UserNotifyHandler),
    ('/user/topics/reply.html',UserTopicsReplyHandler),
    ('/user/topics/',UserTopicsHandler),
    ('/user/orders/list/',UserOrdersHandler),

]

