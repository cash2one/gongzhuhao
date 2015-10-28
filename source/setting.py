# encoding:utf-8
__author__ = 'binpo'

import os

current_path = os.path.dirname(__file__)
static_path = os.path.join(current_path, 'static')
template_path = os.path.join(current_path, 'templates')

mobiel_static_path = os.path.join(current_path, 'weixin_mobile')

mobile_template_path = os.path.join(current_path, 'weixin_mobile')

EV = "TEST"

# img_upload = 'upload/img/'
# upload_path = os.path.join(static_path, img_upload)
#
# avatar_upload = 'upload/img/avatar/'
# upload_avatar_path = os.path.join(static_path, avatar_upload)


settings = dict(
    title=u"公主号",
    desc=u"公主号",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^&&*(())&%^#@#@gongzhuhao1238^($#@&)',
    login_url='/login',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)


admin_settings = dict(
    title=u"公主号",
    desc=u"公主号",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^&&*(())&%^#@#@gongzhuhao1238^($#@&)',
    login_url='/gzh/ops/login',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)


settings_mobile = dict(
    title=u"公主号mobiel",
    desc=u"公主号mobiel",
    static_path=mobiel_static_path,
    template_path=mobile_template_path,
    cookie_secret='^&&*(())&%^#@#@gongzhuhao1238^($#@&)',
    login_url='/mobile/user/login',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)

web_settings = dict(
    title=u"公主号",
    desc=u"公主号",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^&&*(())&%^#@#@gongzhuhao1238^($#@&)',
    login_url='/login',
    xsrf_cookies=False,
    debug=True,
    page_size=50,
)

settings_ignore_csrf = dict(
    title=u"公主好",
    desc=u"公主号",
    static_path=static_path,
    template_path=template_path,
    cookie_secret='^&&*(())&%^#@#@gongzhuhao1238($#@&)',
    login_url='/login/page',
    xsrf_cookies=False,
    debug=False,
    page_size=50,
)

# oss access key
ACCESS_ID = 'axRou5raSPrYnIhN'
SECRET_ACCESS_KEY = '0j9EiLmuzz5zpsEFj3Cu9dzqq4Yv1y'
IMG_BUCKET = 'wwwgongzhuhao'


OSS_HOST = "oss.aliyuncs.com"
EV = "TEST"


#配置相关配置
WX_GZH_AppID='wx1bba07356b89c006'
WX_GZH_AppSecret='bc44188f8185708b2422c812a8a0a54f'
WX_ACCESS_URL = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"   #含两个参数
WX_MENU_DELETE_URL = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
WX_MENU_CREATE_URL = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
WX_MENU_GET_URL = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="
WX_APP_URL = "http://m.gongzhuhao.com/weixin"
WX_JSAPI_TICKET = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi"
WX_DOWN_MEDIA_URL = "http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s"


#ocs access key
OCS_ACCESS_URL = '58144c1529ce4b68.m.cnhzaliqshpub001.ocs.aliyuncs.com:11211'
OCS_ACCESS_ID = '58144c1529ce4b68'
OCS_ACCESS_PASS = 'Qiuyan_123520'

# redis config
REDIS_HOST='127.0.0.1'
REDIS_PORT=6379

# redis config
MEMCACHE_HOST='127.0.0.1:11211'


#celery配置信息
#broker, backend
BACKEND_URL = 'redis://127.0.0.1:6379/2'

# BROKER_URL = 'amqp://guest:guest@localhost:5672//'
BROKER_URL = 'redis://127.0.0.1:6379/1'

#Database : Mysql
ENGINE="mysql://root:123456@localhost:3306/db_gongzhuhao?charset=utf8"
