#encoding:utf-8
__author__ = 'binpo'

from models.message_do import MessageInfo,MessageText
from ..base_services import BaseService
from utils.date_util import yyyydddddatetime
from models.message_do import Message

class MessageService(BaseService):

    def create(self,sender_id,recieve_id,message_type,content_type,content,refer_id):

        message = Message()
        message.message_type = message_type                 #消息类型
        message.content_type = content_type                          #消息类型
        message.content = content
        message.refer_id = refer_id
        message.sender = sender_id                     #发送者
        message.receiver = recieve_id                #消息接受者
        self.db.add(message)
        self.db.commit(message)


    def query_message_by_user_id(self,user_id):
        pass

    # def create_msg_text(self,**kwargs):
    #     #创建消息体
    #     message = MessageText()
    #     if kwargs.has_key('type_code'):
    #         message.type_code = kwargs['type_code']                 #消息类型
    #     message.sender_id = kwargs.get('sender_id', 0)              #消息接受者
    #     message.link = kwargs.get('link')                  #链接
    #     message.title = kwargs.get('title')
    #     message.data = kwargs.get('data')                #消息内容
    #     self.db.add(message)
    #     self.db.commit()
    #     return message.id
    #
    # def create_msg_info(self,**kwargs):
    #     #创建用户消息
    #     if isinstance(kwargs['receiver_id'], list):
    #         for r in kwargs['receiver_id']:
    #             message = MessageInfo()
    #             if kwargs.has_key('type_code'):
    #                 message.type_code = kwargs['type_code']                 #消息类型
    #             message.message_id = kwargs['msg_id']              #消息接受者
    #             message.info_type = kwargs.get('info_type', 0)                   #类型
    #             message.receiver_id = r                #消息内容
    #             self.db.add(message)
    #     else:
    #         message = MessageInfo()
    #         # if kwargs.has_key('type_code'):
    #         #     message.type_code = kwargs['type_code']                 #消息类型
    #         message.message_id = kwargs['msg_id']              #消息接受者
    #         message.info_type = kwargs.get('info_type', 0)                   #类型
    #         message.receiver_id = kwargs['receiver_id']                #消息内容
    #         self.db.add(message)
    #     self.db.commit()
    #
    # def update_msg_from_message_text(self, user_id, read=0):
    #     #更新公共消息 到用户消息表
    #     msg_id = self.db.query(MessageText.id).filter(MessageInfo.receiver == user_id, MessageInfo.message_id != MessageText.id , MessageText.text_type != 'private', MessageText.deleted == 0).all()
    #     time_now = yyyydddddatetime()
    #     if msg_id:
    #         self.db.execute(
    #             MessageInfo.__table__.insert(),[{'message_id': ids[0],'info_type':0, 'receiver_id':user_id, 'is_read': read,'gmt_created': time_now, 'gmt_modified': time_now ,'deleted': 0} for ids in msg_id]
    #         )
    #         self.db.commit()
    #
    # def query_messages(self, user_id, unread=False,text_type='private'):
    #     query = self.db.query(MessageText, MessageInfo).filter(MessageText.text_type == text_type, MessageText.deleted ==0, MessageText.id == MessageInfo.message_id, MessageInfo.receiver_id == user_id)
    #     if unread:
    #         query = query.filter(MessageInfo.is_read == 0)
    #     return query.order_by(MessageInfo.gmt_created.desc())
    #
    # def update_msg_status(self, user_id ,msg_id, **kwargs):
    #     query = self.db.query(MessageInfo).filter(MessageInfo.receiver_id == user_id, MessageInfo.id == msg_id)
    #     query.update(kwargs)
    #     self.db.commit()
    #
    # def update_message_open(self,user_id):
    #     '''
    #     :关闭消息提醒
    #     :param user_id:
    #     :return:
    #     '''
    #     query = self.db.query(MessageInfo).filter(MessageInfo.receiver_id == user_id, MessageInfo.is_open == 0)
    #     query.update({'is_open':1})
    #     self.db.commit()
    #
    # def get_message_by_id(self,user_id,msg_id):
    #
    #     self.db.query(MessageInfo).filter(MessageInfo.receiver==user_id,MessageInfo.id==msg_id)
    #
    # def messages_format(self,messages,msglst):
    #     pass
    #
