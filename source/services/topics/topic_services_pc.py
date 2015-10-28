 #encoding:utf-8
__author__ = 'binpo'
from ..base_services import BaseService
from models.topic_do import TopicCategory,Topics,TopicReply,TopicImages,TopicReplyImages,Tags,UserTopicSns,TopicBanner
from sqlalchemy.sql import or_,func
import re
from utils.date_util import yyyydddddatetime,time_of_seven_days_ago,time_of_a_month_ago
import datetime
import re

class TopicServices(BaseService):

    def get_category_list(self):
        '''
        :todo 获取话题所有列表
        :return: query
        '''
        return self.db.query(TopicCategory).filter(TopicCategory.Fdeleted==0).order_by('Fsort')


    def query_topics_by_category(self,category_id,order_by=None):
        '''
        :todo 根据类型ID查询所有话题
        :param category_id:
        :return: topic_list
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted==0,Topics.Fcotegory_id==category_id)
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

    def query_topic_tags(self,**kwargs):
        '''
        todo:查询标签
        :param kwargs:
        :return:query
        '''
        query = self.db.query(Tags).filter(Tags.Fdeleted == 0)
        if kwargs.get('start_date',''):
            query =  query.filter(Tags.Fcreate_time >= kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(Tags.Fcreate_time <= kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('tag_name',''):
            content = kwargs.get('tag_name')
            query = query.filter(Tags.Ftag_name.like('%'+content+'%'))
        #return self.db.query(Tags).filter(Tags.Fdeleted == 0)
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

    def query_topic_category(self,parent_id = None,order_by = 'Fsort'):
        '''
        todo:获取话题分类
        :return:query
        '''
        query = self.db.query(TopicCategory).filter(TopicCategory.Fdeleted == 0)
        if parent_id:
            query = query.filter(TopicCategory.Fparent_id == parent_id)
        else:
            query = query.filter(TopicCategory.Flevel == 1)
        return query.order_by(order_by)

    def query_topic_category_one(self,**kwargs):
        '''
        todo:获取话题分类
        :return:query
        '''
        query = self.db.query(TopicCategory).filter(TopicCategory.Fdeleted == 0)
        if kwargs.get('id'):
            query = query.filter(TopicCategory.Fid == kwargs['id'])
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
        print 'len_title:',len(kwargs.get('title'))
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
        if kwargs.get('content',''):
            content = kwargs.get('content')
            query = query.filter(or_(Topics.Ftitle.like('%'+content+'%'),Topics.Fcontent.like('%'+content+'%')))
        # if is_essence:
        #     query = query.filter(Topics.Fis_essence == is_essence)
        if order_by:
            query = query.order_by(order_by)
        return query

    def query_topics_all(self,**kwargs):#category_id = None
        '''
        todo:获取话题
        :param category_id:话题分类id
        :return:query
        '''
        # order_by(' Fcreate_time desc ')
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0)
        if kwargs.get('topic_id'):
            query = query.filter(Topics.Fid == kwargs.get('topic_id'))
        if kwargs.get('category_id',''):
            query = query.filter(Topics.Fcotegory_id == kwargs.get('category_id'))
        if kwargs.get('is_essence',''):
            query = query.filter(Topics.Fis_essence == kwargs.get('is_essence'))
        if kwargs.get('content',''):
            content = kwargs.get('content')
            query = query.filter(or_(Topics.Ftitle.like('%'+content+'%'),Topics.Fcontent.like('%'+content+'%')))
        if kwargs.get('start_time'):
            query = query.filter(Topics.Fcreate_time >= kwargs['start_time'])
        if kwargs.has_key('recommend'):
            query = query.filter(Topics.Fis_recommend == kwargs['recommend'])
        # if is_essence:
        #     query = query.filter(Topics.Fis_essence == is_essence)
        if kwargs.get('order_by', ''):
            query = query.order_by(kwargs['order_by'])
        return query

    def query_topic_imgs(self, topic_id):
        return self.db.query(TopicImages).filter(TopicImages.Ftopic_id == topic_id, TopicImages.Fdeleted == 0)

    def get_top_essence_topic_list(self,is_top=None,is_essence=None,**kwargs):
        '''
        todo:获取置顶,精华话题
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fcotegory_id == kwargs.get('category_id'))
        if is_top and is_essence:
            query = query.filter(or_(Topics.Fis_top == 1,Topics.Fis_essence == 1)).order_by('Fis_top desc')
        else:
            query = query.filter(Topics.Fis_essence == is_essence)
        return query

    def get_topic_by_id(self,topic_id,user_id=None):
        '''
        todo:根据id查询话题
        :param topic_id: 话题ID
        :param user_id: 用户ID
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fid == topic_id)
        if user_id:
            query.filter(Topics.Fuser_id == user_id)
        return query.scalar()

    def get_topic_reply(self,topic_id,user_id=None):
        '''
        todo:根据话题ID，用户ID查询话题恢复
        :param topic_id:
        :param user_id:
        :return:query
        '''
        query = self.db.query(TopicReply).filter(TopicReply.Fdeleted == 0,TopicReply.Fid == topic_id)
        if user_id:
            query.filter(TopicReply.Fuser_id == user_id)

        return query.scalar()
        # query = self.db.query(TopicReply).\
        #     filter(TopicReply.Fdeleted == 0,TopicReply.Ftopic_id == topic_id,TopicReply.Fuser_id == user_id)
        # return query

    def update_topic(self,topic_id,**kwargs):
        '''
        todo:根据ID更新，删除话题
        :param topic_id:话题ID
        :return:
        '''
        query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fid == topic_id)
        query.update(kwargs)
        if kwargs.has_key('Fdeleted'):
            self.db.query(TopicCategory).filter(TopicCategory.Fid==Topics.Fcotegory_id, Topics.Fid==topic_id).update({TopicCategory.Ftopic_count:TopicCategory.Ftopic_count-1})
        if kwargs.get('Fis_recommend'):
            self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fid != topic_id, Topics.Fis_recommend == 1).update({Topics.Fis_recommend:0})
        self.db.commit()

    def create_topic_img(self,topic_id,user_id,img_url,img_type,img_size, img_id=None):
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
        if img_id:
            topic_img.Fimg_id = img_id
        self.db.add(topic_img)
        self.db.commit()
        # return topic_img.Fid

    # def create_topic_img_2(self,**kwargs):
    #     '''
    #     :param topic:
    #     :param img_url:图片url
    #     :return:
    #     '''
    #     topic_reply_img = TopicReplyImages()
    #     topic_reply_img.Fuser_id = kwargs.get('user_id')
    #     topic_reply_img.Ftopic_id = kwargs.get('topic_id')
    #     topic_reply_img.Fimg_url = kwargs.get('url')
    #     self.db.add(topic_reply_img)
    #     self.db.commit()

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
        topic_reply.Fparent_id = int(kwargs.get('parent_id',0))
        if topic_reply.Fparent_id==0:
            topic_reply.Fparent_user_id = self.db.query(Topics.Fuser_id).filter(Topics.Fdeleted==0,Topics.Fid==topic_reply.Ftopic_id).scalar()
        else:
            topic_reply.Fparent_user_id = self.db.query(TopicReply.Fuser_id).filter(TopicReply.Fdeleted==0,TopicReply.Fid==topic_reply.Fparent_id).scalar()
        # if 'parent_id' in kwargs:
        #     topic_reply.Fparent_id = int(kwargs.get('parent_id'))
        # else:
        #     topic_reply.Fparent_id = 0
        topic_reply.Fcontent = re.sub(r'\n','<br/>',kwargs.get('content',''))
        self.db.add(topic_reply)
        if topic_reply.Fparent_id==0:
            self.db.query(Topics).filter(Topics.Fid==kwargs.get('topic_id')).update({Topics.Flast_reply_time: yyyydddddatetime(), Topics.Ftotal_assess:Topics.Ftotal_assess+1})
        self.db.commit()
        return topic_reply

    def get_topic_reply_list(self,topic_id, order_by = 'Fcreate_time asc '):
        '''
        todo:根据话题id获取回复
        :param topic_id: 话题ID
        :return:
        '''
        return self.db.query(TopicReply).\
            filter(TopicReply.Fdeleted == 0,TopicReply.Ftopic_id == topic_id,TopicReply.Fparent_id==0).order_by(order_by)

    def get_reply_images_list(self,topic_id,user_id=None):
        '''
        todo:
        :param topic:
        :return:
        '''
        query = self.db.query(TopicReplyImages).filter(TopicReplyImages.Fdeleted == 0,TopicReplyImages.Ftopic_id == topic_id)
        if user_id:
            query = query.filter(TopicReplyImages.Fuser_id == user_id)
        return query

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

    def get_topic_images_list(self,topic_id,user_id):
        '''
        todo:获取话题图片list
        :param topic_id:话题ID
        :param user_id:用户ID
        :return:query
        '''
        query = self.db.query(TopicImages).\
            filter(TopicImages.Fdeleted == 0,TopicImages.Ftopic_id == topic_id,TopicImages.Fuser_id == user_id)
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
        topic_sns = self.db.query(UserTopicSns).filter(UserTopicSns.Ftopic_id==topic_id,
                                                           UserTopicSns.Fuser_id==user_id,
                                                           UserTopicSns.Fsns_type==sns_type,
                                                           UserTopicSns.Ftopic_type==topic_type,UserTopicSns.Fdeleted==0)
        is_exist = topic_sns.first()
        if operation==1 and not is_exist:
            user_topic = UserTopicSns()
            user_topic.Fuser_id=user_id
            user_topic.Ftopic_id=topic_id
            user_topic.Fsns_type = sns_type             # 1.点赞  2.关注
            user_topic.Ftopic_type = topic_type           # 1.topic 2.topic_reply
            self.db.add(user_topic)
            if sns_type == 1:
                if topic_type == 1:
                    self.db.query(Topics).filter(Topics.Fid == topic_id).update({Topics.Fpraise:Topics.Fpraise+1})
                else:
                    self.db.query(TopicReply).filter(TopicReply.Fid == topic_id).update({TopicReply.Fpraise:TopicReply.Fpraise+1})
            self.db.commit()

        elif operation==0 and is_exist:

             #为评论是 增加评论次数
            topic_sns.update({UserTopicSns.Fdeleted:1})
            if sns_type == 1:
                if topic_type == 1:
                    self.db.query(Topics).filter(Topics.Fid == topic_id).update({Topics.Fpraise:Topics.Fpraise-1})
                else:
                    self.db.query(TopicReply).filter(TopicReply.Fid == topic_id).update({TopicReply.Fpraise:TopicReply.Fpraise-1})
            self.db.commit()
        else:
            return False
        return True

    def query_user_sns_topic(self, **kwargs):
        query = self.db.query(UserTopicSns).filter(UserTopicSns.Fdeleted==0)
        if kwargs.get('user_id'):
            query = query.filter(UserTopicSns.Fuser_id == kwargs['user_id'])
        return query


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

    def get_topic_banner_list(self):
        '''
        todo:获取banner图片
        :return:
        '''
        return self.db.query(TopicBanner).\
            filter(TopicBanner.Fdeleted == 0).order_by('Fcreate_time desc').limit(3).offset(0)

    def check_sns_exist(self,user_id,topic_id,sns_type):
        '''
        todo:判断用户是否点赞
        :param user_id:
        :param topic_id:
        :return:
        '''
        query = self.db.query(UserTopicSns).\
            filter(UserTopicSns.Fdeleted == 0,UserTopicSns.Fuser_id == user_id,
                   UserTopicSns.Ftopic_id == topic_id,UserTopicSns.Fsns_type == sns_type).scalar()
        if query:
            return True
        else:
            return False

    def get_top_active_user_topic(self):
        '''获取问答 每月和每周最活跃用户信息'''
        sql_top_week = u"select user_id, sum(c) as c from ((select count(Fid) as c, Fuser_id as user_id from t_topic_reply where Fcreate_time > '%s' group by Fuser_id order by c desc limit 10 ) union all (select count(Fid) as c, Fuser_id as user_id from t_topics where Fcreate_time > '%s' group by Fuser_id order by c desc limit 10)) as tmp group by user_id order by c  desc limit 10" % (time_of_seven_days_ago(),time_of_seven_days_ago())
        sql_top_month = u"select user_id, sum(c) as c from ((select count(Fid) as c, Fuser_id as user_id from t_topic_reply where Fcreate_time > '%s' group by Fuser_id order by c desc limit 10 ) union all (select count(Fid) as c, Fuser_id as user_id from t_topics where Fcreate_time > '%s' group by Fuser_id order by c desc limit 10)) as tmp group by user_id order by c  desc limit 10" % (time_of_a_month_ago(),time_of_a_month_ago())
        top_week = self.db.execute(sql_top_week)
        top_month = self.db.execute(sql_top_month)
        # top_week = self.db.query(TopicReply.Fuser_id,func.count('*').label("user_count")).filter(TopicReply.Fdeleted==0, TopicReply.Fcreate_time>time_of_seven_days_ago()).group_by(TopicReply.Fuser_id).order_by('user_count desc').limit(10).all()
        # top_month = self.db.query(TopicReply.Fuser_id,func.count('*').label("user_count")).filter(TopicReply.Fdeleted==0, TopicReply.Fcreate_time>time_of_a_month_ago()).group_by(TopicReply.Fuser_id).order_by('user_count desc').limit(10).all()
        return top_week, top_month


    def get_reply_of_reply(self,reply_id):
        '''
        :todo 获取回复的回复list
        :param reply_id:
        :return:
        '''
        replies = self.db.query(TopicReply).filter(TopicReply.Ffull_parent_id.like('%/'+str(reply_id)+'/%'))
        total_count = replies.count()
        reply_list = replies.order_by(' Fcreate_time asc')
        return total_count,reply_list

    def get_reply_by_reply_id(self,reply_id):
        '''
        :todo 获取回复的回复list
        :param reply_id:
        :return:
        '''
        return self.db.query(TopicReply).filter(TopicReply.Fid == reply_id, TopicReply.Fdeleted == 0).scalar()

    def query_topic_reply(self, **kwargs):
        query = self.db.query(TopicReply).filter(TopicReply.Fdeleted == 0)
        if kwargs.has_key('parent_id'):
            query = query.filter(TopicReply.Fparent_id==kwargs['parent_id'])
        if kwargs.has_key('topic_id'):
            query = query.filter(TopicReply.Ftopic_id==kwargs['topic_id'])
        return query

    def check_end_date_topics(self,c_top=None,c_essence=None):
        '''
        todo:检查过期的置顶或者加精话题
        :return:
        '''
        now = datetime.datetime.now()
        if c_top:
            query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_top ==1,Topics.Ftop_end_date < now)
            if query.count() > 0:
                query.update({'Fis_top':0,'Ftop_end_date':None})
                self.db.commit()
        if c_essence:
            query = self.db.query(Topics).filter(Topics.Fdeleted == 0,Topics.Fis_essence == 1,Topics.Fessence_expire_time < now)
            if query.count() > 0:
                query.update({'Fis_essence':0,'Fessence_expire_time':None})
                self.db.commit()

    def filter_img_tag(self, str=''):
        return re.sub(r'<img.*?>', '', str)
