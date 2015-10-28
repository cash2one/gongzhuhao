#encoding:utf-8
__author__ = 'wangjinkuan'

from common.base import AdminBaseHandler
from services.topics.topic_services import TopicServices
from utils.upload_utile import upload_to_oss,delete_from_oss
from tornado.options import options
# from apps_crm.albums.photos_handler import img_compression
import tornado.web
import ujson
import datetime

topics_service = TopicServices()

class TagsCreateHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.echo('ops/topic/create_tag.html')

    @tornado.web.authenticated
    def post(self):
        self.get_paras_dict()
        topics_service.set_db(self.db)
        try:
            topics_service.create_topic_tag(**self.qdict)
        except Exception,e:
            return self.write(ujson.dumps({'stat':'1001','info':'exception occured:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','info':''}))

class TagsListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self):
        topics_service.set_db(self.db)
        self.get_paras_dict()
        try:
            tags = topics_service.query_topic_tags(**self.qdict)
            page_data = self.get_page_data(tags)
        except Exception,e:
            return self.echo('ops/500.html')
        self.echo('ops/topic/tag.html',{'page_data':page_data,'page_html':page_data.render_admin_html()})

class TopicCategoryCreateHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self,parent_id):
            topic_category = ''
            self.echo('ops/topic/category.html',{'topic_category':topic_category})

    def post(self, parent_id):
        self.get_paras_dict()
        topics_service.set_db(self.db)
        if parent_id:
            self.qdict['parent_id'] = parent_id
        try:
            topic_category = topics_service.create_topic_category(**self.qdict)
            if self.request.files.get('category_img'):
                is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET, param_name='category_img',file_type='img')
                if is_ok:
                    for file in filenames:
                        data = {}
                        img_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                        data['Fimg_url'] = img_url
                        topics_service.update_category(topic_category.Fid,**data)
                else:
                    return self.write(ujson.dumps({'stat':'1005','info':'图片上传失败'}))
        except Exception,e:
            return self.write(ujson.dumps({'stat':'1001','info':'exception occured:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','info':''}))

class EditTopicCategoryHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self,topic_category_id):
        topics_service.set_db(self.db)
        try:
            topic_catetory = topics_service.get_category_by_id(topic_category_id)
        except Exception,e:
            self.echo('ops/500.html')
        self.echo('ops/topic/category.html',{'topic_category':topic_catetory})

    @tornado.web.authenticated
    def post(self, topic_category_id):
        self.get_paras_dict()
        topics_service.set_db(self.db)
        category_name = self.qdict.get('category_name','')
        category_description = self.qdict.get('category_description','')
        category_sort = self.qdict.get('sort','')
        data = {}
        if category_name or category_description:
            data['Fname'] = self.qdict.get('category_name')
            data['Fdescription'] = self.qdict.get('category_description')
        elif category_sort: #排序
            data['Fsort'] = category_sort
        else: #删除
            data['Fdeleted'] = 1
        try:
            if self.request.files.get('category_img'):
                is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET, param_name='category_img',file_type='img')
                if is_ok:
                    for file in filenames:
                        data = {}
                        img_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                        data['Fimg_url'] = img_url
                else:
                    return self.write(ujson.dumps({'stat':'1005','info':'图片上传失败'}))
            topics_service.update_category(topic_category_id,**data)
        except Exception,e:
            print e
            return self.write(ujson.dumps({'stat':'1001','info':'exception occured:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','info':''}))

class TopicCategoryListHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self,parent_id):
        topics_service.set_db(self.db)
        try:
            if parent_id:
                topic_categorys = topics_service.query_topic_category(parent_id)
            else: #一级话题分类
                topic_categorys = topics_service.query_topic_category()
            page_data = self.get_page_data(topic_categorys)
        except Exception,e:
            self.echo('ops/500.html')
        self.echo('ops/topic/category_list.html',{'page_data':page_data,'page_html':page_data.render_admin_html()})

class TopicListHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.get_paras_dict()
        topics_service.set_db(self.db)
        topics_category = topics_service.get_category_list()
        try:
            topics_service.check_end_date_topics(c_top=1,c_essence=1)
            topics = topics_service.get_topic_list(order_by='Fcreate_time desc',**self.qdict)
            page_data = self.get_page_data(topics)
            page_html = page_data.render_admin_html()
        except Exception,e:
            self.echo('ops/500.html')
        self.echo('ops/topic/topic_list.html',{'page_data':page_data,'page_html':page_html,'topic_category':topics_category})

class TopicOperationHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        topics_service.set_db(self.db)
        self.get_paras_dict()
        if not self.qdict.get('operation'):
            return self.write(ujson.dumps({'stat':'error','info':'请选择操作类型'}))
        if (not self.qdict.get('essence_date')) and (not self.qdict.get('top_date')):
            return self.write(ujson.dumps({'stat':'error','info':'请填写相应操作类型的结束时间'}))
        try:
            data = {}
            if '1' in self.qdict.get('operation'):
                data['Fis_top'] = 1
                data['Ftop_end_date'] = self.qdict.get('top_date')
                data['Fmodify_time'] = datetime.datetime.now()
            if '2' in self.qdict.get('operation'):
                data['Fis_essence'] = 1
                data['Fessence_expire_time'] = self.qdict.get('essence_date')
                data['Fmodify_time'] = datetime.datetime.now()
            topic_id = self.qdict.get('topic_id')
            topics_service.update_topic(topic_id,**data)
        except Exception,e:
            print e.message
            self.echo('ops/500.html')
        self.write(ujson.dumps({'stat':'ok','info':''}))

class TopicDeleteHandler(AdminBaseHandler):

    def get(self, topic_id,*args, **kwargs):

        topics_service.set_db(self.db)
        data = {}
        data['Fdeleted'] = 1
        try:
            topics_service.update_topic(topic_id,**data)
        except Exception,e:
            print e.message

        return self.write(ujson.dumps({'stat':'ok','info':'','data':''}))

class TopicBannerHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.echo('ops/topic/create_banner.html')

    @tornado.web.authenticated
    def post(self):
        topics_service.set_db(self.db)
        self.get_paras_dict()
        try:
            if self.request.files.get('banner_img'):
                file_prex = '/'.join(('topic','banner'))
                is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET,file_prex=file_prex,param_name='banner_img',file_type='img')
                if is_ok:
                    for file in filenames:
                        img_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                        self.qdict['img_url'] = img_url
                        topics_service.create_topic_banner(**self.qdict)
                else:
                    return self.write(ujson.dumps({'stat':'1005','info':'图片上传失败'}))
        except Exception,e:
            return self.write(ujson.dumps({'stat':'1001','info':'exception occured:'+e.message}))
        self.write(ujson.dumps({'stat':'1000','info':''}))

class BannerQueryHandler(AdminBaseHandler):

    @tornado.web.authenticated
    def get(self):
        topics_service.set_db(self.db)
        topics_service.query_topic_category()
        banners = topics_service.get_topic_banner_list()
        self.echo('ops/topic/banner_list.html',{'banners':banners})



