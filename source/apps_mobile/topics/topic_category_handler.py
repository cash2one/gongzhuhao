#encoding:utf-8
__author__ = 'binpo'
from apps_mobile.mobile_base import MobileBaseHandler
from services.topics.topic_services import TopicServices
from conf.topic_conf import TOPIC_KEYS,TOPIC_CATEGORY_KES,BANNERS
import sys

topic_services = TopicServices()
_TOPIC_CATEGORY_DEFAULT_URL = "/static/crm/images/default.gif"

class CategoryHandler(MobileBaseHandler):

    def get(self):
        topic_services.set_db(self.db)
        try:
            query_categorys = topic_services.query_topic_category(order_by='Fsort')
            query_banners = topic_services.get_topic_banner_list(order_by = 'Fcreate_time desc')
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})
        if self.request.uri.startswith('/api/json/'):
            query_hot_topics = topic_services.get_hot_topics_list()
            hot_topics = [self.obj_to_dict(topic,TOPIC_KEYS) for topic in query_hot_topics]
            for hot_topic in hot_topics:
                images = self.get_topic_img(hot_topic.get('Fid'),'topic')
                hot_topic['images'] = images
                hot_topic['Fnick_name'] = self.get_user_info(hot_topic.get('Fuser_id')).get('nick_name')

            topic_banners = [self.obj_to_dict(banner,BANNERS) for banner in query_banners]

            topic_categorys = [self.obj_to_dict(topic_category,TOPIC_CATEGORY_KES) for topic_category in query_categorys]
            for topic_category in topic_categorys:
                topic_category['Fpage_view'] = self.get_page_view('t_topic_category',topic_category.get('Fid'),topic_category.get('Fpage_view'))

            data = {
                'hot_topics':hot_topics,
                'topic_categorys':topic_categorys,
                'topic_banners':topic_banners
            }
            self.write_json({'stat':'ok','data':data,'info':''})
        else:
            self.echo('views/topic/topic.html',
                      {
                       'topic_categorys':query_categorys,
                       'banners':query_banners,
                      })
