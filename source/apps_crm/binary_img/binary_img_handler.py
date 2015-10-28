#encoding:utf-8
__author__ = 'binpo'

from common.base import AdminBaseHandler
import StringIO
from setting import EV
from common.base import BaseHandler
import tornado
class BinaryImgHandler(AdminBaseHandler):

    def post(self,order_id):
        #url = self.get_argument('url')
        domain=''
        if EV=="TEST":
            domain = self.get_client_ip+':8000'
        else:
            domain = 'http://www.gongzhuhao.com'
        url ='http://%s/user/schedule/%s/'
        import qrcode
        q=qrcode.main.QRCode()
        binary_url = url%(domain,order_id)
        q.add_data(binary_url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)

    def get(self,order_id):
        self.post(order_id)
        #self.echo('ops/common/img_binary.html')

class UserInoutUrlQrcreaterHandler(BaseHandler):

    def post(self):
        url = self.get_argument('url')
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()
        self.set_header('Content-Type','image/png')
        self.write(img_data)
    @tornado.web.authenticated
    def get(self):
        if self.get_argument('url',None):
            url = self.get_argument('url')
            import qrcode
            q=qrcode.main.QRCode()
            q.add_data(url)
            q.make(fit=True)
            img = q.make_image()
            output = StringIO.StringIO()
            img.save(output)
            img_data = output.getvalue()
            output.close()
            self.set_header('Content-Type','image/png')
            self.write(img_data)
        else:
            self.echo('crm/system/img_binary.html',layout='crm/common/base.html')