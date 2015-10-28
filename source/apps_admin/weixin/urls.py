#encoding:utf-8
from apps_admin.weixin.weixin_handler import *

__author__ = 'sunlifeng'

handlers=[
        (r'/admin/weixin/', WeixinListHandler), #配置一览默认
        (r'/admin/weixin/detail/([\d\D]*)/', WeixinDetailHandler),  #配置详细
        (r'/admin/weixin/delete/([\d\D]*)', WeixinDeleteHandler),  #配置删除

        (r'/admin/weixin/menu/bind/([\d\D]*)/([\w\W]*)', WeixinMenuBindHandler),  #绑定菜单
        (r'/admin/weixin/menu/unbind/([\d\D]*)/([\w\W]*)', WeixinMenuUnBindHandler),  #解除绑定菜单
        (r'/admin/weixin/menu/([\d\D]*)', WeixinMenuHandler),  #配置菜单

        (r'/admin/weixin/check/', WeixinCheckHandler), #AppID&Secret验证

        (r'/admin/weixin/([\w\W]*)/', WeixinListHandler), #配置一览搜索
]