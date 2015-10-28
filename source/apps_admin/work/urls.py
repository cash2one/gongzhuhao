__author__ = 'frank'

from apps_admin.work.works_handler import *

handlers = [
    (r'/gzh/ops/works/list/([\d]*)',WorksListHandler),
    (r'/gzh/ops/work/delete/([\d]*)',DeleteWorkHandler),
]
