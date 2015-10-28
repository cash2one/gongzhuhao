#!/usr/bin/env python
# encoding: utf-8

__author__ = 'binpo'

from apps_mobile.mobile_login import MobileLoginHandler, LoginOutHandler,APPLoginHandler
from apps_mobile.mobile_base import MobileHandler
from apps_mobile.topics.urls import handler as topic_handler
from mobile_reg import SendRegistCodeHandler,RegisterHandler,APPRegHandler,MobileCodeHandler
from apps_mobile.home import AppIndexHandler


handlers = [

    (r'/mobile/user/login', MobileLoginHandler),
    (r'/mobile/user/loginout', LoginOutHandler),
    (r'/api/json/user/loginout',LoginOutHandler),
    (r'/api/json/user/login',APPLoginHandler),
    (r'/api/json/user/register/',APPRegHandler),
    (r'/mobile/phone/send_phone_code/', SendRegistCodeHandler),
    (r'/mobile/phone/reg/',RegisterHandler),
    (r'/api/json/index/',AppIndexHandler),
    (r'/api/json/mobile/code',MobileCodeHandler),

]


handlers.extend(topic_handler)

from apps_mobile.users.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.orders.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.schedule.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.work.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.series.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.merchants.urls import _handlers as merchant_handers
handlers.extend(merchant_handers)

from apps_mobile.share.urls import _handlers
handlers.extend(_handlers)

from apps_mobile.favorites.urls import _handlers
handlers.extend(_handlers)

# from apps_mobile.demo import _handlers
# handlers.extend(_handlers)


handlers.append((r'/([\w\W]*)', MobileHandler))
