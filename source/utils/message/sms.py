#encoding:utf-8

import requests
import ujson
import threading

def send_phone_msg(phone,content):

    message_thread = MessageThread(content,phone)
    message_thread.start()
    # resp = requests.post(("https://sms-api.luosimao.com/v1/send.json"),
    # auth=("api", "key-0620cf5610cc3f90ddb93041f0babd51"),
    # data={
		# "mobile": phone,
		# "message": content
    # },timeout=3 , verify=False)
    # result = ujson.loads(resp.content)
    # return result

class MessageThread(threading.Thread):
    '''
        多线程发送消息
    '''

    def __init__(self,content,phone):

        threading.Thread.__init__(self)
        self.content = content
        self.phone = phone

    def run(self):
        try:
            resp = requests.post(("https://sms-api.luosimao.com/v1/send.json"),
            auth=("api", "key-0620cf5610cc3f90ddb93041f0babd51"),
            data={
                "mobile": self.phone,
                "message": self.content
            },timeout=3 , verify=False)
            result = ujson.loads(resp.content)
            print result
        except :
            pass

def send_message(phone,content):
    try:
        resp = requests.post(("https://sms-api.luosimao.com/v1/send.json"),
        auth=("api", "key-0620cf5610cc3f90ddb93041f0babd51"),
        data={
            "mobile":phone,
            "message":content
        },timeout=3 , verify=False)
        result = ujson.loads(resp.content)
        print result
    except :
        pass