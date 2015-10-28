#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'

from topic_handler import *
handlers = [
    (r'/topic', TopicIndexHandler), #话题首页
    (r'/topic/(\d+)/(\d*)', TopicIndexHandler), #话题某个分类首页
    (r'/topic/category/(\d*)/(\d*)', TopicQueryHandler), #话题分类list页面
    (r'/topic/detail/(\d+)/(\d+)', TopicDetailHandler), #话题详细页
    (r'/topic/create/(\d*)', TopicCreateHandler), #创建话题
    (r'/topic/edit/(\d*)', TopicEditHandler), #编辑话题
    (r'/topic/reply/create/(\d+)/(\d+)', TopicReplyCreateHandler), #创建回复
    (r'/topic/reply/(\d+)/(\d*)', TopicReplyQueryHandler), #查询某个话题的回复
    # (r'/topic/delete/(\d*)',TopicDeleteHandler), #话题删除
    (r'/topic/sns/([\d]*)/([\d]*)/([\d]*)/([\d]*)',TopicSnsHandler), #话题点赞

    (r'/topic/reply/more/(\d*)', TopicReplyMoreHandler), #查询某个话题的回复
]