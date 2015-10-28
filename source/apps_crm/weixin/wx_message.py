#encoding:utf-8
__author__ = 'sunlifeng'

class WX_MESSAGE:
    def __init__(self):
        pass

    REPLY_TEXT = '''
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[%s]]></Content>
    </xml>
    '''