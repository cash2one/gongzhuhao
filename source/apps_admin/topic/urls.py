#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_admin.topic.topic_handler import TagsCreateHandler,TagsListHandler,TopicCategoryCreateHandler,\
    EditTopicCategoryHandler,TopicCategoryListHandler,TopicListHandler,TopicOperationHandler,TopicBannerHandler,\
    BannerQueryHandler,TopicDeleteHandler

handlers = [
    (r'/gzh/ops/create/topic/tag/',TagsCreateHandler),
    (r'/gzh/ops/create/banner/',TopicBannerHandler),
    (r'/gzh/ops/topic/banner/list',BannerQueryHandler),
    (r'/gzh/ops/query/topic/tags/',TagsListHandler),
    (r'/gzh/ops/create/topic/category/([\d]*)',TopicCategoryCreateHandler),
    (r'/gzh/ops/edit/topic/category/([\d]*)',EditTopicCategoryHandler),
    (r'/gzh/ops/query/topic/categorys/([\d]*)',TopicCategoryListHandler),

    (r'/gzh/ops/topic/delete/([\d]*)',TopicDeleteHandler),
    (r'/gzh/ops/topic/list',TopicListHandler),
    (r'/gzh/ops/topic/operation',TopicOperationHandler),
]