
from home import HomeHandler, HealthCheck,MerchantIndexHandler

handlers = list()

# handlers.append((r'/', HomeHandler))
# handlers.append((r'/ok.html', HealthCheck))

handlers.append((r'/merchant/index/', MerchantIndexHandler))

from apps_crm.orders import urls as orders
handlers.extend(orders.handlers)

from apps_crm.login import urls as login
handlers.extend(login.handlers)

from apps_crm.departments import urls as departments
handlers.extend(departments.handlers)

from apps_crm.schedule import urls as schedule
handlers.extend(schedule.handlers)

from apps_crm.albums import urls as albums
handlers.extend(albums.handlers)

from apps_crm.departments import urls as departments
handlers.extend(departments.handlers)

from apps_crm.staffers import urls as staffers
handlers.extend(staffers.handlers)

from apps_crm.binary_img import url as binary_url
handlers.extend(binary_url.handlers)

from apps_crm.merchants import urls as merchants
handlers.extend(merchants.handlers)

from apps_crm.work import urls as work_url
handlers.extend(work_url.handlers)

from apps_crm.series import urls as series_url
handlers.extend(series_url.handlers)

from apps_crm.weixin import urls as weixin_url
handlers.extend(weixin_url.handlers)

from weddingdress import urls as weddingdress_url
handlers.extend(weddingdress_url.handlers)

from weddingcompany import urls as weddingcompany_url
handlers.extend(weddingcompany_url.handlers)

# from apps_crm.demo.handler import ZtreeHandler
# handlers.append((r'/ztree', ZtreeHandler))
from home import TestIEJson
handlers.append((r'/iejson/', TestIEJson))


handlers.append((r'/', MerchantIndexHandler))

