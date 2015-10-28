#encoding:utf-8
__author__ = 'binpo'

from apps_mobile.topics.topic_category_handler import CategoryHandler
from apps_mobile.topics.topic_handler import TopicCreateHandler,TopicQueryHandler,\
    TopicDetailHandler,TopicPhotosUploadHandler,TopicReplyCreateHandler
from tornado.web import url

handler=[

    (r'/mobile/topics/index/',CategoryHandler),
    (r'/mobile/topics/photo/upload/',TopicPhotosUploadHandler),
    (r'/mobile/topics/create/([\d]*)/([\d]*)', TopicCreateHandler),
    (r'/mobile/reply/create/([\d]*)/([\d]*)/([\d]*)',TopicReplyCreateHandler),
    (r'/mobile/topics/query/([\d]*)/([\d]*)/([\d]*)',TopicQueryHandler),
    (r'/mobile/topic/detail/([\d]*)/([\d]*)/([\d]*)/([\d]*)',TopicDetailHandler),

]

apps_handlers = [
    url(r'/api/json/topics/index/',CategoryHandler,name='topics_index'),
    url(r'/api/json/topics/query/([\d]*)/([\d]*)/([\d]*)',TopicQueryHandler,name='topics_list'),
    url(r'/api/json/topic/detail/([\d]*)/([\d]*)/([\d]*)/([\d]*)',TopicDetailHandler,name='topic_detail'),
]

handler.extend(apps_handlers)
