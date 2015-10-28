#encoding:utf-8
__author__ = 'morichounami'

from apps_admin.message.message import MessageHandle,MessageIndex
handlers = [
    (r'/ops/message/index/',MessageIndex),
    (r'/ops/message/send/',MessageHandle)
]
