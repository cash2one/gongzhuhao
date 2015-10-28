#encoding:utf-8
__author__ = 'binpo'

from common.pyoauth2 import Client

import ujson

from tornado.options import options, define
from utils.oauth_user_util import get_oauth_user_info
import urllib
from services.users.user_services import UserServices

from common.base import BaseHandler
class WeixinLoginHandler(BaseHandler):
    def post(self):
        # client = Client(options.WEIXIN_KEY, options.WEIXIN_SECRET,
        #                  site='https://open.weixin.qq.com',
        #                  authorize_url='https://open.weixin.qq.com/connect/qrconnect',
        #                  token_url='https://api.weixin.qq.com/sns/oauth2/access_token')
        #
        #
        # authorize_url = client.auth_code.authorize_url(redirect_uri=options.WEIXIN_CALLBACK,
        #                     scope='snsapi_login',response_type='code',appid=options.WEIXIN_KEY)
        #self.redirect(authorize_url)
        # #
        #authorize_url = client.auth_code.authorize_url(redirect_uri=options.WEIXIN_CALLBACK,
        #                     scope='get_user_info,list_album,upload_pic,do_like')
        # redirect_url  = urllib.urlencode(options.WEIXIN_CALLBACK)
        params = {'appid':options.WEIXIN_KEY,'redirect_uri':urllib.urlencode(options.WEIXIN_CALLBACK),'response_type':'code','scope':'snsapi_login'}
        authorize_url = 'https://open.weixin.qq.com/connect/qrconnect?'+urllib.urlencode(params)
        self.redirect(authorize_url)

    def get(self, *args, **kwargs):
        client = Client(options.WEIXIN_KEY, options.WEIXIN_SECRET,
                         site='https://open.weixin.qq.com',
                         authorize_url='https://open.weixin.qq.com/connect/qrconnect',
                         token_url='https://api.weixin.qq.com/sns/oauth2/access_token')


        authorize_url = client.auth_code.authorize_url(redirect_uri=options.WEIXIN_CALLBACK,
                            scope='snsapi_login',response_type='code',appid=options.WEIXIN_KEY)
        self.redirect(authorize_url)

class WeixinloginHandlerCallback(BaseHandler):

    def get(self, *args, **kwargs):
        code = self.get_argument('code')
        code = code.strip()


        # print code
        # client = Client(options.QQ_KEY, options.QQ_SECRET,
        #         site='https://graph.qq.com',
        #         authorize_url='https://graph.qq.com/oauth2.0/authorize',
        #         token_url='https://graph.qq.com/oauth2.0/token')
        # access_token = client.auth_code.get_token(code, redirect_uri=options.QQ_CALLBACK, parse='query')
        #
        #
        # # for key in access_token.params.keys():
        # #     print access_token.params.get(key),'0000000000000'
        #
        #
        #
        # token = access_token.token
        # client_id = access_token.params.get('client_id')
        author_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code'

        content = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(options.WEIXIN_KEY,options.WEIXIN_SECRET,code)).read()
        token_info = ujson.loads(content)
        openid = token_info.get('openid')
        access_token = token_info.get('access_token')
        user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'%(access_token,openid)).read()
        user = ujson.loads(user_info)

        user_service = UserServices(self.db)
        exist_user = user_service.get_user_by_weixin(openid)
        print 'openid:',openid
        new_user = user_service.create_user_by_weixin(user=exist_user,nick=user.get('nickname'),photo=user.get('headimgurl'),weixin=openid,sex=user.get('sex'))
        print new_user.id
        cookies = user_service.user_format(new_user)
        self.set_secure_cookie('loginuser',ujson.dumps(cookies))
        self.redirect('/')


    def post(self, *args, **kwargs):
        self.get()

    # def get_qq_user_info(self):
    #     https://graph.qq.com/user/get_user_info?
    #     import urllib
    #     try:
    #         import urlparse
    #     except ImportError:
    #         import urllib.parse as urlparse
    #     try:
    #         import urllib.parse as urllib_parse
    #     except ImportError:
    #         import urllib as urllib_parse
    #     weibo_user_url = options.WEIBO_USER_SHOW_URL+'?'+urllib_parse.urlencode(kwargs)
    #     response = urllib.urlopen(options.WEIBO_USER_SHOW_URL,urllib_parse.urlencode(kwargs))
    #     #print weibo_user_url
    #     response = urllib.urlopen(weibo_user_url)
    #     return  response.read()
# client = Client(KEY, SECRET,
#                 site='https://graph.qq.com',
#                 authorize_url='https://graph.qq.com/oauth2.0/authorize',
#                 token_url='https://graph.qq.com/oauth2.0/token')
#
# print '-' * 80
# authorize_url = client.auth_code.authorize_url(redirect_uri=CALLBACK,
#                     scope='get_user_info,list_album,upload_pic,do_like')
# print 'Go to the following link in your browser:'
# print authorize_url
# print '-' * 80
#
# code = raw_input('Enter the verification code and hit ENTER when you\'re done:')
# code = code.strip()
# access_token = client.auth_code.get_token(code, redirect_uri=CALLBACK, parse='query')
#
# print 'token', access_token.headers
# print access_token.expires_at