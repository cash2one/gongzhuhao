#encoding:utf-8
__author__ = 'binpo'

from common.pyoauth2 import Client

import ujson

from tornado.options import options, define
from utils.oauth_user_util import get_oauth_user_info
import urllib
from services.users.user_services import UserServices

from common.base import BaseHandler
class QQLoginHandler(BaseHandler):
    def post(self):
        client = Client(options.QQ_KEY, options.QQ_SECRET,
                        site='https://graph.qq.com',
                        authorize_url='https://graph.qq.com/oauth2.0/authorize',
                        token_url='https://graph.qq.com/oauth2.0/token')

        authorize_url = client.auth_code.authorize_url(redirect_uri=options.QQ_CALLBACK,
                            scope='get_user_info,list_album,upload_pic,do_like')
        self.redirect(authorize_url)

    def get(self, *args, **kwargs):
        self.post()

class QQloginHandlerCallback(BaseHandler):

    def get(self, *args, **kwargs):
        code = self.get_argument('code')
        code = code.strip()
        client = Client(options.QQ_KEY, options.QQ_SECRET,
                site='https://graph.qq.com',
                authorize_url='https://graph.qq.com/oauth2.0/authorize',
                token_url='https://graph.qq.com/oauth2.0/token')
        access_token = client.auth_code.get_token(code, redirect_uri=options.QQ_CALLBACK, parse='query')


        # for key in access_token.params.keys():
        #     print access_token.params.get(key),'0000000000000'



        token = access_token.token
        client_id = access_token.params.get('client_id')
        content = urllib.urlopen('https://graph.qq.com/oauth2.0/me?access_token='+access_token.token).read()
        open_id = ujson.loads(content[content.find('{'):content.find('}')+1]).get('openid')
        user_info = get_oauth_user_info('https://graph.qq.com/user/get_user_info',oauth_consumer_key=options.QQ_KEY,access_token=access_token.token,format='json',openid=open_id)
        user = ujson.loads(user_info)
        #['figureurl_2','nickname','open_id']

        # print user.get('figureurl_2')
        # print open_id
        # print user.get('nickname')
        # print user.get('gender')
        #
        # print user_info

        user_service = UserServices(self.db)
        exist_user = user_service.get_user_by_qq(open_id)
        #user = user_service.get_user_by_weibo(user_json.get('idstr'))


        user = user_service.create_user_by_qq(user=exist_user,nick=user.get('nickname'),photo=user.get('figureurl_qq_2'),qq=open_id)
        #
        # uid = self.user_uid(user_name=kargs.get('open_id',''))
        # user.uid = uid
        # user.nick = kargs.get('nick','')
        # user.email = kargs.get('email','')
        # user.phone = kargs.get('phone','')
        # user.photo = kargs.get('photo', '')
        # user.is_employee = kargs.get('is_employee',0)
        # user.sex = kargs.get('sex','')
        # user.last_visit = datetime.now()
        # user.last_visit_ip = kargs.get('last_visit_ip','')
        # user.visit_times = kargs.get('visit_times',0)
        # user.regist_from = kargs.get('regist_from','qq')
        # user.find_pw_url = kargs.get('find_pw_url','')
        # user.status = kargs.get('status','normal')
        # user.avatar = kargs.get('avatar','')
        # user.sign_text = kargs.get('sign_text','')

        # qq_weibo_info = get_oauth_user_info('https://graph.qq.com/user/get_info',oauth_consumer_key=options.QQ_KEY,access_token=access_token.token,format='json',openid=open_id)
        # print qq_weibo_info
        # print 'save user'
        print user.id
        cookies = user_service.user_format(user)
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