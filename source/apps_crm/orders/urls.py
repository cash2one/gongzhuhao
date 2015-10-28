
from orders_handler import *
from bespeak_order_handler import BespeakOrdersHandler
handlers = [
    (r'/merchant/orders/', CHandlerOrdersList),
    (r'/merchant/orders/add/', CHandlerOrdersAdd),
    (r'/merchant/orders/update/([\d]{1,28})/', CHandlerOrdersUpdate),
    (r'/merchant/orders/confirm/([\d]{1,28})', OrderConfirmHandler),
    (r'/merchant/orders/list/([\d]{1,28})',OrderQueryHandler),
    (r'/merchant/orders/delete/([\d]{1,28})',OrderDeleteHandler),
    (r'/merchant/orders/backup/',OrdersBackupHandler),
    (r'/merchant/orders/backup/download/([\d]{1,28})',OrderBackDownload),

    (r'/merchant/bespeak_order',BespeakOrdersHandler),

]

