#encoding:utf-8
__author__ = 'binpo'

from common.pyoauth2 import Client

import ujson

from tornado.options import options, define
from utils.oauth_user_util import get_oauth_user_info
import urllib

from common.base import BaseHandler
class MWeixinLoginHandler(BaseHandler):

    def get(self, *args, **kwargs):
        authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize?'
        p={}
        p['appid']='wx35567001c17ac9a1'
        authorize_url=authorize_url+urllib.urlencode(p)
        p={}
        p['redirect_uri']=self.get_argument('http://mx.zenmez.com/test/mwx/callback')
        authorize_url=authorize_url+'&'+urllib.urlencode(p)
        p={}
        p['response_type']='code'
        authorize_url=authorize_url+'&'+urllib.urlencode(p)
        p={}
        p['scope']='snsapi_userinfo'
        authorize_url=authorize_url+'&'+urllib.urlencode(p)
        #wechat_redirect
        url = authorize_url+'#wechat_redirect'
        self.redirect(url)

#https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx35567001c17ac9a1&redirect_uri=http%3A%2F%2Fmx.zenmez.com%2Ftest%2Fmwx%2Fcallback&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect
#https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx35567001c17ac9a1&redirect_uri=http%3A%2F%2Fmx.zenmez.com%2Ftest%2Fmwx%2Fcallback&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect

