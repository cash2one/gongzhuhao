
from schedule_handler import *
from schedule_h5_handler import *

handlers = [
    (r'/user/schedule/([\d]{1,28})/', CHandlerScheduleH5List),
    (r'/user/schedule/([\d]{1,28})/([0-4])/', CHandlerScheduleH5Tips),

    (r'/merchant/schedule/edit/template/site/', CHandlerTemplateSiteUpdate),
    (r'/merchant/schedule/delete/template/site/', CHandlerTemplateSiteDelete),
    (r'/merchant/schedule/setdefault/template/site/', CHandlerTemplateSiteSetDefualt),

    (r'/merchant/schedule/edit/template/msg/', CHandlerTemplateAttention),

    (r'/merchant/schedule/([\d]{1,28})/', CHandlerScheduleList),
    (r'/merchant/schedule/update/([\d]{1,28})/', CHandlerScheduleUpdate),

    (r'/merchant/schedule/plan/', ScheduleOperationHandler),
    (r'/merchant/set/schedule/plan/', SchedulePlanHandler),
    (r'/merchant/update/schedule/plan/', UpdateSchedulePlanHandler),
    (r'/merchant/get/schedule/by_month/', ScheduleQueryHandler),

    (r'/merchant/schedule/query/detail/', ScheduleSearchHandler),

    (r'/merchant/schedule/category/add/',ScheduleCategoryAddHandler),
    (r'/merchant/schedule/category/list/',ScheduleCategoryListHandler),
    (r'/merchant/schedule/category/edit/([\w\W]*)',ScheduleCategoryEditHandler),
    (r'/merchant/schedule/category/delete/([\w\W]*)',DeleteScheduleCategoryHandler),
    (r'/merchant/order/schedule/update/',OrdersScheduleUpdateHandler),
    (r'/merchant/share/wishes/',MerchantWishesHandler),
    (r'/merchant/delete/share/wishes/([\w\W]*)',DeleteMerchantWishesHandler),

    #(r'/merchant/schedule/export/([\w\W]*)/([\w\W]*)/([\w\W]*)',ScheduleExport),
    (r'/merchant/schedule/export_by_schedule_type/([\w\W]*)/([\w\W]*)',ScheduleExportByType),
    # (r'/merchant/schedule/plan/check/',SchedulePlanCheckHandler),
]

