#encoding:utf-8
__author__ = 'binpo'
from common.base import AdminBaseHandler


sql1 = "SELECT * FROM t_orders where Foperation_id=9 and date_format(Fcreate_time,'%Y-%m-%d')='2015-06-11'"
sql2 = "SELECT * FROM t_orders where Foperation_id=9 and date_format(Fcreate_time,'%Y-%m-%d')='2015-05-05'"

# phone_msg_tempalte ="""<上海唯一视觉> 已为您开通微信客服，关注微信"公主号"用手机号+验证登陆,即可查看我们为您的设置的拍摄档期.【公主号】"""
# phone_msg_tempalte ="""<上海唯一视觉> 已为您开通"公主号"(微信服务号)客服,手机号+验证码登陆,即可查看拍摄档期.【公主号】"""
# phone_msg_tempalte ="""上海唯一视觉提醒你 已为您开通"公主号"(微信服务号)客服,手机号+验证码登陆,即可查看拍摄档期.【公主号】"""

phone_msg_tempalte ="""上海唯一视觉提醒您，关注微信服务号（公主号）用手机号+验证码登陆,即可查看拍摄档期。【公主号】"""

from models.order_do import Orders
import datetime
from utils.message.sms import *
company_name = '上海唯一视觉全球摄影'

from models.message_do import PhoneMessage
import time
class MessageIndex(AdminBaseHandler):

    def get(self, *args, **kwargs):
        self.echo('ops/message/index.html')

class MessageHandle(AdminBaseHandler):

    def get(self, *args, **kwargs):
        orders = self.db.query(Orders).filter(Orders.Fdeleted==0,Orders.Fuid_mct==9)
        if self.get_current_user().get('Fuser_name')!='qiuyan':
            return self.write('没有权限')
        print orders.count()

        index=0
        f= open('send','r')
        phone_content = f.read()
        for order in orders:
            try:
                if str(order.Fuser_mobi) in str(phone_content):
                    continue
                phone_message = self.db.query(PhoneMessage).filter(PhoneMessage.Fphone==order.Fuser_mobi)
                if phone_message.count()>0:
                    continue
                if datetime.datetime.strftime(order.Fcreate_time,'%Y-%m-%d') in ('2015-06-11','2015-05-05'):
                    username = order.Fuser_name
                    mobile = order.Fuser_mobi
                    print mobile
                    print order.Fcreate_time
                    #mobile='18268802385'
                    msg_send = MessageThread(phone_msg_tempalte,mobile)
                    msg_send.start()
                    #send_message(mobile,phone_msg_tempalte)
                    print 'send one message'
                    #break
                    message  = PhoneMessage()
                    message.Frecive_user_id = order.Fuid
                    message.Fcontent = phone_msg_tempalte
                    message.Fphone = mobile
                    self.db.add(message)
                    self.db.commit()
                    index+=1
                    # if index>1000:
                    #     break
            except:
                pass
        print index
        self.write('发送成功')

    def post(self, *args, **kwargs):
        self.echo('')



