#encoding:utf-8
__author__ = 'binpo'
from common.base import MobileBaseHandler
from datacache.count_cache import cache_views,cache_replys,count_category_tipics
import ujson
import datetime
from services.users.user_services import UserServices
from services.topics.topic_services import TopicServices
from services.company.company_services import CompanyServices
from services.schedules.schedules_service import ScheduleService
from services.share.share_service import ShareService
from services.home.home_service import HomeService
from services.work.work_services import WorkServices
from services.series.series_services import SeriesServices
from services.favorites.favorites_services import FavoritesService
from models.user_do import Users
from tornado.web import decode_signed_value
import math
import sys

user_service = UserServices()
topic_service = TopicServices()
company_service = CompanyServices()
share_service = ShareService()
schedule_service = ScheduleService()
home_servie = HomeService()
work_service = WorkServices()
series_service = SeriesServices()
favorite_service = FavoritesService()

class MobileBaseHandler(MobileBaseHandler):

    data={}

    def get_current_user(self):

        #判断从app端过来的请求
        user_id = ''
        self.get_paras_dict()
        try:

            user_agent = self.request.headers.get('Request-Type') \
                if self.request.headers.get('Request-Type') else self.qdict.get('Request-Type')

            if user_agent and user_agent == 'apicloud': #从apicloud来

                login_token = self.request.headers.get('login_token') \
                    if self.request.headers.get('login_token') else self.qdict.get('login_token')#获取客户端token

                if login_token:
                    user_json = decode_signed_value(self.application.settings["cookie_secret"], 'loginuser', login_token) #判断token合法性
                    if user_json:
                        user_info = ujson.loads(user_json)
                        user_id = user_info.get('Fid')

            else: #微信端
                user_json = self.get_secure_cookie("loginuser",None)
                if user_json:
                    user_info = ujson.loads(user_json)
                    user_id = user_info.get('Fid')

        except Exception,e:
            pass

        if user_id:#跟用户id获取用户信息
            user = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fid==user_id).scalar()
            if not user:
                return None
            user_service.set_db(self.db)
            user = ujson.dumps(user_service.user_format(user))
            return ujson.loads(user)

        return None

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

    def echo(self, template, context=None, globals=None,layout=''):
        data = self.render(template, context, globals,layout)
        self.write(data)

    def write_json(self,data):
        '''
        :todo 返回json数据
        :param data:
        :return:
        '''
        return self.write(ujson.dumps(data))

    def execute_datetime(self,inputtime):
        execute_time = (datetime.datetime.now()-inputtime)
        total_seconds = execute_time.total_seconds()
        if total_seconds<60:
            return str(int(total_seconds))+'秒前'
        elif total_seconds<60*60:
            return str(int(total_seconds/60))+'分钟前'
        elif total_seconds<60*60*24:
            return str(int(total_seconds/(60*60)))+'小时前'
        else:
            return str(execute_time.days)+'天前'

    def set_page_view(self,table,id_key,page_view=0):
        '''
        :浏览量数据统计
        :param table:
        :param id_key:
        :param page_view:
        :return:
        '''
        try:
            if self.rcache:
                count = self.rcache.hget(table, id_key)
                if not count:
                    count=page_view
                self.rcache.hset(table, id_key, int(count)+1)
                #cache_views(table,int(id_key),count=page_view)
        except:
            pass

    def set_reply_count(self,table,id_key,default_count=0):
        '''
        :todo 设置回复数
        :param table:
        :param id_key:
        :param count:
        :return:
        '''
        try:
            if self.rcache:
                count = self.rcache.hget(table+'_count_reply', id_key)
                if not count:
                    count=default_count
                self.rcache.hset(table+'_count_reply', id_key, int(count)+1)

        except:
            pass

    def child_account_key(self,user):
        user_service.set_db(self.db)
        if 'merchant' in user.Frole_codes:
            company = user_service.get_company_merchant_id(user.Fid)
            if company:
                return {'Fcompany_id':company.Fid,'Fmerchant_id':user.Fid,'Fcompany_name':company.Fcompany_name}
            else:
                return {'Fcompany_id':'','Fmerchant_id':'','Fcompany_name':''}

        if user.Fpermission:
            user_id = user.Fid
            data = user_service.get_merchant_id_by_child_acount(user_id)
            return data

    def get_user_info(self,key):
        '''
        todo:获取用户信息
        :param key: id
        :return:
        '''
        m_key = 'user_'+str(key)
        data = self.mcache.get(m_key)
        if not data:
            user_service.set_db(self.db)
            user = user_service.get_user_by_id(key)
            data = {'nick_name':user.Fnick_name,'photo_url':user.Fphoto_url}
            self.mcache.set(m_key,data,86400)
        return data


    def delete_user_info(self,key):
        '''
        todo:删除缓存信息
        :param key:
        :return:
        '''
        m_key = 'user_'+str(key)
        data = self.mcache.get(m_key)
        if data:
            self.mcache.delete(m_key)

    def get_sns_info(self,user_id,topic_id,sns_type):
        '''
        todo:获取用户点赞信息
        :param user_id:
        :param topic_id:
        :return:
        '''
        my_key= str(user_id)+'topic_sns'+str(topic_id)+str(sns_type)
        data = self.mcache.get(my_key)
        if not data:
            topic_service.set_db(self.db)
            is_ok = topic_service.check_sns_exist(user_id,topic_id,sns_type) #是否点赞或关注
            if is_ok:
                data = 1
                self.mcache.set(my_key,data)
            else:
                data = 0
                self.mcache.set(my_key,data)
        return data

    def delete_sns_info(self,user_id,topic_id,sns_type):
        '''
        todo:删除点赞信息
        :param user_id:
        :param topic_id:
        :return:
        '''
        my_key= str(user_id)+'topic_sns'+str(topic_id)+str(sns_type)
        data = self.mcache.get(my_key)
        if data or data == 0:
            self.mcache.delete(my_key)

    def get_total_page(self,lst,page_size):
        total_page = (len(lst) % page_size==0) and (len(lst)/page_size) or int(math.ceil(len(lst) / page_size))+1
        return total_page

    def get_topics_info(self,topic_id,topic_type):
        '''
        todo:查询话题或者回复
        :param id:
        :param topic_type:
        :return:
        '''
        if topic_type == 'topic_':
            cache_key = 't_'+str(topic_id)
        elif topic_type == 'reply_':
            cache_key = 'r_'+str(topic_id)
        data = self.mcache.get(cache_key)
        if not data:
            topic_service.set_db(self.db)
            topic = topic_service.get_topic_by_id(topic_id,topic_type)
            data = self.obj_to_dict(topic,
                                    ['Fid','Fuser_id','Ftopic_id','Fparent_id','Ffull_parent_id',
                                     'Fparent_user_id','Fcotegory_id',
                                     'Freply_index','Ftitle','Fcontent','Fis_top','Fis_essence',
                                     'Fis_prime','Fis_hot','Ftags','Fis_lock','Fpage_view',
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
            my_key = 't_images_'+str(topic_id)
        elif type == 'reply':
            my_key = 'r_images_'+str(topic_id)
        data = self.mcache.get(my_key)
        if not data:
            topic_service.set_db(self.db)
            data = []
            for image in topic_service.get_topic_images_list(topic_id,type):
                data.append({'img':self.img_compression(image.Fimg_url,image.Fimg_size),'original_img':image.Fimg_url})
            self.mcache.set(my_key,data,86400)
        return data

    def get_sns_users_info(self,topic_id,sns_type):
        '''
        todo:获取话题或者跟帖的关注或点赞用户信息
        :param topic_id:
        :param sns_type:
        :return:
        '''
        if sns_type == 2:
            cache_key = str(topic_id)+'attention'
        elif sns_type == 1:
            cache_key = str(topic_id)+'praise'
        lstdata = self.mcache.get(cache_key)
        if not lstdata:
            lstdata = []
            count = 0
            topic_service.set_db(self.db)
            for sns in topic_service.get_sns_topics_list(topic_id=topic_id,sns_type=sns_type):
                lstdata.append(sns.Fuser_id)
                count += 1
            self.mcache.set(cache_key,lstdata,86400)
        return lstdata,count

    def get_reply_count_info(self,follow_id):
        '''
        todo:获取跟帖的回复数量信息
        :param follow_id: 跟帖ID
        :return:
        '''
        cache_key = 'r_list'+str(follow_id)
        lstdata = self.mcache.get(cache_key)
        if not lstdata:
            lstdata = []
            topic_service.set_db(self.db)
            count,comments = topic_service.get_reply_of_reply(follow_id)
            for comment in comments:
                tmp_dic = self.obj_to_dict(comment,['Fid','Ffull_parent_id','Fuser_id','Fparent_user_id','Fcreate_time','Fcontent'])
                lstdata.append(tmp_dic)
            self.mcache.set(cache_key,lstdata,86400)
        return lstdata

    def delete_reply_count_info(self,follow_id):
        '''
        todo:删除回复数量信息
        :param follow_id:
        :return:
        '''
        cache_key = 'r_list'+str(follow_id)
        data = self.mcache.get(cache_key)
        if data:
            self.mcache.delete(cache_key)

    def is_page(self,total_page,page):
        '''
        todo:查询还有无下一页
        :param total_page:
        :param page:
        :return:
        '''
        if total_page - int(page) > 0:
            is_page = 1
        else:
            is_page = 0
        return is_page



    def is_favorite(self,favorite_type,favorite_id):
        '''
        todo:判断用户是否收藏某产品
        :param favorite_type:
        :param favorite_id:
        :return:
        '''
        if self.get_current_user():
            user_id = self.get_current_user().get('Fid')
            m_key = str(user_id)+'favorite'+str(favorite_type)+str(favorite_id)
            if self.mcache.get(m_key):
                return 1
        return 0


class MobileHandler(MobileBaseHandler):

    def get(self,args=None,**kwargs):
        self.redirect('/mobile/user/index/')
