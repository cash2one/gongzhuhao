__author__ = 'morichounami'
from apps_crm.users.user_handler import *

handlers = [
    (r'/admin/users/welcome',UserHandler),
]