#encoding:utf-8
__author__ = 'binpo'

from apps_admin.users.roles_handler import *
from apps_admin.users.user_handler import *
from apps_admin.users.merchant_handler import *


handlers=[

    (r'/gzh/ops/users/resetpwd/(\d*)/', UserResetPasswd),
    (r'/gzh/ops/users/new', UserCreateHandler),
    (r'/gzh/ops/roles/([\w\W]*)', RolesHandler),
    (r'/gzh/ops/permissions/',MerchantPermissionHandler),
    (r'/gzh/ops/users/edit/([\w\W]*)/([\w\W]*)', UserEditHandler),
    (r'/gzh/ops/users/delete/([\w\W]*)', UserDeleteHandler),
    (r'/gzh/ops/users/list/([\w\W]*)', UserQueryHandler),
    (r'/gzh/ops/merchant/list/([\w\W]*)',UserQueryHandler),
    (r'/gzh/ops/users/authorize/([\w\W]*)',AuthorizeHandler),
    (r'/gzh/ops/change/province/([\w\W]*)',ProvinceChangeHandler),
    (r'/gzh/ops/change/city/([\w\W]*)',CityChangeHandler),
]
