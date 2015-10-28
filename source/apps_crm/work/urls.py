
from work_handler import *

handlers = [
    (r'/merchant/work/', WorkList),
    (r'/merchant/work/list/([\w\W]*)', WorkList),
    (r'/merchant/work/add/', WorkAdd),
    (r'/merchant/work/add/(\d*)/', WorkAdd),
    (r'/merchant/work/edit/(\d*)/', WorkAdd),
    (r'/merchant/work/delete/(\d*)/', WorkDelete),
    (r'/merchant/work/delete/img/(\d*)', WorkImageDelete),

]