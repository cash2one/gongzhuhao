#encoding:utf-8

import ujson
import tornado.concurrent
import tornado.httpclient
import urllib

class AuthError(Exception):
    pass


class AuthHandler(object):


    def authenticate_redirect(self, app_name, next, callback=None):
        login_url="/gzh/ops/login"
        args = {
                'APP_NAME': app_name,
                'BACK_URL': next,
                }
        self.redirect(login_url + '?' + urllib.urlencode(args))

    @tornado.concurrent.return_future
    def get_authenticated_user(self, token, callback):
        http = self.get_auth_http_client()
        def on_auth(callback, response):
            user = {}
            result = ujson.loads(response.body)
            if not result[u'hasError']:
                user = ujson.loads(result['content'])
                user = self.normalize_user(user)
            else:
                raise AuthError(result.get('content'))
            callback(user)

        http.fetch(self.COMMUNICATE_URL,
                self.async_callback(on_auth, callback),
                method='POST',
                )

    def normalize_user(self, user):
       return user

    def get_auth_http_client(self):
        return tornado.httpclient.AsyncHTTPClient()
