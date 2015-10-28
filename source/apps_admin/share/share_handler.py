#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from services.share.share_service import ShareService
import sys

share_service = ShareService()

class ShareHandlerList(AdminBaseHandler):

    def get(self,page):
        '''
        todo:获取分享列表
        :return:
        '''
        share_service.set_db(self.db)
        try:
            query = share_service.get_share_list()
            shares = self.get_page_data(query)
            self.echo('views/share/share_list.html',{'shares':shares},layout='views/share/index.html')
        except Exception,e:

            return self.echo('views/500.html')