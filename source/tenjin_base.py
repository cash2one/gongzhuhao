#encoding:utf-8

import os
import urllib
import urlparse
import tenjin
import tornado.web

from tenjin.helpers import *

crm_engine = tenjin.Engine(path=[os.path.join(os.path.dirname(__file__),'templates')], cache=tenjin.MemoryCacheStorage(),preprocess=True)

mobile_engine = tenjin.Engine(path=[os.path.join(os.path.dirname(__file__),'weixin_mobile')], cache=tenjin.MemoryCacheStorage(),preprocess=True)

web_engine = crm_engine #tenjin.Engine(path=[os.path.join(os.path.dirname(__file__),'gongzhuhao_web')], cache=tenjin.MemoryCacheStorage(),preprocess=True)

from raven.contrib.tornado import SentryMixin

class TenjinBase(tornado.web.RequestHandler,SentryMixin):

    def __init__(self, *argc, **argkw):
        self.title=''
        self.description=''
        self.keywords=''
        super(TenjinBase, self).__init__(*argc, **argkw)

    @property
    def get_client_ip(self):
        ip = self.request.headers.get("X-Client-Ip",'')
        if ip==None or ip=='':
            ip = self.request.headers.get("X-Real-IP",'')
        if ip==None or ip=='':
            ip = self.request.remote_ip
        return ip.split(',')[0]

    def get_paras_dict(self):
        """
        :todo 获取请求参数 字典
        """
        if self.request.method=='GET':
            query = self.request.query
            self.qdict = urlparse.parse_qs(query)
            for k, v in self.qdict.items():
                self.qdict[k] = v and v[0] or ''
        elif self.request.method in ('POST','PUT'):
            self.qdict={}
            query = self.request.arguments
            for key in query.keys():
                self.qdict[key]=len(query[key])!=1 and query[key] or (query[key][0] and query[key][0] or '')

    def get_show_img_url(self,img_url,width):
        _url = ''
        if img_url:
            img_list = img_url.split('@')
            if len(img_list)<=1:
                _url = img_list[0]+'@'+str(width)+'h.jpg'
            else:
                tmp_list = img_list[:-1]
                tmp_list.append('@')
                tmp_list.append(str(width)+'h_')
                tmp_list.append(img_list[-1])
                _url = ''.join(tmp_list)
        return _url

    def img_compression(self,img_url,img_size=0):
        '''
            jpg格式压缩
            原图:876K
            80q压缩:134
            43q压缩:70
            30q压缩:55
        '''
        if img_size==0 or not img_size:
            return img_url
        _url = ''
        if img_url:
            img_list = img_url.split('@')
            if len(img_list)<=1:
                _url = img_list[0]
            else:
                tmp_list = img_list[:-1]
                _url = ''.join(tmp_list)

        img_size = img_size/1000

        if img_size > 4000:
            return _url+'@50q_0r.jpg'
        elif img_size > 3000:
            return _url+'@60q_0r.jpg'
        elif img_size > 2000:
            return _url+'@65q_0r.jpg'
        elif img_size > 1000:
            return _url+'@70q_0r.jpg'
        elif img_size > 500:
            return _url+'@90q_0r.jpg'
        else:
            return _url+'@80q_0r.jpg'

        # if img_size>1000:
        #     return _url+'@300h.jpg'
        # elif img_size>500:
        #     return _url+'@400h.jpg'
        # else:
        #     return _url

    def set_cache(self, seconds, is_privacy=None):
        if seconds <= 0:
            self.set_header('Cache-Control', 'no-cache')
        else:
            if is_privacy:
                privacy = 'public, '
            elif is_privacy is None:
                privacy = ''
            else:
                privacy = 'private, '
            self.set_header('Cache-Control', '%smax-age=%s' % (privacy, seconds))

class WebTenjinBase(TenjinBase):

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html(),
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        return crm_engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):

        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        self.write(self.render(template, context, globals, layout))

class MobileTenjinBase(TenjinBase):

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html(),
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        return mobile_engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        self.write(self.render(template, context, globals, layout))

class ViewsTenjinBase(TenjinBase):

    def render(self, template, context=None, globals=None, layout=False):
        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html(),
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        return web_engine.render(template, context, globals, layout)

    def echo(self, template, context=None, globals=None, layout=False):

        if context is None:
            context = {}
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            xsrf_form_html=self.xsrf_form_html,
            xsrf_token=self.xsrf_token,
        )
        context.update(args)
        self.write(self.render(template, context, globals, layout))

