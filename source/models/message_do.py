#encoding:utf-8
__author__ = 'zhaowenpeng'

from base_do import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, SmallInteger,Text
from sqlalchemy.sql.functions import now

class MessageInfo(Base):
    '''
      用户消息 废弃
    '''
    __tablename__='message_info'

    FTYPE = {0:'公共消息',1:'评论',2:'私信',3:'赞'}            #消息类型定义

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer)  #消息体id

    info_type = Column(SmallInteger, default=0)                  #消息类型
    receiver = Column(Integer,index=True)                #消息接受者
    is_read = Column(Boolean,default=False)              #消息状态  0.为未读  1.已读
    is_pending = Column(Boolean,default=False)             #是否打开

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)


class MessageText(Base):
    '''
    消息体  废弃
    '''
    __tablename__='message_text'

    FTYPE = {'private':'私人消息','all':'公共消息','merchant':'商户消息','admin':'管理员消息', 'system': '系统消息'}     #消息类型定义

    id = Column(Integer, primary_key=True)

    text_type = Column(String(128), default='private', index=True)                  #消息类型
    sender = Column(Integer)                             #消息发送者
    link = Column(String(256))                           #消息的跳转链接
    data = Column(Text)                                  #消息内容
    is_read = Column(Boolean,default=False)              #消息状态  0.为未读  1.已读
    is_pending = Column(Boolean,default=False)             #是否打开

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)

class Message(Base):
    '''
    消息体  废弃
    '''
    __tablename__='message'

    FTYPE = {'private':'私人消息','all':'公共消息','merchant':'商户消息','admin':'管理员消息', 'system': '系统消息'}     #消息类型定义
    TEXT_TYPE = {0:'公共消息',1:'评论',2:'私信',3:'赞'}                                                              #内容定义

    id = Column(Integer, primary_key=True)
    message_type = Column(String(128), default='private')                   #消息类型
    content_type = Column(SmallInteger, default=0)                          #消息类型
    content = Column(String(2048),default='消息内容')
    refer_id = Column(Integer,doc='相关ID')
    sender = Column(Integer,doc='发送者')                      #发送者
    receiver = Column(Integer,doc='消息接受者')                #消息接受者

    is_read = Column(Boolean,default=False)              #消息状态  0.为未读  1.已读
    is_pending = Column(Boolean,default=False)             #是否打开

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)


class PhoneMessage(Base):
    '''
        手机短信记录
    '''
    __tablename__='t_phone_message'

    Fid = Column(Integer, primary_key=True)
    Frecive_user_id = Column(Integer)
    Fcontent = Column(Text)
    Fphone = Column(String(32))

    gmt_created = Column(DateTime,default=now())
    gmt_modified = Column(DateTime,default=now())
    deleted = Column(Boolean,default=False)

'''
{
    nid: { type: String, unique: true },
    published: { type: Number, default: Date.now },
    verb: { type: String },
    template: { type: String },
    is_read: { type: Number, index: true, default: 0 },
    is_pending: { type: Number, index: true, default: 0 },
    filter: {
        ftype: { type: String }
    },
    sender: { type: Actor },
    receiver : { type: String , index: true},
    data: {
        entity: { type: Entity },
        source: { type: Entity },
        target: { type: Entity }
    }
}
'''