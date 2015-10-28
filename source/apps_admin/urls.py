#encoding:utf-8
__author__ = 'binpo'

from apps_admin.users.urls import handlers as user_handlers
from apps_admin.recommend import _handlers as recommend_handlers
from apps_admin.home import AdminHandler
from apps_admin.orders.urls import handlers as order_handlers
from apps_admin.system.urls import handlers as system_handler
from apps_admin.companys.urls import handlers as company_handlers
from apps_admin.albums.urls import handlers as albums_handlers
from apps_admin.schedules.urls import handlers as schedule_handlers
from apps_admin.weixin.urls import handlers as weixin_handler
from apps_admin.work.urls import handlers as work_handler
from apps_admin.music.urls import handlers as music_handler
from apps_admin.series.urls import handlers as series_handler
from apps_admin.topic.urls import handlers as topic_handler
from apps_admin.message.urls import handlers as message_handler
from apps_admin.banner import _handlers as banner_handlers
from apps_admin.activities.urls import _handlers as activity_handler

handlers=[
    # (r'/', AdminHandler),
    (r'/admin/index', AdminHandler),
]
handlers.extend(company_handlers)

handlers.extend(series_handler)
handlers.extend(user_handlers)
handlers.extend(order_handlers)
handlers.extend(system_handler)
handlers.extend(albums_handlers)
handlers.extend(schedule_handlers)
handlers.extend(weixin_handler)
handlers.extend(work_handler)
handlers.extend(music_handler)
handlers.extend(topic_handler)
handlers.extend(recommend_handlers)
handlers.extend(message_handler)
handlers.extend(banner_handlers)
handlers.extend(activity_handler)