#encoding:utf-8

from weibo import APIClient
import datetime
from tornado.options import options, define
import ujson

from common.base import BaseHandler


from utils.oauth_user_util import get_oauth_user_info
from services.users.user_services import *
class WeiboLoginHandler(BaseHandler):
    def post(self): # 注意，这里是post
        client = APIClient(app_key=options.APP_KEY,
                           app_secret=options.APP_SECRET,
                           redirect_uri=options.CALLBACK_URL)
        url = client.get_authorize_url()
        # self.write('<a href="' + url +'">click</a>')
        # 用户点击链接后跳转到验证界面

        self.redirect(url) # 直接跳转到验证界面

    def get(self, *args, **kwargs):
        self.post()

class WeiboLoginHandlerCallback(BaseHandler):
    """微博登录回调函数
        获取微博用户信息
    """
    def post(self): # 注意，这里也是post
        code = self.get_argument('code', '21330')
        if code == '21330':
            self.redirect('/login')
        client = APIClient(app_key=options.APP_KEY,
                           app_secret=options.APP_SECRET,
                           redirect_uri=options.CALLBACK_URL)
        r = client.request_access_token(code)
        access_token = r.access_token
        expires_in = r.expires_in
        uid = r.uid
        client.set_access_token(access_token, expires_in)
        user_json = ujson.loads(get_oauth_user_info(options.WEIBO_USER_SHOW_URL,access_token=access_token,uid=uid))
        # print user_json
        # print '------------------------'
        # print 'weibo login-----------'
        # print type(user_json)
        # print '---------------分割线---------------'
        # for key in user_json.keys():
        #     print key,user_json.get(key)
        user_service = UserServices(self.db)

        user = user_service.get_user_by_weibo(user_json.get('idstr'))
        # if user:
        #     pass
        # else:
        #     '根据微博创建用户'
        #user = user_service.get_user_by_username(user_json['idstr'])
        '''

            user.nick = kargs.get('nick','')
            user.email = kargs.get('email','')
            user.phone = kargs.get('phone','')
            user.photo = kargs.get('photo', '')
            user.is_employee = kargs.get('is_employee',0)
            user.sex = kargs.get('sex','')
            user.weibo = kargs.get('weibo','')
            user.last_visit = datetime.now()
            user.last_visit_ip = kargs.get('last_visit_ip','')
            user.visit_times = kargs.get('visit_times',0)
            user.regist_from = kargs.get('regist_from','weibo')
            user.find_pw_url = kargs.get('find_pw_url','')

            user.status = kargs.get('status','normal')
            user.avatar = kargs.get('avatar','')
            user.sign_text = kargs.get('sign_text','')

        '''
        #if not user:
            #['idstr','location','description','profile_image_url','screen_name','gender','verified_contact_email']

        user = user_service.create_user_by_weibo(user=user ,weibo=user_json.get('idstr'),email=user_json.get('verified_contact_email'),photo=user_json.get('profile_image_url'),nick=user_json.get('screen_name'),sign_text=user_json.get('description'))
        #print user.nick
        # else:
        #     #user.last_visit = datetime.datetime.now()
        #     user.last_visit_ip = self.get_client_ip#self.request.remote_ip
        #     user.visit_times = user.visit_times+1
        #     self.db.add(user)

        self.db.commit()
        print user.id
        cookies = user_service.user_format(user)
        self.set_secure_cookie('loginuser',ujson.dumps(cookies))
        self.redirect('/')

        ['idstr','location','description','profile_image_url','screen_name','gender','verified_contact_email']

        """

            domain zenmez
            avatar_large http://tp1.sinaimg.cn/5365421384/180/5715426504/1
            bi_followers_count 16
            verified_source
            ptype 0
            verified_level 3
            block_word 0
            star 0
            微博id:id 5365421384
            verified_reason_url
            city 15
            verified True
            邮件:verified_contact_email
            verified_reason_modified
            credit_score 80
            block_app 0
            follow_me False
            verified_reason 上海壹家人网络科技有限公司
            followers_count 99
            地域:location 上海 浦东新区
            verified_state 0
            verified_trade
            mbtype 0
            verified_source_url
            profile_url zenmez
            province 31
            avatar_hd http://ww4.sinaimg.cn/crop.106.143.966.966.1024/005R6LcAjw8enyw7uthwdj30xc0xcdhw.jpg
            statuses_count 124
            description 怎么装，全国最大的家装分享平台。想怎么装就怎么装，从此告别装修烦恼！ zenmez.com
            friends_count 20
            online_status 1
            mbrank 0
            微博ID:idstr 5365421384
            小头像:profile_image_url http://tp1.sinaimg.cn/5365421384/50/5715426504/1
            allow_all_act_msg False
            following False
            allow_all_comment True
            geo_enabled True
            class 1
            名称:name 壹家人-怎么装
            lang zh-cn
            weihao
            remark
            favourites_count 0
            显示名称:screen_name 壹家人-怎么装
            verified_contact_mobile
            url
            性别:gender m
            created_at Mon Nov 10 16:18:19 +0800 2014
            verified_contact_name
            verified_type 2
            cover_image http://ww1.sinaimg.cn/crop.0.0.920.300/005R6LcAgw1en2bj2k64qj30pk08cmzb.jpg
            pagefriends_count 0
            urank 8

        {
            id: 1671621591,
            idstr: "1671621591",
            class: 1,
            screen_name: "冰_破",
            name: "冰_破",
            province: "33",
            city: "1",
            location: "浙江 杭州",
            description: "",
            url: "",
            profile_image_url: "http://tp4.sinaimg.cn/1671621591/50/40014847527/1",
            profile_url: "u/1671621591",
            domain: "",
            weihao: "",
            gender: "m",
            followers_count: 0,
            friends_count: 0,
            pagefriends_count: 0,
            statuses_count: 0,
            favourites_count: 111,
            created_at: "Tue Apr 06 09:05:06 +0800 2010",
            following: false,
            allow_all_act_msg: false,
            geo_enabled: true,
            verified: false,
            verified_type: -1,
            remark: "",
            status: { },
            ptype: 0,
            allow_all_comment: true,
            avatar_large: "http://tp4.sinaimg.cn/1671621591/180/40014847527/1",
            avatar_hd: "http://tp4.sinaimg.cn/1671621591/180/40014847527/1",
            verified_reason: "",
            verified_trade: "",
            verified_reason_url: "",
            verified_source: "",
            verified_source_url: "",
            follow_me: false,
            online_status: 1,
            bi_followers_count: 148,
            lang: "zh-cn",
            star: 0,
            mbtype: 0,
            mbrank: 0,
            block_word: 0,
            block_app: 0,
            credit_score: 80
            }
        """

    def get(self, *args, **kwargs):
        self.post()
    #
    # def get_weibo_user_info(self,**kwargs):
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