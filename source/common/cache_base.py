#encoding:utf-8
__author__ = 'wangjinkuan'

from conf.work_conf import SERIES_KEYS,WORK_KEYS
from conf.merchant import COMPANY_KEYS
from conf.share_conf import SHARE_KEYS
from services.work.work_services import WorkServices
from services.series.series_services import SeriesServices
from services.favorites.favorites_services import FavoritesService
from services.company.company_services import CompanyServices
from services.topics.topic_services import TopicServices
from services.share.share_service import ShareService
from services.home.home_service import HomeService
from services.banner.banner_service import BannerService
from services.company.location_service import LocationServices
from services.schedules.schedules_service import ScheduleService
from conf.home_conf import packages_position,products_position,companys_position
from conf.order_conf import EVALUATION_KEYS
from datacache.datacache import UserMsgCache
from tenjin_base import TenjinBase
import datetime

work_service = WorkServices()
series_service = SeriesServices()
favorite_service = FavoritesService()
company_service = CompanyServices()
share_service = ShareService()
home_servie = HomeService()
banner_service = BannerService()
topic_services = TopicServices()
schedule_service = ScheduleService()

class CacheBaseHandler(TenjinBase):

    @property
    def db(self):
        return self.application.db

    @property
    def mcache(self):
        return self.application.mcache

    @property
    def rcache(self):
        return self.application.rcache

    def obj_to_dict(self,obj,keys,format='%Y-%m-%d %H:%M:%S'):
        data={}
        for key in keys:
            if obj.__dict__.get(key,None):
                data[key] = obj.__dict__.get(key,None)
                if isinstance(data[key],datetime.datetime):
                    data[key]=datetime.datetime.strftime(data[key],format)
            elif obj.__dict__.get(key) == 0:
                data[key] = 0
            else:
                data[key] = ''
        return data

    def get_banner(self,banner_code):
        '''
        todo:获取banner
        :param banner_code:
        :return:
        '''
        m_key = str(banner_code)+'_banner'
        data = self.mcache.get(m_key)
        if not data:
            banner_service.set_db(self.db)
            banner = banner_service.query_banner(banner_code = banner_code).scalar()
            if not banner:
                data = {}
            else:
                data = self.obj_to_dict(banner,['Fid','Fname','Fimage_url','Fdescription','Fvalue_type','Flink'])
            self.mcache.set(m_key,data,86400*7)
        return data

class AppCacheHandler(CacheBaseHandler):

    def get_favorites_info(self,user_id,favorite_type):
        '''
        todo:获取用户收藏信息
        :param user_id:用户ID
        :param favorite_type:收藏类型
        :return:
        '''
        m_key = str(user_id)+'favorite'+str(favorite_type)
        lst_data = self.mcache.get(m_key)
        if not lst_data:
            favorite_service.set_db(self.db)
            favorites = favorite_service.query_favorite(user_id = user_id,favorite_type = favorite_type)
            lst_data = []
            if favorite_type == '1':
                for f in favorites:
                    company_service.set_db(self.db)
                    company = company_service.get_company_by_uid(f.Ffavorites_id)
                    company_dict = self.obj_to_dict(company,COMPANY_KEYS)
                    lst_data.append(company_dict)
            elif favorite_type == '2':
                for f in favorites:
                    series_service.set_db(self.db)
                    series = series_service.query_series(id = f.Ffavorites_id).scalar()
                    series_dict = self.obj_to_dict(series,SERIES_KEYS)
                    lst_data.append(series_dict)
            else:
                for f in favorites:
                    work_service.set_db(self.db)
                    work = work_service.query_work(id = f.Ffavorites_id).scalar()
                    work_dict = self.obj_to_dict(work,WORK_KEYS)
                    lst_data.append(work_dict)
            self.mcache.set(m_key,lst_data,86400)
        return lst_data

    def delete_user_favorite(self,user_id,favorite_type):
        '''
        todo:删除用户收藏
        :param user_id:
        :param favorite_type:
        :return:
        '''
        m_key = str(user_id)+'favorite'+str(favorite_type)
        lst_data = self.mcache.get(m_key)
        if lst_data:
            self.mcache.delete(m_key)

    def get_user_share_info(self):
        '''
        todo:获取真人秀
        :return:
        '''
        m_key = 'shares_list'
        lst_data = self.mcache.get(m_key)
        if not lst_data:
            lst_data = []
            share_service.set_db(self.db)
            query_shares = share_service.get_share_list()

            for share in query_shares.limit(5).offset(0):
                share_dict = self.obj_to_dict(share,SHARE_KEYS)
                lst_data.append(share_dict)
                self.mcache.set(m_key,lst_data,86400)
        return lst_data

class WebCacheHandler(CacheBaseHandler):

    def get_recommend_series(self):
        '''
        todo:获取首页推荐套系
        :return:
        '''
        my_key = 'recommend_series'
        lst_series = self.mcache.get(my_key)
        if not lst_series:
            home_servie.set_db(self.db)
            lst_series = []
            for position in packages_position:
                data = {'Fposition':position,'Frecommend_type':1,'Fis_on_share':1}
                query = home_servie.query_recommend(**data)
                re = query.scalar()
                lst_series.append(re)
            self.mcache.set(my_key,lst_series)
        return lst_series

    def get_recommend_products(self):
        '''
        todo:获取首页推荐产品
        :return:
        '''
        my_key = 'recommend_products'
        lst_products = self.mcache.get(my_key)
        if not lst_products:
            home_servie.set_db(self.db)
            lst_products = []
            for position in products_position:
                data = {'Fposition':position,'Frecommend_type':2,'Fis_on_share':1}
                query = home_servie.query_recommend(**data)
                re = query.scalar()
                lst_products.append(re)
            self.mcache.set(my_key,lst_products)
        return lst_products

    def get_recommend_merchants(self):
        '''
        todo:获取首页推荐商户
        :return:
        '''
        my_key = 'recommend_merchants'
        lst_merchants = self.mcache.get(my_key)
        if not lst_merchants:
            home_servie.set_db(self.db)
            lst_merchants = []
            for position in companys_position:
                data = {'Fposition':position,'Frecommend_type':3,'Fis_on_share':1}
                query = home_servie.query_recommend(**data)
                re = query.scalar()
                lst_merchants.append(re)
            self.mcache.set(my_key,lst_merchants)
        return lst_merchants

    def get_essence(self,page_size, series_service=None):
        '''
        todo:获取精品推荐
        :return:
        '''
        lst_series = self.mcache.get('new_essence_series')
        if not lst_series:
            if series_service is None:
                series_service = SeriesServices()

            series_service.set_db(self.db)
            query = series_service.get_essence_series()
            lst_series = []
            for s in query:
                lst_series.append({'cover_img':s.Fcover_img,'package_name':s.Fpackage_name,'price':s.Fsale_price})
            self.mcache.set('new_essence_series',lst_series)
        return lst_series

    def get_company_info(self,merchant_id):
        '''
        todo:获取公司信息
        :param merchant_id:
        :return:
        '''
        my_key = 'merchant_'+str(merchant_id)
        company_dict = self.mcache.get(my_key)
        if not company_dict:
            company_service.set_db(self.db)
            company = company_service.get_company_by_uid(merchant_id)
            company_dict = self.obj_to_dict(company,COMPANY_KEYS)
            self.mcache.set(my_key,company_dict,86400)
        return company_dict

    def get_area_name(self,area_id):
        '''
        todo:获取area
        :param area_id:
        :return:
        '''
        my_key = 'area_'+str(area_id)
        area_name = self.mcache.get(my_key)
        if not area_name:
            location_service = LocationServices(self.db)
            area_name = location_service.get_location_name_by_id('area',area_id)
            self.mcache.set(my_key,area_name)
        return area_name

    def get_package_count(self,merchant_id, series_service=None):
        '''
        todo:获取商户套系数量
        :param merchant_id:
        :return:
        '''
        my_key = 'package_count_'+str(merchant_id)
        count = self.mcache.get(my_key)
        if not count:
            if series_service is None:
                series_service = SeriesServices()

            series_service.set_db(self.db)
            query = series_service.query_series(merchant_id=merchant_id)
            count = query.count()
            self.mcache.set(my_key,count)
        return count

    def get_product_count(self,merchant_id, work_service=None):
        '''
        todo:获取商户作品数量
        :param type:
        :param id:
        :return:
        '''
        my_key = 'product_count_'+str(merchant_id)
        count = self.mcache.get(my_key)
        if not count:
            if work_service is None:
                work_service = WorkServices()
            work_service.set_db(self.db)
            query = work_service.query_work(merchant_id=merchant_id)
            count = query.count()
            self.mcache.set(my_key,count)
        return count

    def get_sns_topics_info(self,user_id,sns_type):
        '''
        todo:获取用户关注话题信息
        :param user_id:
        :return:
        '''
        if sns_type == 2:
            cache_key = str(user_id)+'attention'
        elif sns_type == 1:
            cache_key = str(user_id)+'praise'
        lstdata = self.mcache.get(cache_key)
        if not lstdata:
            lstdata = []
            topic_services.set_db(self.db)
            for sns in topic_services.get_sns_topics_list(user_id,sns_type):
                lstdata.append(sns.Ftopic_id)
            self.mcache.set(cache_key,lstdata)
        return lstdata

    def get_topics_info(self,topic_id,topic_type):
        '''
        todo:查询话题或者回复
        :param id:
        :param topic_type:
        :return:
        '''
        if topic_type == 'topic_':
            cache_key = 'topic_'+str(topic_id)
        elif topic_type == 'reply_':
            cache_key = 'reply_'+str(topic_id)
        data = self.mcache.get(cache_key)
        if not data:
            topic_services.set_db(self.db)
            topic = topic_services.get_topic_by_id(topic_id,topic_type)
            data = self.obj_to_dict(topic,
                                    ['Fid','Fuser_id','Ftopic_id','Fparent_id','Ffull_parent_id',
                                     'Fparent_user_id','Freply_index','Ftitle','Fcontent','Fis_top',
                                     'Fis_essence','Fis_prime','Fis_hot','Ftags','Fis_lock','Fpage_view',
                                     'Ftotal_assess','Fpraise','Fcreate_time','Fmodify_time'
                                    ])
            self.mcache.set(cache_key,data,86400)
        return data

    def get_topic_img(self,topic_id,type):
        '''
        todo:获取话题相片
        :param topic_id:主话题或者回复话题
        :return:
        '''
        if type == 'topic':
            my_key = 'topic_images_'+str(topic_id)
        elif type == 'reply':
            my_key = 'reply_images_'+str(topic_id)
        data = self.mcache.get(my_key)
        if not data:
            topic_services.set_db(self.db)
            data = []
            for image in topic_services.get_topic_images_list(topic_id,type):
                data.append({'img':self.img_compression(image.Fimg_url,image.Fimg_size),'original_img':image.Fimg_url})
            self.mcache.set(my_key,data)
        return data

    def delete_user_info(self,key):
        '''
        todo:删除缓存信息
        :param key:
        :return:
        '''
        data = self.mcache.get(key)
        if data:
            self.mcache.delete(key)
        UserMsgCache(self.db).refresh_user_msg(key)

class AdminCacheHandler(CacheBaseHandler):

    def delete_banner(self,banner_code):
        '''
        todo:删除banner缓存
        :param banner_code:
        :return:
        '''
        m_key = str(banner_code)+'_banner'
        data = self.mcache.get(m_key)
        if data:
            self.mcache.delete(m_key)

    def delete_recommend_series(self):
        '''
        todo:删除首页套系
        :return:
        '''
        my_key = 'recommend_series'
        lst_series = self.mcache.get(my_key)
        if lst_series:
            self.mcache.delete(my_key)

    def delete_recommend_products(self):
        '''
        todo:删除作品
        :return:
        '''
        my_key = 'recommend_products'
        lst_product = self.mcache.get(my_key)
        if lst_product:
            self.mcache.delete(my_key)

    def delete_recommend_merchant(self):
        '''
        todo:删除首页商家
        :return:
        '''
        my_key = 'recommend_merchants'
        lst_merchant = self.mcache.get(my_key)
        if lst_merchant:
            self.mcache.delete(my_key)

class MobileCacheHandler(CacheBaseHandler):

    def get_company_info(self,key):
        '''
        todo:获取公司信息
        :param key:
        :return:
        '''
        m_key = 'merchant_'+str(key)
        company_dict = self.mcache.get(m_key)
        if not company_dict:
            company_service.set_db(self.db)
            company = company_service.get_company_by_uid(key)
            company_dict = self.obj_to_dict(company,COMPANY_KEYS)
            self.mcache.set(m_key,company_dict,86400)
        return company_dict

    def get_evaluation(self,order_id,evaluation_code):
        '''
        todo:获取真人秀信息
        :param order_id:
        :param evaluation_code:
        :return:
        '''
        schedule_service.set_db(self.db)
        cache_key = str(order_id)+'_evaluation_info_'+str(evaluation_code)
        evaluation_dict = self.mcache.get(cache_key)
        if not evaluation_dict:
            evaluation = schedule_service.query_order_evaluations(order_id = order_id,schedule_type_code = evaluation_code).scalar()
            if evaluation:
                evaluation_dict = self.obj_to_dict(evaluation,EVALUATION_KEYS)
                images = []
                for img in schedule_service.get_evaluation_images(evaluation.Fid):
                    images.append(img.Fimg_url)
                evaluation_dict['images'] = images
                evaluation_dict['type_code'] = evaluation_code+1


                if evaluation_code == 0:
                    evaluation_dict['Fstaffer_name'] = [{'title':'礼服师','name':evaluation_dict['Fstaffer_name']}]
                    evaluation_dict['Fscore'] = [{'tag':'试衣','score':evaluation_dict.get('Fscore')}]

                elif evaluation_code == 1:
                    names = evaluation_dict.get('Fstaffer_name')
                    scores = evaluation_dict.get('Fscore').split('&')
                    evaluation_dict['Fstaffer_name'] = [{'title':'摄影师','name':names[0]},{'title':'化妆师','name':names[1]}]
                    evaluation_dict['Fscore'] = [{'tag':'摄影','score':scores[0]},{'tag':'化妆','score':scores[1]}]

                elif evaluation_code == 2:
                    evaluation_dict['Fstaffer_name'] = [{'title':'选样师','name':evaluation_dict['Fstaffer_name']}]
                    evaluation_dict['Fscore'] = [{'tag':'选样','score':evaluation_dict.get('Fscore')}]

                elif evaluation_code == 3:
                    evaluation_dict['Fstaffer_name'] = [{'title':'看样师','name':evaluation_dict['Fstaffer_name']}]
                    evaluation_dict['Fscore'] = [{'tag':'定稿','score':evaluation_dict.get('Fscore')}]

                else:
                    evaluation_dict['Fstaffer_name'] = [{'title':'客服代表','name':evaluation_dict['Fstaffer_name']}]
                    evaluation_dict['Fscore'] = [{'tag':'取件','score':evaluation_dict.get('Fscore')}]

                self.mcache.set(cache_key,evaluation_dict,86400)
            else:
                return {}
        return evaluation_dict

    def get_share_images(self,share_id):
        '''
        todo:获取分享图片
        :param share_id:
        :return:
        '''
        m_key = 'share_img_'+str(share_id)
        images = self.mcache.get(m_key)
        if not images:
            images = []
            share_service.set_db(self.db)
            query = share_service.get_share_images(share_id)
            if query.count() >= 1:
                for img in query:
                    _url = img.Fimg_url.split('@')[0] if len(img.Fimg_url.split('@')) <= 1 else img.Fimg_url.split('@')[:-1]
                    images.append(_url+'@20q_0r.jpg')
                self.mcache.set(m_key,images,86400)
        return images















