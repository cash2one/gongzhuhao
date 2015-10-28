#encoding:utf-8
__author__ = 'binpo'

from apps_web.demo.urls import _handlers as demo_handers
from apps_web.users.urls import _handlers as user_handlers
from apps_web.login_handler import LoginApiHandler,LoginOutApiHandler,RegApiHandler,CheckLoginHandler,\
    DemoTestHandler,LoginHandler,RegisterHandler,MobileCodeLogin
from apps_web.home import TopicIndexHandler,ViewsIndexHandler,UserIndexHandler,HomeHandler,Activities

handlers=[


    (r'/login',LoginHandler),                    #用户登陆
    (r'/login_code.html',MobileCodeLogin),                    #用户登陆
    (r'/reg',RegisterHandler),
    (r'/api/login',LoginApiHandler),                    #用户登陆
    (r'/api/reg',RegApiHandler),                        #用户注册
    (r'/logout',LoginOutApiHandler),                #用户登出
    (r'/api/logout/',LoginOutApiHandler),                #用户登出
    (r'/api/check_login/',CheckLoginHandler),            #判断是否登录
    (r'/api/template_test/',DemoTestHandler),

    (r'/topics/views/([\w\W]*)',ViewsIndexHandler),
    (r'/topics/([\w\W]*)',TopicIndexHandler),

    (r'/views/account/index.html',UserIndexHandler),#用户首页
    (r'/views/([\w\W]*)',ViewsIndexHandler),
    (r'/tmp/([\w\W]*)',Activities)
]
handlers.extend(demo_handers)
handlers.extend(user_handlers)

from apps_web.album import urls as ablum_url
handlers.extend(ablum_url.handlers)

from apps_web.topic import urls as topic_url
handlers.extend(topic_url.handlers)

from apps_web.merchants import urls as merchant_url
handlers.extend(merchant_url._handlers)

from apps_web.series import  urls as series_url
handlers.extend(series_url.handlers)

from apps_web.products import urls as product_url
handlers.extend(product_url.handlers)

from apps_web.orders import urls as order_url
handlers.extend(order_url.handlers)

from apps_web.activity import urls as activity_url
handlers.extend(activity_url._handlers)

from apps_web.weddingdress import urls as weddingdress_url
handlers.extend(weddingdress_url.handlers)

from apps_web.weddingcompany import urls as weddingcompany_url
handlers.extend(weddingcompany_url.handlers)

handlers.append((r'/([\w\W]*)',HomeHandler))