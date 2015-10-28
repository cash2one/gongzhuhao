#enoding:utf-8
__author__ = 'binpo'
import ujson
import urllib
from setting import WX_GZH_AppID
def get_wx_login_redirect_url(redirect_url):
    authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize?'
    p={}
    p['appid']=WX_GZH_AppID
    authorize_url=authorize_url+urllib.urlencode(p)
    p={}
    p['redirect_uri']=redirect_url#
    authorize_url=authorize_url+'&'+urllib.urlencode(p)
    p={}
    p['response_type']='code'
    authorize_url=authorize_url+'&'+urllib.urlencode(p)
    p={}
    p['scope']='snsapi_userinfo'
    authorize_url=authorize_url+'&'+urllib.urlencode(p)

    url = authorize_url+'#wechat_redirect'
    return url

def get_wx_login_redirect_url_with_none_access(redirect_url):
    authorize_url='https://open.weixin.qq.com/connect/oauth2/authorize?'
    p={}
    p['appid']=WX_GZH_AppID
    authorize_url=authorize_url+urllib.urlencode(p)
    p={}
    p['redirect_uri']=redirect_url
    authorize_url=authorize_url+'&'+urllib.urlencode(p)
    p={}
    p['response_type']='code'
    authorize_url=authorize_url+'&'+urllib.urlencode(p)
    p={}
    p['scope']='snsapi_base'
    authorize_url=authorize_url+'&'+urllib.urlencode(p)
    #wechat_redirect
    url = authorize_url+'#wechat_redirect'
    return url

def get_wx_user_info(code):
    code = code.strip()
    author_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=APPID&secret=SECRET&code=CODE&grant_type=authorization_code'
    content = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%('wx35567001c17ac9a1','d456626b7c20ea58a94ba2ad410c9d33',code)).read()
    token_info = ujson.loads(content)
    openid = token_info.get('openid')
    access_token = token_info.get('access_token')
    user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'%(access_token,openid)).read()
    user = ujson.loads(user_info)
    return user