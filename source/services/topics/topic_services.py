#encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.topic_do import TopicCategory,Topics,TopicReply,TopicImages,TopicReplyImages,Tags,UserTopicSns,TopicBanner
from sqlalchemy.sql import or_
import re
import datetime

class TopicServices(BaseService):

    def get_category_list(self):
        '''
        :todo 获取话题所有列表
        :return: query
        '''
        return self.db.query(TopicCategory).filter(TopicCategory.Fdeleted==0).order_by('Fsort')


    def query_topics_by_category(self,category_id=None,order_by=None):
        '''
        :todo 根据类型ID查询所有话题
        :param category_id:
        :return: topic_list
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted==0)
        if category_id:
            query = query.filter(Topics.Fcotegory_id==category_id)
        if order_by:
            query = query.order_by(order_by)
        return query

    def get_topic_detail_by_id(self,topic_id,user_id=None):
        '''
        :todo 获取话题的detail
        :param topic_id:
        :return: topic obj和图片
        '''
        topic = self.db.query(Topics).filter(Topics.Fdeleted==0,Topics.Fid==topic_id)
        images = self.db.query(TopicImages).filter(TopicImages.Fdeleted==0,TopicImages.Ftopic_id==topic_id)
        if user_id:
            topic = topic.filter(Topics.Fuser_id==user_id)
            images = images.filter(TopicImages.Fuser_id==user_id)
        return topic.scalar(),images

    def get_replies_by_topic_id(self,topic_id):
        '''
        :todo 根据话题id查询所有的回复
        :param topic_id:
        :return:
        '''
        pass


    def delete_topic_by_id(self,user_id,topic_id):
        '''
        :todo 删除话题
        :param user_id:
        :param topic_id:
        :return:
        '''


    def create_topic_tag(self,**kwargs):
        '''
        todo:创建标签
        :param kwargs:
        :return:
        '''
        tag = Tags()
        tag.Ftag_name = kwargs.get('tag_name','')
        self.db.add(tag)
        self.db.commit()

    def query_topic_tags(self):
        '''
        todo:查询标签
        :param kwargs:
        :return:query
        '''
        query = self.db.query(Tags).filter(Tags.Fdeleted == 0)
        return query

    def create_topic_category(self,**kwargs):
        '''
        todo:创建话题分类
        :param kwargs:
        :return:topic_category
        '''
        topic_category = TopicCategory()
        topic_category.Fname = kwargs.get('category_name','')
        topic_category.Fdescription = kwargs.get('category_description','')
        if 'parent_id' in kwargs:
            topic_category.Fparent_id = int(kwargs.get('parent_id',''))
            topic_category.Flevel = self.get_category_by_id(kwargs.get('parent_id')).Flevel+1 #父级话题的级别加1
        self.db.add(topic_category)
        self.db.commit()
        return topic_category


    def get_category_by_id(self,topic_category_id):
        '''
        todo:根据id查找话题分类
        :param topic_category_id:话题分类id
        :return:topic_category
        '''
        return self.db.query(TopicCategory).filter(TopicCategory.Fdeleted == 0,TopicCategory.Fid == topic_category_id).scalar()

    def update_category(self,topic_category_id,**kwargs):
        '''
        todo:更新；删除话题分类
        :param topic_category_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(TopicCategory).filter(TopicCategory.Fdeleted == 0,TopicCategory.Fid == topic_category_id)
        query.update(kwargs)
        self.db.commit()

    def query_topic_category(self,parent_id = None,order_by = None):
        '''
        todo:获取话题分类
        :return:query
        '''
        query = self.db.query(TopicCategory).filter(TopicCategory.Fdeleted == 0)
        if parent_id:
            query = query.filter(TopicCategory.Fparent_id == parent_id)
        else:
            query = query.filter(TopicCategory.Flevel == 1)
        if order_by:
            query = query.order_by(order_by)
        return query

    def create_topic(self,**kwargs):
        '''
        todo:创建话题
        :param kwargs:
        :return:topic
        '''
        topic = Topics()
        topic.Fuser_id = int(kwargs.get('user_id'))
        topic.Fcotegory_id = int(kwargs.get('category_id'))
        topic.Ftitle = kwargs.get('title','')
        topic.Fcontent = re.sub(r'\n','<br/>',kwargs.get('content',''))
        self.db.add(topic)
        self.db.commit()
        return topic

    def query_imgCount(self,user_id,topic_id):
        '''
        todo:根据用户ID，话题ID查询照片数量
        :param user_id:
        :param topic_id:
        :return:count
        '''
        sql = "select count(*) from t_topic_images where Fdeleted = 0 and Fuser_id={0} and Ftopic_id={1}"
        count = self.db.execute(int(user_id),int(topic_id))
        return count

    def query_topics(self,order_by=None,**kwargs):#category_id = None
        '''
        todo:获取非置顶；精华话题
        :param category_id:话题分类id
        :return:query
        '''
        # order_by(' Fcreate_time desc ')
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_top == 0,Topics.Fis_essence == 0)
        if kwargs.get('category_id',''):
            query = query.filter(Topics.Fcotegory_id == kwargs.get('category_id'))
        if kwargs.get('user_id',''):
            query = query.filter(Topics.Fuser_id == kwargs.get('user_id'))
        if kwargs.get('content',''):
            content = kwargs.get('content')
            query = query.filter(Topics.Ftitle.like('%'+content+'%'))
        if order_by:
            query = query.order_by(order_by)
        return query

    def get_last_reply_topic_list(self,category_id):
        '''
        todo:获取最新回复话题
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fcotegory_id == category_id).order_by('Flast_reply_time desc')
        return query

    def check_end_date_topics(self,c_top=None,c_essence=None):
        '''
        todo:检查过期的置顶或者加精话题
        :return:
        '''
        now = datetime.datetime.now()
        if c_top and int(c_top):
            query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_top ==1,Topics.Ftop_end_date < now)
            if query.count() > 0:
                query.update({'Fis_top':0,'Ftop_end_date':None})
                self.db.commit()
        if c_essence and int(c_essence):
            query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_essence == 1,Topics.Fessence_expire_time < now)
            if query.count() > 0:
                query.update({'Fis_essence':0,'Fessence_expire_time':None})
                self.db.commit()

    def get_topic_list(self,order_by=None,is_top=None,is_essence=None,**kwargs):
        '''
        todo:获取话题list
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0)
        if kwargs.get('category_id',''):
            query = query.filter(Topics.Fcotegory_id == kwargs.get('category_id'))
        if kwargs.get('user_id',''):
            query = query.filter(Topics.Fuser_id == kwargs.get('user_id'))
        if kwargs.get('topic_title',''):
            topic_title = kwargs.get('topic_title')
            query = query.filter(Topics.Ftitle.like('%'+topic_title+'%'))
        if is_top or is_essence:
            query = query.filter(or_(Topics.Fis_top == is_top,Topics.Fis_essence == is_essence))
        if order_by:
            query = query.order_by(order_by)
        return query

    def get_topic_by_id(self,topic_id,topic_type=None):
        '''
        todo:根据id查询话题
        :param topic_id: 话题ID
        :param user_id: 用户ID
        :return:
        '''
        if topic_type == 'topic_':
            query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fid == topic_id).scalar()
        elif topic_type == 'reply_':
            query = self.db.query(TopicReply).filter(TopicReply.Fdeleted == 0,TopicReply.Fid == topic_id).scalar()
        return query

    def update_topic(self,topic_id,**kwargs):
        '''
        todo:根据ID更新，删除话题
        :param topic_id:话题ID
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fid == topic_id)
        query.update(kwargs)
        self.db.commit()

    def create_topic_img(self,topic_id,user_id,img_url,img_type,img_size):
        '''
        todo:创建话题图片
        :param topic:
        :param img_url:图片url
        :return:
        '''
        if img_type == 'topic':
            topic_img = TopicImages()
        else:
            topic_img = TopicReplyImages()
        topic_img.Ftopic_id = topic_id
        topic_img.Fuser_id = user_id
        topic_img.Fimg_url = img_url
        topic_img.Fimg_size = img_size
        self.db.add(topic_img)
        self.db.commit()
        # return topic_img.Fid


    def create_topic_reply(self,**kwargs):
        '''
        todo:创建话题回复
        :param kwargs:
        :return:
        '''
        topic_reply = TopicReply()
        topic_reply.Fuser_id = kwargs.get('user_id','')
        topic_reply.Ftopic_id = kwargs.get('topic_id','')

        topic_index = self.get_max_index(kwargs.get('topic_id'))
        topic_reply.Freply_index = topic_index+1

        topic_reply.Fparent_id = kwargs.get('parent_id',0)
        topic_reply.Fcontent = re.sub(r'\n','<br/>',kwargs.get('content',''))
        topic_reply.Ffull_parent_id = kwargs.get('full_parent_id')
        if topic_reply.Fparent_id==0:
            topic_reply.Fparent_user_id = self.db.query(Topics.Fuser_id).filter(Topics.Fdeleted==0,Topics.Fid==topic_reply.Ftopic_id).scalar()
        else:
            topic_reply.Fparent_user_id = self.db.query(TopicReply.Fuser_id).filter(TopicReply.Fdeleted==0,TopicReply.Fid==topic_reply.Fparent_id).scalar()
        self.db.add(topic_reply)
        if topic_reply.Fparent_id == 0:
            self.db.query(Topics).filter(Topics.Fid==kwargs.get('topic_id')).update({Topics.Ftotal_assess:Topics.Ftotal_assess+1})
        self.db.commit()
        return topic_reply

    def get_topic_reply_list(self,topic_id=None,parent_id=None,full_parent_id=None,order_by=None):
        '''
        todo:根据话题id获取回复
        :param topic_id: 话题ID
        :return:
        '''
        query = self.db.query(TopicReply).filter(TopicReply.Fdeleted == 0)
        if topic_id:
            query = query.filter(TopicReply.Ftopic_id == topic_id)
        if parent_id or parent_id == 0:
            query = query.filter(TopicReply.Fparent_id == parent_id)
        return query


    # def get_reply_images_list(self,topic_id,user_id):
    #     '''
    #
    #     :param topic:
    #     :return:
    #     '''
    #     return self.db.query(TopicReplyImages).\
    #         filter(TopicReplyImages.Fdeleted == 0,TopicReplyImages.Ftopic_id == topic_id,TopicReplyImages.Fuser_id == user_id)

    def get_max_index(self,topic_id):
        '''
        todo:获取同一话题的回帖最大序号
        :param topic_id:
        :return:
        '''
        sql = 'select count(*) from t_topic_reply where Ftopic_id ={0} and Fdeleted = 0'
        count = self.db.execute(sql.format(int(topic_id)))
        for c in count:
            return c[0]
        # return count[0]

    def update_topic_reply(self,topic_reply_id,**kwargs):
        '''
        todo:更新，删除回复
        :param topic_reply_id:回复ID
        :param kwargs:
        :return:
        '''
        query = self.db.query(TopicReply).filter(TopicReply.Fdeleted == 0,TopicReply.Fid == topic_reply_id)
        query.update(kwargs)
        self.db.commit()

    def get_topic_images_list(self,topic_id,type=None):
        '''
        todo:获取话题图片list
        :param topic_id:话题ID
        :param user_id:用户ID
        :return:query
        '''
        if type == 'topic':
            query = self.db.query(TopicImages).\
                filter(TopicImages.Fdeleted == 0,TopicImages.Ftopic_id == topic_id)
        elif type == 'reply':
            query = self.db.query(TopicReplyImages).\
                filter(TopicReplyImages.Fdeleted == 0,TopicReplyImages.Ftopic_id == topic_id)
        return query

    def create_topic_sns(self,topic_id,user_id,sns_type,topic_type,operation=0):
        '''
        :收藏,点赞,删除收藏,删除点赞
        :param topic_id: 话题ID或者回复ID
        :param user_id: 用户ID
        :param operation:
        :param topic_type:标识是类型还是回复
        :param db_operation:
        :param sns_id:
        :return:
        '''
        if operation==1:
            user_topic = UserTopicSns()
            user_topic.Fuser_id=user_id
            user_topic.Ftopic_id=topic_id
            user_topic.Fsns_type = sns_type             # 1.点赞  2.关注
            user_topic.Ftopic_type = topic_type           # 1.topic 2.topic_reply
            self.db.add(user_topic)
            self.db.commit()
        elif operation==0:
            topic_sns = self.db.query(UserTopicSns).filter(UserTopicSns.Ftopic_id==topic_id,
                                                           UserTopicSns.Fuser_id==user_id,
                                                           UserTopicSns.Fsns_type==sns_type,
                                                           UserTopicSns.Ftopic_type==topic_type)
            if topic_sns.count()>=1:
                for sns in topic_sns:
                    self.db.delete(sns)
                    self.db.commit()


    def create_topic_banner(self,**kwargs):
        '''
        todo:创建banner图
        :param kwargs:
        :return:
        '''
        topic_banner = TopicBanner()
        topic_banner.Fbanner_type = kwargs.get('banner_type')
        topic_banner.Ftitle = kwargs.get('title')
        topic_banner.Fimg_url = kwargs.get('img_url')
        topic_banner.Flink_url = kwargs.get('link_url','')
        topic_banner.Finvalid_date = kwargs.get('invalid_date','')
        self.db.add(topic_banner)
        self.db.commit()
        return topic_banner

    def get_topic_banner_list(self,limit=3,order_by=None):
        '''
        todo:获取banner图片
        :return:
        '''
        query = self.db.query(TopicBanner).filter(TopicBanner.Fdeleted == 0)
        if order_by:
            query = query.order_by(order_by)
        if limit:
            query = query.limit(limit).offset(0)
        # else:
        #     query = query.order_by('Fcreate_time desc')
        return query

    def check_sns_exist(self,user_id,topic_id,sns_type):
        '''
        todo:判断用户是否点赞
        :param user_id:
        :param topic_id:
        :return:
        '''
        query = self.db.query(UserTopicSns).\
            filter(UserTopicSns.Fdeleted == 0,UserTopicSns.Fuser_id == user_id,
                   UserTopicSns.Ftopic_id == topic_id,UserTopicSns.Fsns_type == sns_type)
        if query.count()>=1:
            return True
        else:
            return False

    def get_hot_topics_list(self):
        '''
        todo:获取热门话题列表
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_hot == 1)
        return query


    def get_sns_topics_list(self,user_id=None,topic_id=None,sns_type=None):
        '''
        todo:获取用户关注话题
        :param user_id:
        :return:
        '''
        if user_id:
            query = self.db.query(UserTopicSns)\
                .filter(UserTopicSns.Fdeleted == 0,UserTopicSns.Fuser_id == user_id,UserTopicSns.Fsns_type == sns_type)
        if topic_id:
            query = self.db.query(UserTopicSns)\
                .filter(UserTopicSns.Fdeleted == 0,UserTopicSns.Ftopic_id == topic_id,UserTopicSns.Fsns_type == sns_type)
        return query

    def get_reply_of_reply(self,reply_id):
        '''
        :todo 获取回复的回复list
        :param reply_id:
        :return:
        '''
        replies = self.db.query(TopicReply).filter(TopicReply.Ffull_parent_id.like('%/'+str(reply_id)+'/%'))
        total_count = replies.count()
        reply_list = replies.order_by('Fcreate_time')
        return total_count,reply_list


    def query_user_topics(self,user_id):
        '''
        :获取用户的所有topics
        :param user_id:
        :return:
        '''
        return self.db.query(Topics).filter(Topics.Fdeleted==0,Topics.Fuser_id==user_id).order_by('Fcreate_time desc ')

    def get_imgaes_by_topic_id(self,topic_id):
        '''
        :获取话题图片
        :param topic_id:
        :return:
        '''
        return self.db.query(TopicImages).filter(TopicImages.Fdeleted==0,TopicImages.Ftopic_id==topic_id).order_by('Fcreate_time desc ')


    def get_user_replies(self,user_id):
        '''
        :获取用户回复
        :param user_id:
        :return:
        '''
        return self.db.query(TopicReply).filter(TopicReply.Fdeleted==0,TopicReply.Fuser_id==user_id).order_by('Fcreate_time desc ')

    # def get_topics(self):
    #
    #     now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Ftop_end_date < now)
    #     return query
