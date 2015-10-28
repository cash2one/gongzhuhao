#encoding:utf-8

__author__ = 'sunlifeng'

import hashlib
from lxml import etree
import time
import urlparse

from common.base import BaseHandler
from wx_message import WX_MESSAGE
from contants import Constant
import sys
import traceback

class HelloHandler(BaseHandler):

    def get(self, m_id=None):
        try:
            self.echo('mobile/error.html', {'err_msg': "hello"})
        except Exception,e:
            e = sys.exc_info()[0](traceback.format_exc())
            print(e)

from services.company.company_services import CompanyServices

class AccessHandler(BaseHandler):

    def get(self,company_id=None):
        try:
            #获取输入参数
            query = self.request.query
            qdict = urlparse.parse_qs(query)
            print('AccessHandler get() qdict='+str(qdict))

            if not qdict:
                print('qdict is null.')
                return

            if not company_id:
                print('company_id is null.')
                return

            #获取token
            company_db = CompanyServices(self.db)
            company = company_db.get_company_by_id(int(company_id))
            if not company:
                print('no user!')
                return

            #校验
            isFromWeixin = self.checkSignature(company.Fapp_token, **qdict)

            if isFromWeixin:    #匹配成功
                print('weixin check ok!')
                if qdict.has_key('echostr'):
                    self.write(qdict.get('echostr')[0])
                else:
                    self.write('')
            else:
                print('weixin check error!')
                self.write('[ERROR]not Weixin!')
        except Exception,e:
            e = sys.exc_info()[0](traceback.format_exc())
            print(e)

            print('weixin access error!')

            return

    def post(self, company_id=None):
        #获取输入参数
        print('AccessHandler post()')
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        print('AccessHandler post() qdict='+str(qdict))

        if company_id:
            print('company_id='+str(company_id))
            #获取token
            company_db = CompanyServices(self.db)
            company = company_db.get_company_by_id(int(company_id))
            if not company:
                print('no company!')
                return

            #校验
            isFromWeixin = self.checkSignature(company.Fapp_token, **qdict)

            if not isFromWeixin:#匹配不成功
                print('not match!')
                self.write('')
                return
        else:
            print('no company id')
            self.write('')
            return

        nonce = qdict.get('nonce')[0]
        request_data = str(self.request.body)
        print('request_data='+request_data)

        request_xml = etree.fromstring(request_data)    #进行XML解析
        msgType = request_xml.find("MsgType").text
        fromUser = request_xml.find("FromUserName").text
        toUser = request_xml.find("ToUserName").text

        result_msg = ''
        print('msgType='+msgType)
        if msgType == 'event':#事件
            event = request_xml.find("Event").text  #获得事件内容
            print('event='+event)
            if event == 'subscribe':  #关注事件
                result_msg = WX_MESSAGE.REPLY_TEXT %(fromUser, toUser, int(time.time()), unicode('欢迎关注%s!' %(company.Fcompany_name)))
            elif event == 'unsubscribe':  #取消关注事件
                result_msg = ''
                #???后台清理
            elif event == 'CLICK':  #菜单点击事件
                eventKey = request_xml.find("EventKey").text  #获得事件KEY值
                print('eventKey='+eventKey)
                if eventKey == Constant.EVENT_CONTACT:  #联系我们
                    #读取联系信息
                    msgx_content = ''
                    if company.Fcompany_name:
                        msgx_content = msgx_content + u'名称：' + company.Fcompany_name + '\n'
                    if company.Faddress:
                        msgx_content = msgx_content + u'地址：' + company.Faddress + '\n'
                    if company.Fcontact:
                        msgx_content = msgx_content + u'联系人：' + company.Fcontact + '\n'
                    if company.Fphone:
                        msgx_content = msgx_content + u'电话：' + company.Fphone + '\n'
                    if company.Fqq:
                        msgx_content = msgx_content + u'QQ：' + company.Fqq + '\n'
                    if company.Fmail:
                        msgx_content = msgx_content + u'邮箱：' + company.Fmail
                    result_msg = WX_MESSAGE.REPLY_TEXT %(fromUser, toUser, int(time.time()), msgx_content)
            elif event == 'VIEW':  #取消关注事件
                eventKey = request_xml.find("EventKey").text  #获得事件KEY值
                print('VIEW url='+eventKey)
                #result_msg = WX_MESSAGE.REPLY_TEXT %(fromUser, toUser, int(time.time()), u'未绑定用户，请在菜单中进行绑定.')
                result_msg = nonce
        else:
            content = request_xml.find("Content").text  #获得用户所输入的内容
            result_msg = WX_MESSAGE.REPLY_TEXT %(fromUser, toUser, int(time.time()), unicode('欢迎关注%s!' %(company.Fcompany_name)))

        self.write(result_msg)

    def checkSignature(self, app_token, **kwargs):
        signature=kwargs.get('signature')[0]
        timestamp=kwargs.get('timestamp')[0]
        nonce=kwargs.get('nonce')[0]

        print(str(kwargs))
        print('app_token=' + app_token)

        #字典序排序
        list=[app_token, timestamp, nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hash_code = sha1.hexdigest()   #sha1加密算法

        #如果是来自微信的请求，则回复true
        if hash_code == signature:
            return True
        else:
            return False
