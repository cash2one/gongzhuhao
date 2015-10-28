#encoding:utf-8
__author__ = 'binpo'

from models.base_do import Base
from sqlalchemy import Column,Integer,String,DateTime,Boolean,SmallInteger,Date,Text
from sqlalchemy.sql.functions import now
from sqlalchemy import event

class TopicBanner(Base):

    __tablename__ = 't_topic_banners'

    Fid = Column(Integer, primary_key=True)
    Fbanner_type = Column(Boolean)                      # 0手机,1 PC电脑

    Ftitle = Column(String(32))                          #标题
    Fimg_url = Column(String(256),default='',nullable=True)
    Flink_url = Column(String(256),nullable=True,default='')
    Finvalid_date = Column(Date,nullable=True,default='',doc='结束时间')

    Fcreate_time = Column(DateTime, default=now())      #创建日期
    Fmodify_time = Column(DateTime, default=now())      #修改日期
    Fdeleted = Column(Boolean, default=0)


class Tags(Base):
    __tablename__ = 't_tags'

    Fid = Column(Integer, primary_key=True)
    Ftag_name = Column(String(32))                      #标签名称
    Fcreate_time = Column(DateTime, default=now())      #创建日期
    Fmodify_time = Column(DateTime, default=now())      #修改日期
    Fdeleted = Column(Boolean, default=0)

class TopicCategory(Base):
    __tablename__ = 't_topic_category'

    Fid = Column(Integer, primary_key=True)
    Fname = Column(String(32))   #分类名称
    Fcode = Column(String(128),default='',doc='代码')
    Fparent_id = Column(Integer,nullable=True,doc='父级目录')
    Flevel = Column(SmallInteger,default=1)
    Fsort = Column(SmallInteger,default=0)
    Fimg_url = Column(String(256),doc='图片URL')
    Fdescription = Column(String(256),doc='分类描述',default='')
    Fpage_view = Column(Integer,default=0)              #浏览量
    Ftopic_count = Column(Integer,default=0)            #话题数量
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class TopicRoles(Base):

    __tablename__ = 't_topic_roles'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(String(128), default='',doc='代码')
    Fname = Column(String(128), default='',doc='名称')
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class TopicUserRoles(Base):

    __tablename__ = 't_topic_user_roles'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(String(128), default='',doc='代码')
    Fname = Column(String(128), default='',doc='名称')
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class Topics(Base):
    """话题/论坛"""
    __tablename__ = 't_topics'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)   #用户ID
    Fcotegory_id = Column(Integer,doc='分类ID')
    Ftitle = Column(String(32), nullable=False)   #标题
    Fcontent = Column(Text,default='')       #话题内容
    Ftotal_img = Column(Integer,default=0)      # 总图片数

    Fis_top = Column(Boolean,default=0,doc='是否置顶')
    Ftop_end_date = Column(DateTime,doc='置顶到最后时间')    #
    Fis_essence = Column(Boolean,default=0,doc="精华")                           #是否是精华帖
    Fessence_expire_time = Column(DateTime,doc="精华过期时间")                           #精华过期时间
    Fis_hot = Column(Boolean,default=0,doc='热门')
    Ftags = Column(String(256),doc='标签',default='')
    Fis_lock = Column(Boolean,default=0,doc='锁定')

    Fpage_view = Column(Integer,default=0)                  #浏览量
    Ftotal_assess= Column(Integer,default=0)                #评论数
    Fpraise = Column(Integer,default=0)                     #点赞数

    Fis_recommend = Column(Boolean,default=0,doc="是否推荐")
    Fedit_times = Column(Integer,default=0) #编辑次
    Flast_edit_time = Column(DateTime, default=now())    #最后编辑日期

    Flast_reply_time = Column(DateTime,default=now())       #最后回复事件
    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class TopicImages(Base):
    """话题/论坛"""
    __tablename__ = 't_topic_images'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)   #用户ID
    Ftopic_id = Column(Integer,doc='话题ID')
    Fimg_id = Column(Integer,doc='图片ID')            #图片ID
    Fimg_size = Column(Integer,doc='图片大小')
    Fimg_url = Column(String(256),doc='图片URL')        #图片URL
    Fremark = Column(String(256),doc='图片描述',default='') #图片描述

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class TopicReply(Base):

    __tablename__='t_topic_reply'

    Fid = Column(Integer, primary_key=True)
    Freply_index = Column(Integer,doc='同一话题回帖序号')
    Fuser_id = Column(Integer)   #用户ID
    Fparent_user_id = Column(Integer,nullable=True)   #用户ID
    Ftopic_id = Column(Integer,doc='话题ID')
    Fparent_id = Column(Integer,doc='回复ID',default=0)             #回复ID
    Ffull_parent_id = Column(String(512),doc='全路径',default='0')  #全路径ID
    Fcontent = Column(Text,default='')                             #回复内容
    Fpraise = Column(Integer,default=0)                             #点赞数

    Fis_top = Column(Boolean,default=0,doc='是否置顶')
    Fis_prime = Column(Boolean,default=0,doc='是否精华')
    Ftags = Column(String(256),doc='标签',default='')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class TopicReplyImages(Base):
    """话题/论坛"""
    __tablename__ = 't_topic_reply_images'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)   #用户ID
    Ftopic_id = Column(Integer,doc='话题ID')
    Fimg_id = Column(Integer,doc='图片ID')            #图片ID
    Fimg_url = Column(String(256),doc='图片URL')                   #图片URL
    Fimg_size = Column(Integer,doc='图片大小')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)

class UserJoinTopic():
    '''用户加入的板块'''
    __tablename__='t_user_join_category'

    Fid = Column(Integer, primary_key=True)
    Fuser_id = Column(Integer)   #用户ID
    Ftopic_category = Column(Integer,doc='话题ID')

    Fcreate_time = Column(DateTime, default=now())     #创建日期
    Fmodify_time = Column(DateTime, default=now())    #修改日期
    Fdeleted = Column(Boolean, default=0)


class UserTopicSns(Base):

    __tablename__ = 't_user_topic_sns'

    Fid = Column(Integer, primary_key=True)
    Fuser_id=Column(Integer,doc='收藏的用户')
    Ftopic_id=Column(Integer,doc='id')
    Fsns_type = Column(SmallInteger,doc='操作类型')             # 1.点赞  2.关注
    Ftopic_type = Column(SmallInteger,doc='话题类型')            # 1.topic 2.跟帖
    Fcreate_time = Column(DateTime,default=now())               #创建日期
    Fmodify_time = Column(DateTime,default=now())               #修改日期
    Fdeleted = Column(Boolean, default=0)                       #默认存在

#
# class TopicPraise():
#     '''
#         用户点赞
#     '''
#     __tablename__='t_topic_Praise'
#
#     Fid = Column(Integer, primary_key=True)
#     Fuser_id = Column(Integer)   #用户ID
#     Ftopic_id = Column(Integer,doc='话题ID')
#
#     Fcreate_time = Column(DateTime, default=now())     #创建日期
#     Fmodify_time = Column(DateTime, default=now())    #修改日期
#     Fdeleted = Column(Boolean, default=0)
#
# @event.listens_for(Topics, "before_insert", propagate=True)
# def my_listener_function(mapper,conn,object):
#     object.Fmodify_time=now()

@event.listens_for(Topics, "after_insert", propagate=True)
def topic_category_count_listener(mapper,conn,object):
    connection=conn.connect()
    sql = 'update t_topic_category set Ftopic_count=Ftopic_count+1 where Fid='+str(object.Fcotegory_id)
    connection.execute(sql)
    # connection.transaction.commit()
    connection.close()

@event.listens_for(TopicReply, 'after_insert')
def after_insert_listener(mapper, conn, target):
    connection=conn.connect()
    import datetime
    current_time = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
    sql = 'update t_topics set Flast_reply_time="'+current_time+'" where Fid='+str(target.Ftopic_id)
    connection.execute(sql)
    connection.close()

@event.listens_for(TopicImages, 'after_insert')
def after_insert_listener(mapper, conn, target):
    connection=conn.connect()
    sql = 'update t_topics set Ftotal_img=Ftotal_img+1 where Fid='+str(target.Ftopic_id)
    connection.execute(sql)
    connection.close()
