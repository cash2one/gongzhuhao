#encoding:utf-8
__author__ = 'binpo'

from common.base import BaseHandler
import ujson

class RestFullApiHandler(BaseHandler):

    '''重写四种方法'''
    def get(self, *args, **kwargs):
        '''
        查询
        :param args:
        :param kwargs:
        :return:
        '''
        data={'stat':'1000','data':{},'info':'get 请求'}
        self.write(ujson.dumps(data))

    def post(self, *args, **kwargs):
        '''
        :增加(创建)
        :param args:
        :param kwargs:
        :return:
        '''
        data={'stat':'1000','data':{},'info':'post 请求'}
        self.write(ujson.dumps(data))

    def put(self, *args, **kwargs):
        '''
        修改
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        print 'self.qdict:',self.qdict

        data={'stat':'1000','data':{},'info':'put 请求'}
        self.write(ujson.dumps(data))


    def delete(self, *args, **kwargs):
        '''
        :删除
        :param args:
        :param kwargs:
        :return:
        '''
        data={'stat':'1000','data':{},'info':'delete请求'}
        self.write(ujson.dumps(data))




'''

数据规范
api提供文档规范

1.API功能描述
2.请求路劲(通常包含测试路劲和线上正式环境路劲)
3.请求参数
4.请求方法(常用的 get,post,put,delete)
5.返回值
6.如果有加密,提供加解密规范
7.测试用例


用例如下
1.话题查询功能
2.请求路劲
    线上环境:m.gongzhuhao.com/v1/topic/api/
    测试环境:127.0.0.1:8008/v1/topic/api/

3.参数描述
    -------------------------------------------------
    |参数名称    |参数类型  |是否必须    |参数描述       |
    -------------------------------------------------
    |page       |int      |否         |页码 第几页    |
    -------------------------------------------------
    |topic_id   |int      |否         |话题ID        |
    -------------------------------------------------
    |category_id|int      |否         |话题类型ID     |
    -------------------------------------------------
    备注:page和topic_id 不能同时为空

4.GET 请求
5.返回值
    -------------------------------------------------
    |返回值名称     |数据类型  |是否必须    |参数描述    |
    -------------------------------------------------
    |state         |str      |是         |状态码     |
    -------------------------------------------------
    |data          |dict     |是         |返回数据内容|
    -------------------------------------------------
    |info          |返回描述  |是         |返回值描述  |
    -------------------------------------------------
    state:
        1000:成功
        1001:xxx错误
        1002:xxxx错误
        1003:xxxx错误
6.参数无加密

7.测试用例
    正确请求:
        param1={
                'page':0,
                'category_id':'2'
            }
        result1={
                'state':'1000'
                'data':{'topic_list':[{'id':1........},{'id':2....}.......]}
                'info':''
            }

    错误请求:
        param1={
                'category_id':'2'
            }
        result1={
                'state':'1001'
                'data':{}
                'info':'请求参数错误'
            }

备注加密规范:
import hmac
from hashlib import sha256

def generate_sig(endpoint, params, secret):
    sig = endpoint
    for key in sorted(params.keys()):
        sig += '|%s=%s' % (key, params[key])
    return hmac.new(secret, sig, sha256).hexdigest()

endpoint = '/media/657988443280050001_25025320'
params = {
    'access_token': 'fb2e77d.47a0479900504cb3ab4a1f626d174d2d',
    'count': 10,
}
secret = '6dc1787668c64c939929c17683d7cb74'

sig = generate_sig(endpoint, params, secret)
print sig
'''




class RestHtmlHandler(BaseHandler):

    def get(self, *args, **kwargs):
        self.echo('demo/test_restfull.html',layout='')