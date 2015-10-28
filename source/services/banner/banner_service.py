#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.banner_do import *

class BannerService(BaseService):

    def create_banner_type(self,**kwargs):
        '''
        todo:添加banner类型
        :param kwargs:
        :return:
        '''
        banner_type = BannerType()

        banner_type.Fbanner_name = kwargs.get('banner_name')
        banner_type.Fbanner_code = kwargs.get('banner_code')
        banner_type.Fbanner_desc = kwargs.get('banner_desc')
        self.db.add(banner_type)
        self.db.commit()

    def get_banner_type_by_code(self,banner_code):
        '''
        todo:根据banner_code获取banner_type
        :param banner_code:
        :return:
        '''
        return self.db.query(BannerType).filter(BannerType.Fdeleted == 0,BannerType.Fbanner_code == banner_code).scalar()

    def get_banner_type_list(self):
        '''
        todo:获取所有banner类型
        :return:
        '''
        return self.db.query(BannerType).filter(BannerType.Fdeleted == 0)


    def create_banner(self,**kwargs):
        '''
        todo:创建banner图片
        :param kwargs:
        :return:
        '''
        query = self.db.query(Banner).filter(Banner.Fdeleted == 0,Banner.Fbanner_code == kwargs.get('banner_code'))
        if query.count() >0:
            query.update({'Fdeleted':1})
            self.db.commit()
        banner = Banner()

        banner.Fname = kwargs.get('banner_name')
        banner.Fbanner_code = kwargs.get('banner_code')
        banner.Fimage_url = kwargs.get('img_url')
        banner.Fdescription = kwargs.get('banner_desc')
        banner.Flink = kwargs.get('link_url')
        banner.Fstart_time = kwargs.get('start_time')
        banner.Fexpire_time = kwargs.get('expire_time')
        self.db.add(banner)
        self.db.commit()
        return banner

    def query_banner(self,**kwargs):
        '''
        todo:查询banner
        :param kwargs:
        :return:
        '''
        query = self.db.query(Banner).filter(Banner.Fdeleted == 0)
        if kwargs.get('banner_code',''):
            query = query.filter(Banner.Fbanner_code == kwargs.get('banner_code'))

        return query














