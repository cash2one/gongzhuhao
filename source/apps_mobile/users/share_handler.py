#encoding:utf-8
__author__ = 'jinkuan'

import tornado
from services.users.user_services import UserServices
from services.ablums.photos_service import PhotosServices
from services.shares.shares_service import ShareServices
from services.music.music_service import MusicServices
from conf.share_conf import SHARE_TITLE,_SHARE_TEMPLATE
from conf.order_conf import _TYPE_ORDER
from services.company.company_services import CompanyServices,CompanyAdditionInfoServices
import urllib,ujson
from common.mweixin_oauth.wx_mobile_info import get_wx_login_redirect_url
from common.permission_control import Mobile_login_control
from setting import WX_GZH_AppID,WX_GZH_AppSecret
from datacache.datacache import PageDataCache
from utils.sign import sign
from apps_mobile.mobile_base import MobileBaseHandler
import sys

user_service = UserServices()
photos_service = PhotosServices()
share_service = ShareServices()
info_service = CompanyAdditionInfoServices()
company_service = CompanyServices()
music_service = MusicServices()


class WxPhotosShareHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self):
        uid = self.get_current_user().get('Fid')
        share_service.set_db(self.db)
        try:
            shares = share_service.query_shares_by_user_id(uid)
            lstdata = []
            for share in shares:
                lstdata.append({'cover_img':self.get_show_img_url(share.Fcover_img,300) if share.Fcover_img else '',
                                'title':share.Ftitle,
                                'description':share.Fdescription,
                                'create_time':share.Fcreate_time,
                                'href':'/mobile/user/photos/share/'+str(share.Fid)+'/'
                               })
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','list':[],'data':{},'info':'获取分享失败,失败原因:'+e.message})
        self.write_json({'stat':'1000','list':lstdata,'data':{},'info':''})

class ShareCreateHandler(MobileBaseHandler):

    @Mobile_login_control()
    def get(self,album_id):
        photos_service.set_db(self.db)
        music_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        try:
            album = photos_service.get_ablum_ablum_id(album_id)
            musics = music_service.query_share_music()
            lstmusics = []
            for music in musics:
                lstmusics.append({'music_url':music.Fmusic_url,'music_id':music.Fid,'music_name':music.Fmusic_name})
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'An exception occured,caused:'+e.message})
        self.write_json({'stat':'1000','title':SHARE_TITLE % (album.Fablum_name, album.Falbum_type),
                         'description':_SHARE_TEMPLATE[_TYPE_ORDER.index(album.Falbum_type)],'list_music':lstmusics})

    @Mobile_login_control()
    def post(self, album_id):
        user_id = self.get_current_user().get('Fid')
        photos_service.set_db(self.db)
        share_service.set_db(self.db)
        try:
            album = photos_service.get_ablum_ablum_id(album_id)
            body = ujson.loads(self.request.body)

            print '>>>>>>body>>>>>>',body

            body['Fcover_img'] = album.Furl_pic_cover
            body['user_id'] = user_id
            body['album_id'] = album.Fid
            body['Fmerchant_id'] = album.Fuid_mct
            body['Forder_id'] = album.Forder_id
            data = {}
            data['Fdeleted'] =1
            share_service.update_share(album.Fid,**data)
            user_photo_share = share_service.create_share(**body)
            photos = photos_service.query_photos_by_ablum_id2(user_id,album.Fid)
            share_service.create_share_image(user_photo_share.Fid,photos)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'An exception occur,cause:'+e.message})
        self.write_json({'stat':'1000','info':'','href':'/mobile/user/photos/share/'+str(user_photo_share.Fid)+'/'})

class UserShareDetailHandler(MobileBaseHandler):

    def get(self, user_share_id, **kwargs):

        share_service.set_db(self.db)
        company_service.set_db(self.db)
        user_photos_share = share_service.get_by_id(user_share_id)
        share_images = share_service.get_images_by_id(user_photos_share.Fid)
        share_wishs = share_service.get_wishs_by_share_id(user_photos_share.Fid)
        company = company_service.get_company_by_uid(user_photos_share.Fmerchant_id)

        login_user = self.get_current_user()

        nick_name = ''
        is_self=False
        if not self.get_current_user() or (login_user and login_user.get('Fid')!=user_photos_share.Fuser_id):
            weixin_data = self.get_cookie('mobile_wish_weixin')
            if weixin_data:
                nick_name = ujson.loads(weixin_data).get('nickname')
            else:
                try:
                    user_agent = self.request.headers.get('User-Agent')
                    user_agent = user_agent.lower()
                    is_weixin = user_agent.find('micromessenger') > -1
                    if is_weixin:
                        self.get_paras_dict()
                        if not self.qdict.has_key('code'):
                            raise
                        else:
                            code = self.qdict.get('code')
                            code = code.strip()
                            content = urllib.urlopen('https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(WX_GZH_AppID,WX_GZH_AppSecret,code)).read()
                            token_info = ujson.loads(content)
                            openid = token_info.get('openid')
                            access_token = token_info.get('access_token')
                            user_info = urllib.urlopen('https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s'%(access_token,openid)).read()

                            user = ujson.loads(user_info)
                            nick_name = user.get('nickname')
                            photo=user.get('headimgurl')
                            weixin=openid
                            data={'view_weixin_openid':weixin,'photo':photo,'nick_name':nick_name}
                            self.set_cookie('mobile_wish_weixin',ujson.dumps(data),expires_days=1)

                except Exception,e:
                    params = urllib.urlencode(self.qdict)
                    _url='http://m.gongzhuhao.com/mobile/user/photos/share/'+user_share_id+"/"
                    direct_url = get_wx_login_redirect_url(_url)
                    return self.redirect(direct_url)
        else:
            is_self=True

        cookies = self.get_cookie('mobile_wish_weixin')
        if cookies:
            openid = ujson.loads(cookies).get('view_weixin_openid')
            share_wish = share_service.get_wish_by_weixin_and_share_id(user_share_id,openid)
        else:
            share_wish=1

        #微信-配置
        page_cache = PageDataCache(self.db)
        access_token = page_cache.get_access_token(WX_GZH_AppID,WX_GZH_AppSecret)
        jsapi_ticket = page_cache.get_jsapi_ticket(access_token)
        share_url = 'http://m.gongzhuhao.com' + '/mobile/user/photos/share/'+user_share_id+'/'
        wx_sign = sign(WX_GZH_AppID, jsapi_ticket, share_url)
        dic_sign = wx_sign.get_sign()

        # cache_views('t_user_photos_share',int(user_share_id),count=user_photos_share.Fpage_view)
        self.set_page_view('t_user_photos_share',user_photos_share.Fid,0)

        url = 'views/photos/share.html'
        self.echo(url,
                  {
                   'user_photos_share':user_photos_share,
                   'user_photo_share_id':user_share_id,
                   'share_wishs':share_wishs,
                   'access_token' : access_token,
                   'dic_sign' : dic_sign,
                   'share_url':share_url,
                   'share_images':share_images,
                   'is_self':is_self,
                   'share_wish':share_wish,
                   'company':company
                  },layout='')

class ShareWishHandler(MobileBaseHandler):

    def post(self):
        share_service.set_db(self.db)
        try:
            self.get_paras_dict()
            wx_info = self.get_cookie('mobile_wish_weixin')
            self.qdict['weixin'] = ujson.loads(wx_info)
            wish = share_service.commit_wishes(**self.qdict)
            _html = self.render('views/photos/share_page.html',{'wish':wish})
            self.write_json({'code':200,'data':_html,'info':''})
        except Exception,e:
            pass

class PotentialCustomerHandler(MobileBaseHandler):

    def post(self, *args, **kwargs):

        share_service.set_db(self.db)
        user_service.set_db(self.db)

        try:
            self.get_paras_dict()
            if not self.qdict.get('Fcust_phone'):
                return self.write_json({'stat':'error','info':'请填写手机号码'})
            user_id = self.qdict.get('Fuser_id')
            user = user_service.get_user_by_id(user_id)
            self.qdict['Fuser_name'] = user.Fnick_name
            cus = share_service.commit_potential(**self.qdict)
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':e.message})

        return self.write_json({'stat':'ok','info':'','data':''})
















