#encoding:utf-8
__author__ = 'binpo'

import functools
from urllib import urlencode
from tornado.web import HTTPError
import urlparse
from tornado.log import gen_log as log
import tornado
import ujson

def admin_permission_control(role_code):
    """
    check user's rule
    :param role_code  like 'admin,shigong,' 多个用都好隔开
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()#ujson.loads(self.current_user
            x = [ r for r in role_code.split(',') if r in user.get('Frole_codes', '')]
            if x:
                return method(self, *args, **kwargs)
            else:
                self.echo('ops/permission.html')
        return wrapper
    return control


def admin_permission_access():
    """
    check user's rule
    :param role_code  like 'admin,shigong,' 多个用都好隔开
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()#ujson.loads(self.current_user
            if user.get('is_employee') in (1,'1'):
                return method(self, *args, **kwargs)
            else:
                self.redirect('/ops/permission.html')
        return wrapper
    return control

def company_permission_control(permission_code):
    """
    商户后台登陆权限
    :param role_code  like 'admin,shigong,' 多个用都好隔开
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()
            x = [ r for r in permission_code.split(',') if r in user.get('Fpermission', '')]
            if 'merchant' in user.get('Frole_codes') or x:
                return method(self, *args, **kwargs)
            else:
                return self.write(ujson.dumps({'stat':'1003','msg':'抱歉，您无权限操作'}))
        return wrapper
    return control

def Mobile_login_control():
    """
    登录控制
    :param
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()
            if user:
                return method(self, *args, **kwargs)
            else:
                return self.write(ujson.dumps({'code':1001,'data':{},'info':'You haven\'t log on the system!'}))
        return wrapper
    return control

def login_control():
    """
    登录控制
    :param
    """
    def control(method):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            user = self.get_current_user()
            if user:
                return method(self, *args, **kwargs)
            else:
                return self.write(ujson.dumps({'code':1001,'data':{},'info':'You haven\'t log on the system!'}))
        return wrapper
    return control

def site_authenticated(method):

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            if self.request.method in ("GET", "HEAD"):
                url = self.get_login_url()
                if "?" not in url:
                    if urlparse.urlsplit(url).scheme:
                        # if login url is absolute, make next absolute too
                        next_url = self.request.full_url()
                    else:
                        next_url = self.request.uri
                    url += "?" + urlencode(dict(next=next_url))
                self.redirect(url)
                return
            raise HTTPError(403)
        return method(self, *args, **kwargs)
    return wrapper