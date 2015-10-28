#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.home_do import *
from models.banner_do import *


class HomeService(BaseService):

    def query_recommend(self,**kwargs):
        '''
        todo:查询展示信息
        :param kwargs:
        :return:
        '''
        query = self.db.query(HomeRecommend).filter(HomeRecommend.Fdeleted == 0)
        if kwargs.get('code',''):
            query = query.filter(HomeRecommend.Frecommend_type == kwargs.get('code'))
        if kwargs.get('Fproduct_id',''):
            query = query.filter(HomeRecommend.Fproduct_id == kwargs.get('Fproduct_id'))
        if kwargs.get('Frecommend_type',''):
            query = query.filter(HomeRecommend.Frecommend_type == kwargs.get('Frecommend_type'))
        if kwargs.get('Fposition',''):
            query = query.filter(HomeRecommend.Fposition == kwargs.get('Fposition'))
        if kwargs.get('Fis_on_share'):
            query = query.filter(HomeRecommend.Fis_on_share == kwargs.get('Fis_on_share'))
        return query

    def create_recommend(self,**kwargs):
        '''
        todo：创建首页展示信息
        :param kwargs:
        :return:
        '''
        home_recommend = HomeRecommend()
        home_recommend.Fuser_id = kwargs.get('user_id','')
        home_recommend.Fproduct_id = kwargs.get('product_id','')
        home_recommend.Fproduct_name = kwargs.get('product_name','')
        home_recommend.Frecommend_type = kwargs.get('type','')
        home_recommend.Fmerchant_id = kwargs.get('merchant_id','')
        self.db.add(home_recommend)
        self.db.commit()

    def update_recommend(self,re_id,**kwargs):
        '''
        todo:修改展示信息
        :param product_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(HomeRecommend).filter(HomeRecommend.Fdeleted == 0,HomeRecommend.Fid == re_id)
        query.update(kwargs) #位置，上架标志更新
        self.db.commit()

    def delete_recommend(self,re_id):
        '''
        todo:删除首页推荐
        :param re_id:
        :return:
        '''
        query = self.db.query(HomeRecommend).filter(HomeRecommend.Fdeleted == 0,HomeRecommend.Fid == re_id)
        if query.count() >= 1:
            for re in query:
                self.db.delete(re)
                self.db.commit()





