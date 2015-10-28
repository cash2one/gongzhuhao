#encoding:utf-8
__author__ = 'binpo'

from apps_mobile.mobile_base import MobileBaseHandler
from services.topics.topic_services import TopicServices
from services.users.user_services import UserServices
from apps_web.album.photo_upload_handler import img_compression
from utils.datetime_util import datetime_format
from utils.upload_utile import upload_to_oss
from celery_tasks.tasks_cache import count_topics_sns_set
from tornado.options import options
import tornado.web
import datetime
import ujson
import sys
import re
import tornado

from setting import WX_GZH_AppID,WX_GZH_AppSecret
from datacache.datacache import PageDataCache
from utils.sign import sign

topic_services = TopicServices()
user_serveces = UserServices()

PAGE_SIZE = 20

class TopicCreateHandler(MobileBaseHandler):#创建话题操作

    @tornado.web.authenticated
    def get(self,category_id,type_num):

        self.echo('views/topic/create_topic.html',{'category_id':category_id,'type_num':type_num})

    def post(self,category_id,type_num):
        try:
            user_serveces.set_db(self.db)
            self.get_paras_dict()
            if not self.qdict.get('title') or not self.qdict.get('content'):
                return self.write_json({'stat':'1006','info':'标题和内容不能为空'})
            user_id =self.get_current_user().get('Fid')
            self.qdict['user_id'] = user_id
            self.qdict['category_id'] = category_id
            topic_services.set_db(self.db)

            imgs = [x for x in ujson.loads(self.get_argument('img', '[]')) if x ]
            self.qdict['total_img'] = len(imgs)
            topic = topic_services.create_topic(**self.qdict)
            for img in imgs:
                topic_services.create_topic_img(topic.Fid,user_id,img['url'].split('@')[0],'topic',img['size'])
            self.write_json({
                            'stat':'ok',
                            'msg':'',
                            'topic_user_id': topic.Fuser_id,
                            'topic_id':topic.Fid,
                            'category_id':category_id,
                            'type_num':type_num
                            })
        except Exception,e:
            pass
            self.echo('views/500.html')

class TopicReplyCreateHandler(MobileBaseHandler):

    @tornado.web.authenticated
    def get(self,topic_id,type_num,parent_id=None):
        is_reply=False
        if not parent_id or parent_id==1:
            is_reply = True
        self.echo('views/topic/reply_topic.html',
                    {'topic_id':topic_id,
                     'parent_id':parent_id,
                     'is_reply':is_reply,
                     'type_num':type_num
                    })

    def post(self,topic_id,type_num,parent_id=None):
        '''
        todo:创建回复
        :param topic_id:话题id
        :param parent_id: 父帖id
        :return:
        '''
        try:
            topic_services.set_db(self.db)
            self.get_paras_dict()
            if not self.qdict.get('content'):
                return self.write_json({'stat':'1006','info':'内容不能为空'})
            if parent_id and int(parent_id): #评论或回复
                self.qdict['parent_id'] = parent_id
                full_parent_id = self.get_topics_info(parent_id,'reply_').get('Ffull_parent_id')
                if full_parent_id == '0':
                    self.qdict['full_parent_id'] = '/'+str(parent_id)+'/'
                    self.delete_reply_count_info(parent_id)
                else:
                    if full_parent_id.endswith('/'):
                        self.qdict['full_parent_id'] = full_parent_id+str(parent_id)
                    else:
                        self.qdict['full_parent_id'] = full_parent_id+'/'+str(parent_id)
                    self.delete_reply_count_info(full_parent_id.split('/')[1])
            user_id = self.get_current_user().get('Fid')
            self.qdict['topic_id'] = topic_id
            self.qdict['user_id'] = user_id
            reply = topic_services.create_topic_reply(**self.qdict)
            imgs = [x for x in ujson.loads(self.get_argument('img', '[]')) if x ]
            for img in imgs:
                topic_services.create_topic_img(reply.Fid,user_id,img['url'].split('@')[0],'reply',img['size'])
            category_id = self.get_topics_info(topic_id,'topic_').get('Fcotegory_id')
            self.write_json({
                            'stat':'ok','msg':'',
                            'topic_id':topic_id,
                            'topic_user_id': reply.Fuser_id,
                            'category_id':category_id,
                            'type_num':type_num
                            })
        except Exception,e:
            pass
            self.echo('views/500.html')

class TopicPhotosUploadHandler(MobileBaseHandler):

    def post(self):
        date_format_prefix = datetime_format(format='%Y%m%d')
        try:
            rsp={'files':[],'stat':'err','msg':''}
            file_prex = '/'.join(['topics',str(self.get_current_user().get('Fid')),date_format_prefix])
            is_ok,filenames = upload_to_oss(self,options.IMG_BUCKET,param_name='files',file_type='img',file_prex=file_prex,max_size=3)
            if is_ok:
                for f in filenames:
                    rsp['files'].append(
                        {
                        "name": f.get('file_name'),
                        "size": f.get('size'),
                        "type": f.get('content_type'),
                        "url": options.IMG_DOMAIN+'/'+f.get('full_name')+img_compression(f.get('size')),
                        "full_name":f.get('full_name'),
                        }
                    )
                rsp['stat'] = 'ok'
                rsp['files'][0]['id'] = '0'
            else:
                rsp['stat'] = 'err'
                rsp['msg'] = filenames
            return self.write(ujson.dumps(rsp))

        except Exception,e:
            pass
            self.echo('views/500.html')

class TopicQueryHandler(MobileBaseHandler):#查询话题操作

    def get(self,category_id,type_num,page):
        '''
        :param category_id: 话题模版id
        :param page: 页码
        :return:
        '''
        if not page or int(page) <= 1:
            page = 1
        topic_services.set_db(self.db)
        try:
            topic_category = topic_services.get_category_by_id(category_id)
            if type_num == '1':
                lst,is_page = get_new_topics_list(self,topic_services,category_id,page)
            elif type_num == '2':
                lst,is_page = get_reply_topics_list(self,topic_services,category_id,page)
            else:
                lst,is_page = get_essence_topics_list(self,topic_services,category_id,page)

            if int(page) > 1 and self.request.uri.startswith('/mobile/topics/'):
                return self.others_page(lst,is_page,type_num,category_id,topic_category)

            if self.request.uri.startswith('/api/json/'):
                category_dict = self.obj_to_dict(topic_category,['Fname','Fimg_url','Fdescription','Ftopic_count'])
                category_dict['Fpage_view'] = self.get_page_view('t_topic_category',category_id,topic_category.Fpage_view)
                self.write_json({'stat':'ok',
                                 'data':{'topics':lst,
                                         'category_info':category_dict,
                                         'has_next':is_page,
                                        },
                                 'info':''
                                })
            else:
                self.echo('views/topic/topic_page.html',
                         {'topics':lst,
                          'topic_category':topic_category,
                          'page_view':self.get_page_view('t_topic_category',category_id,topic_category.Fpage_view),
                          'type_num':type_num,
                          'has_next':is_page,
                          'category_id':category_id
                         },
                         layout='views/topic/topic_list.html')
            self.set_page_view('t_topic_category',category_id,0)
        except Exception,e:
            pass
            self.echo('views/500.html')

    def others_page(self,lst,is_page,type_num,category_id,topic_category):
        _html = self.render('views/topic/topic_page.html',
                            {'topics':lst,
                             'page_view':self.get_page_view('t_topic_category',category_id,topic_category.Fpage_view),
                             'type_num':type_num,
                             'category_id':category_id
                            })
        self.write_json({'stat':'ok','html':_html,'has_next':is_page})

def get_new_topics_list(self,db,category_id,page):
    '''
    todo:获取最新发布
    :param category_id:
    :return:
    '''
    lst = []
    db.check_end_date_topics(c_top=1,c_essence=1)
    topics_nte = db.query_topics(order_by='Fcreate_time desc',category_id=category_id)
    page_topics = self.get_page_data(topics_nte,page_size=PAGE_SIZE,page=page)
    if int(page) == 1:
        topics_te = topic_services.get_topic_list(is_top=1,is_essence=1,category_id=category_id,order_by='Fmodify_time desc') #置顶或加精话题
        topics = topics_te.all()+page_topics.result.all()
    else:
        topics = page_topics.result
    topics_format(self,topics,lst)
    return lst,self.is_page(page_topics.page_num,page=page)

def get_reply_topics_list(self,db,category_id,page):
    '''
    todo:获取最新回复
    :param category_id:
    :param page:
    :return:
    '''
    lst = []
    db.check_end_date_topics(c_top=1,c_essence=1)
    topics = db.get_last_reply_topic_list(category_id=category_id)
    page_topics = self.get_page_data(topics,page_size=PAGE_SIZE,page=page)
    topics_format(self,page_topics.result,lst)
    return lst,self.is_page(page_topics.page_num,page=page)

def get_essence_topics_list(self,db,category_id,page):
    '''
    todo:获取精华
    :param category_id:
    :param page:
    :return:
    '''
    lst = []
    db.check_end_date_topics(c_essence=1)
    topics = db.get_topic_list(is_essence=1,category_id=category_id)
    page_topics = self.get_page_data(topics,page_size=PAGE_SIZE,page=page)
    topics_format(self,page_topics.result,lst)
    return lst,self.is_page(page_topics.page_num,page=page)

def topics_format(self,topics,lst):
    '''
    todo:格式化
    :param topics:
    :param lst:
    :return:
    '''
    for topic in topics:
        user = self.get_user_info(str(topic.Fuser_id))
        tmp_dict = self.obj_to_dict(topic,['Fid','Fuser_id','Ftitle','Fis_top','Fis_essence','Ftotal_assess'])
        tmp_dict['photo'] = 1 if topic.Ftotal_img else 0,
        tmp_dict['nick_name'] = user.get('nick_name')
        tmp_dict['head_url'] = user.get('photo_url')
        tmp_dict['time'] = self.execute_datetime(topic.Fcreate_time)
        tmp_dict['last_reply_time'] = self.execute_datetime(topic.Flast_reply_time)
        tmp_dict['has_img'] = 1 if len(self.get_topic_img(topic.Fid,'topic')) > 0 else 0
        lst.append(tmp_dict)

class TopicDetailHandler(MobileBaseHandler):#查询一个话题的detail数据

    def get(self,topic_id,page,type_num,category_id):
        '''
        :param topic_id:
        :param page:页码
        :param operation:默认、只看楼主、倒序排列、收藏该贴(1,2,3,4)
        :return:
        '''
        if not page or int(page) <= 1:
            page = 1
        topic_services.set_db(self.db)
        user_agent = self.request.headers.get('Request-Type')
        lst_follow = []
        lst_praise_head_url = []
        topic = self.get_topics_info(topic_id,'topic_')
        topic_images = self.get_topic_img(topic_id,'topic')

        lst_user_id,praise_count = self.get_sns_users_info(topic_id,1)
        for user_id in lst_user_id:
            lst_praise_head_url.append({'praise_img':self.get_user_info(str(user_id)).get('photo_url')}) #点赞头像
        try:
            query = topic_services.get_topic_reply_list(topic_id=topic_id,parent_id=0) #跟帖
            follows = self.get_page_data(query,page_size=PAGE_SIZE,page=page)

            for follow in follows.result:
                follow_images = self.get_topic_img(follow.Fid,'reply')
                tmp_dic = self.obj_to_dict(follow,['Fid','Freply_index'])

                content = follow.Fcontent
                if user_agent and user_agent == 'apicloud':
                    for expression in re.findall(r'\[em\_\d*\]',content):
                        content = content.replace(expression,'<img src="../../images/faces/'+re.findall(r'\d+',expression)[0]+'.gif" border="0" />')
                else:
                    for expression in re.findall(r'\[em\_\d*\]',content):
                        content = content.replace(expression,'<img src="/static/images/faces/'+re.findall(r'\d+',expression)[0]+'.gif" border="0" />')
                tmp_dic['Fcontent'] = content

                tmp_dic.update({
                                'time':self.execute_datetime(follow.Fcreate_time),
                                'head_url':self.get_user_info(str(follow.Fuser_id)).get('photo_url'),
                                'nick_name':self.get_user_info(str(follow.Fuser_id)).get('nick_name'),
                                'images':follow_images
                               })
                tmp_dic['has_count'] = len(self.get_reply_count_info(follow.Fid))>=1 and 1 or 0
                tmp_dic['replies'] = self.get_comments(follow.Fid)
                lst_follow.append(tmp_dic)

            if int(page) > 1:
                if self.request.uri.startswith('/api/json/'):
                    data = {
                            'follows':lst_follow,
                            'has_next':self.is_page(follows.page_num,page=page)
                           }
                    return self.write_json({'stat':'ok','data':data,'info':''})
                else:
                    return self.others_page(lst_follow,self.is_page(follows.page_num,page=page,),topic_id,category_id,type_num,page)

            content = topic.get('Fcontent')

            if user_agent and user_agent == 'apicloud':
                for expression in re.findall(r'\[em\_\d*\]',content):
                    content = content.replace(expression,'<img src="../../images/faces/'+re.findall(r'\d+',expression)[0]+'.gif" border="0" />')
            else:
                for expression in re.findall(r'\[em\_\d*\]',content):
                    content = content.replace(expression,'<img src="/static/images/faces/'+re.findall(r'\d+',expression)[0]+'.gif" border="0" />')

            self.set_page_view('t_topics',topic.get('Fid'),0)#浏览数据写入memcache

            #微信-配置
            page_cache = PageDataCache(self.db)
            access_token = page_cache.get_access_token(WX_GZH_AppID,WX_GZH_AppSecret)
            jsapi_ticket = page_cache.get_jsapi_ticket(access_token)
            share_url = 'http://m.gongzhuhao.com' + '/mobile/topic/detail/'+str(topic_id)+'/'+str(page)
            wx_sign = sign(WX_GZH_AppID, jsapi_ticket, share_url)
            dic_sign = wx_sign.get_sign()

            topic_info = {
                             'topic_title':topic.get('Ftitle'),
                             'topic_content':content,
                             'topic_images':topic_images,
                             'nick_name':self.get_user_info(str(topic.get('Fuser_id'))).get('nick_name'),
                             'head_url':self.get_user_info(str(topic.get('Fuser_id'))).get('photo_url'),
                             'time':self.execute_datetime(datetime.datetime.strptime(topic.get('Fcreate_time'),'%Y-%m-%d %H:%M:%S'))
                         }

            if self.request.uri.startswith('/api/json/'):
                self.write_json({'stat':'ok',
                                 'data':{'head_info':topic_info,
                                         'follows':lst_follow,
                                         'has_next':self.is_page(follows.page_num,page=page)
                                        },
                                 'info':''
                                })
            else:
                data_mobile = {
                                 'follows':lst_follow,
                                 'praise_urls':lst_praise_head_url,
                                 'praise_count':praise_count,
                                 'dic_sign':dic_sign,
                                 'share_url':share_url,
                                 'topic_id':topic_id,
                                 'page':page,
                                 'type_num':type_num,
                                 'category_id':category_id,
                                 'has_next':self.is_page(follows.page_num,page=page)
                              }
                topic_info.update(data_mobile)
                self.echo('views/topic/topic_detail_page.html',topic_info,layout='views/topic/topic_detail.html')
        except Exception,e:
            pass
            self.echo('views/500.html')

    def others_page(self,follows,is_page,topic_id,category_id,type_num,page):
        _html = self.render('views/topic/topic_detail_page.html',
                            {
                                'follows':follows,
                                'topic_id':topic_id,
                                'category_id':category_id,
                                'type_num':type_num,
                                'page':page
                            })
        self.write_json({'stat':'ok','html':_html,'has_next':is_page})

    def get_comments(self,follow_id):
        '''
        todo:获取回复list
        :param follow_id:
        :return:
        '''
        replies = []
        topic = self.get_topics_info(follow_id,'reply_')
        try:
            comments = self.get_reply_count_info(follow_id)
            for comment in comments:
                content = comment.get('Fcontent')
                for expression in re.findall(r'\[em\_\d*\]',content):
                    content = content.replace(expression,'<img src="/static/images/faces/'+re.findall(r'\d+',expression)[0]+'.gif" border="0" />')

                if comment.get('Ffull_parent_id').endswith('/'):
                    is_reply = len(comment.get('Ffull_parent_id').split('/')) > 3 and 1 or 0
                else:
                    is_reply = len(comment.get('Ffull_parent_id').split('/')) > 2 and 1 or 0

                replies.append({
                                'is_reply':is_reply,
                                'id':comment.get('Fid'),
                                'reply_name':self.get_user_info(str(comment.get('Fuser_id'))).get('nick_name'),
                                'is_floor':1 if comment.get('Fuser_id') == topic.get('Fparent_user_id') else 0,
                                'reply_content':content,
                                'reply_parent_name':self.get_user_info(str(comment.get('Fparent_user_id'))).get('nick_name'),
                                'parent_head_url':self.get_user_info(str(comment.get('Fparent_user_id'))).get('photo_url'),
                                'is_parent_floor':1 if comment.get('Fparent_user_id') == topic.get('Fparent_user_id') else 0,
                                'time':self.execute_datetime(datetime.datetime.strptime(comment.get('Fcreate_time'),'%Y-%m-%d %H:%M:%S')),
                               })
            return replies
        except Exception,e:
            pass
            self.echo('views/500.html')


# class TopicSnsHandler(MobileBaseHandler):
#
#     @login_control()
#     def get(self,topic_id,sns_type,topic_type,db_operation):
#         '''
#         :param topic_id: 话题id或者话题回复id
#         :param sns_type: 收藏还是点赞 (2,1)
#         :param topic_type: 话题or回复 (1,2)
#         :param db_operation:删除还是新增 0,1
#         :return:
#         '''
#         try:
#             if int(sns_type) not in (1,2) or int(topic_type) not in (1,2) or int(db_operation) not in (0,1):
#                 raise SiteError('参数类型不正确')
#             topic_services.set_db(self.db)
#             user_id = self.get_current_user().get('Fid')
#             topic_services.create_topic_sns(topic_id,user_id,sns_type,topic_type,operation=int(db_operation))
#             self.delete_sns_info(user_id,topic_id,sns_type)
#             data={'stat':'1000','info':'操作成功'}
#             # if sns_type == '2' and db_operation == 1: #点赞操作
#             #     count_topics_sns_set('t_user_topic_sns',topic_id)
#         except Exception,e:
#             pass
#             data={'stat':'1001','info':'exception:'+e.message}
#         self.write_json(data)