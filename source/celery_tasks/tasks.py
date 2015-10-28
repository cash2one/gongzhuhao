#!/usr/bin/env python2.7
# encoding:utf-8
from __future__ import absolute_import

__author__ = 'dozy-sun'

import time

from celery_tasks.base import DatabaseTasks
from celery_tasks.celery import app
import requests
import ujson
from services.message.message_service import MessageService
msg_db = MessageService()

# @app.task(base=DatabaseTasks)
# def create_user_message(**kwargs):
#     print 'user_message 20'
#     print kwargs
#     msg_db.set_db(create_user_message.db)
#     kwargs['msg_id'] = msg_db.create_msg_text(**kwargs)
#     if kwargs.get('info_type') or kwargs.get('text_type') and kwargs['text_type'] == 'private':
#         msg_db.create_msg_info(**kwargs)
#     create_user_message.db.close()
#     return True

@app.task(base=DatabaseTasks)
def create_user_message(**kwargs):
    # text_type  消息体类型  {'private':'私人消息','all':'公共消息','merchant':'商户消息','admin':'管理员消息', 'system': '系统消息'}  默认 private
    # 'info_type':  消息类型   0:'公共消息',1:'评论',2:'私信',3:'赞'  默认0
    # 'sender_id':   #发送者id
    # 'receiver_id': #接受者id  可以为list
    # 'title':  #消息标题
    # 'link':  #消息链接
    # 'data':   #消息内容
    if not kwargs['receiver_id'] or not kwargs['sender_id']:
        return False,'接收发送者不能空'

    kwargs['text_type'] = 'private' if not kwargs.get('text_type','') else kwargs['text_type']
    msg_db.set_db(create_user_message.db)
    kwargs['msg_id'] = msg_db.create_msg_text(**kwargs)

    if kwargs.get('info_type') and kwargs.get('text_type') and kwargs['text_type'] == 'private':
        msg_db.create_msg_info(**kwargs)
    create_user_message.db.close()
    return True,''

@app.task()#base=DatabaseTasks)
def send_msg_with_celery(phone,content):
    try:
        resp = requests.post(("https://sms-api.luosimao.com/v1/send.json"),
        auth=("api", "key-0620cf5610cc3f90ddb93041f0babd51"),
        data={
            "mobile": phone,
            "message": content
        },timeout=3 , verify=False)
        result = ujson.loads(resp.content)
        print result
    except :
        pass