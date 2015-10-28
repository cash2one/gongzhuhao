#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from services.series.series_services import SeriesServices
from services.home.home_service import HomeService
from services.company.company_services import CompanyServices
from services.work.work_services import WorkServices
from services.topics.topic_services import TopicServices
import time
import sys

series_service = SeriesServices()
company_service = CompanyServices()
work_service = WorkServices()
topic_service = TopicServices()
home_service = HomeService()

class UserIndexHandler(BaseApiHandler):

    #@login_control()
    def get(self, *args, **kwargs):
        self.echo('views/account/index.html')


class TopicIndexHandler(BaseApiHandler):

    def get(self, *args, **kwargs):
        self.redirect('/topic')
class ViewsIndexHandler(BaseApiHandler):

    def get(self,view_path, **kwargs):
        views = view_path.split('views')
        url = 'views/'+views[-1]

        self.echo(url)

class HomeHandler(BaseApiHandler,WebCacheHandler):

    def get(self, *args, **kwargs):
        '''
        todo:首页
        :param args:
        :param kwargs:
        :return:
        '''
        home_service.set_db(self.db)
        try:
            series_essence,series_upper_left,series_upper_center,series_upper_right,series_down_first,\
            series_down_second,series_down_third,series_down_fourth = self.get_recommend_series()

            hot,product_upper_left,product_upper_center,product_upper_right,product_down_left,\
            product_down_center,product_down_right= self.get_recommend_products()

            lst_merchant = self.get_recommend_merchants()

            w_banner_first = self.get_banner('w_banner_first')
            w_banner_second = self.get_banner('w_banner_second')
            w_banner_third = self.get_banner('w_banner_third')
            w_activity_banner = self.get_banner('web_activity')
            self.keywords = '公主号，结婚日记，婚礼策划，婚庆公司，婚纱摄影，婚礼创意，旅游婚纱，结婚论坛，结婚社区'
            self.description = '数万新人真实备婚日记，让过来人告诉你怎样的商家“才靠谱”，学习别人的经验，你的婚礼将更完美！'
            self.title='公主号，结婚真实案例分享平台，特价秒杀天天有'
            self.echo('view/home/index.html',
                  {
                   's_essence':series_essence,
                   's_upper_left':series_upper_left,
                   's_upper_center':series_upper_center,
                   's_upper_right':series_upper_right,
                   's_down_first':series_down_first,
                   's_down_second':series_down_second,
                   's_down_third':series_down_third,
                   's_down_fourth':series_down_fourth,
                   'p_hot':hot,
                   'p_upper_left':product_upper_left,
                   'p_upper_center':product_upper_center,
                   'p_upper_right':product_upper_right,
                   'p_down_left':product_down_left,
                   'p_down_center':product_down_center,
                   'p_down_right':product_down_right,
                   'merchants':lst_merchant,
                   'w_banner_first':w_banner_first,
                   'w_banner_second':w_banner_second,
                   'w_banner_third':w_banner_third,
                   'w_activity_banner':w_activity_banner
                  })
        except Exception,e:
            pass



class Activities(BaseApiHandler):
    def get(self,tmp, **kwargs):
        url = 'view/activities'+tmp
        self.echo(url)




