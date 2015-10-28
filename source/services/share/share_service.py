#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.share_do import *

class ShareService(BaseService):

    def get_share_list(self,**kwargs):
        '''
        todo:获取分享列表
        :return:
        '''
        query = self.db.query(UserPhotosShare).filter(UserPhotosShare.Fdeleted == 0).order_by('Fcreate_time desc')
        if kwargs.get('share_id'):
            query = query.filter(UserPhotosShare.Fid == kwargs.get('share_id'))
        return query

    def get_share_images(self,share_id):
        '''
        todo:获取分享相片
        :param share_id:
        :return:
        '''
        query = self.db.query(ShareImages).\
            filter(ShareImages.Fdeleted == 0,ShareImages.Fuser_photos_share_id == share_id)
        return query

