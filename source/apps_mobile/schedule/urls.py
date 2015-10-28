#!/usr/bin/env python
# encoding: utf-8

from schedule_handler import CHandlerScheduleH5List, CHandlerScheduleH5Tips,\
    CWxHandlerOrderList,OrderEvaluationHandler,EvaluationUploadHandler,DeleteImagesHandler

_handlers = [
    (r'/mobile/schedule/list/([\d]{1,9})/', CHandlerScheduleH5List),

    (r'/weixin/user/orders/', CWxHandlerOrderList),  # 订单列表信息

    (r'/mobile/schedule/detail/([\d]{1,9})/([\d]{1,9})/',CHandlerScheduleH5Tips),

    (r'/mobile/create/evaluation/category/([\w\W]*)/([\w\W]*)/',OrderEvaluationHandler),

    (r'/mobile/create/evaluation/image/([\d]*)',EvaluationUploadHandler),
    (r'/mobile/delete/evaluation/image/([\d]*)',DeleteImagesHandler),
]
