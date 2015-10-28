#!/usr/bin/env python2.7
# encoding:utf-8
__author__ = 'dozy-sun'
from common.base import BaseApiHandler as BaseHandler
from services.topics.topic_services_pc import TopicServices
from services.users.user_services import UserServices
from utils.date_util import time_passed
from datacache.datacache import UserMsgCache,TopicUserSnsCache


from common.base import SiteError
import ujson
import sys
import tornado
from celery_tasks.tasks import create_user_message
import StringIO
import base64
import re
from utils.date_util import yyyydddddatetime
_TOPIC_CATEGORY_DEFAULT_URL = "/static/crm/images/default.gif"
topic_services = TopicServices()
user_serveces = UserServices()

PAGE_SIZE=20

class TopicIndexHandler(BaseHandler):
    def get(self,category_id=None,type_num='1'):

        type_num = type_num if type_num else '1'
        topic_services.set_db(self.db)
        user_serveces.set_db(self.db)
        topic_categorys = topic_services.query_topic_category()
        topic_cate = []
        cate_basic_info = {}
        for topic_category in topic_categorys:
            cate_info = {'id':topic_category.Fid,'name':topic_category.Fname,
                            'url':topic_category.Fimg_url+'@200h.jpg' if topic_category.Fimg_url else _TOPIC_CATEGORY_DEFAULT_URL,
                            'desc':topic_category.Fdescription,'topic_count':topic_category.Ftopic_count,
                            'page_view':11,
                        }

            topic_cate.append(cate_info)
            if category_id and int(category_id) == cate_info['id']:
                cate_basic_info = cate_info

        if not cate_basic_info: #选中分类的基本信息
            cate_basic_info = topic_cate[0]

        data = {}

        data['category_id'] = int(category_id) if category_id else ''
        data['is_essence'] = 1 if type_num == '3' else 0
        data['order_by'] = 'Fis_top desc, Fis_essence desc, Fmodify_time desc' if type_num == '1' else 'Fis_top desc, Fis_essence desc, Flast_reply_time desc ' if type_num == '2' else 'Fcreate_time'
        lst_new = [] #最新发布

        topics = topic_services.query_topics_all(**data)
        page_data = self.get_page_data(topics, int(self.get_argument('page_size', PAGE_SIZE)))
        for topic in page_data.result:
                user = user_serveces.get_user_by_id(topic.Fuser_id)

                lst_new.append({
                    'Fid':topic.Fid,
                    'Fuser_id':topic.Fuser_id,
                    'Ftitle':topic.Ftitle,
                    'Fcontent': topic_services.filter_img_tag(topic.Fcontent),
                    'Fis_top':topic.Fis_top,
                    'Fis_essence':topic.Fis_essence,
                    'Ftotal_assess':topic.Ftotal_assess,
                    'Fpage_view':self.get_page_view('t_topics',topic.Fid,topic.Fpage_view),
                    'Fpraise': topic.Fpraise,
                    #'imgs': [[image.Fid, self.img_compression(image.Fimg_url,image.Fimg_size)] for image in topic_services.query_topic_imgs(topic.Fid).limit(5)],
                    'photo':1 if topic.Ftotal_img else 0,
                    'nick_name':user.Fnick_name,
                    'head_url': user.Fphoto_url,
                    'time':time_passed(topic.Fcreate_time)})

        rec_topic = topic_services.query_topics_all(recommend=1).first()
        if not rec_topic:
            rec_topic = topic_services.query_topics_all(order_by=' Ftotal_assess desc').first()   #活跃榜
        top_week, top_month = topic_services.get_top_active_user_topic()

        self.title = '最火的结婚交流社区-网友互助爆料!'
        self.keywords = '结婚求互'
        self.description = ''
        self.echo('view/qa/new_topic_list.html',{
            'topic_cate': topic_cate,
            'topic_list': lst_new,
            'total_page': page_data.page_num,
            'cate_basic_info': cate_basic_info,
            'base_data': data,
            'is_admin':True if self.current_user and 'admin' in self.current_user['Frole_codes'] else False,
            'rec_topic': rec_topic,
            'top_week': top_week,
            'top_month': top_month,
            'user_db': UserMsgCache(self.db),
            'cur_type': 'topic',
            'time_passed': time_passed,

        })
        '''
        self.echo('view/qa/topic_list.html',{
            'topic_cate': topic_cate,
            'topic_list': lst_new,
            'total_page': page_data.page_num,
            'cate_basic_info': cate_basic_info,
            'base_data': data,
            'is_admin':True if self.current_user and 'admin' in self.current_user['Frole_codes'] else False,
            'hot_topic': hot_topic,
            'top_week': top_week,
            'top_month': top_month,
            'user_db': UserMsgCache(self.db),
            'cur_type': 'topic',

        '''

    def post(self, *args, **kwargs):
        #生成二维码
        rsp = {}
        url = self.request.full_url()
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()

        rsp['stat'] = 'ok'
        rsp['data'] = base64.b64encode(img_data)


class TopicQueryHandler(BaseHandler):#查询话题操作

    #@login_control()
    def get(self,category_id=None,type_num=None):
        rsp = {'stat': 'err'}
        topic_services.set_db(self.db)
        user_serveces.set_db(self.db)
        category_id = int(category_id)
        if category_id:
            topic_category = topic_services.get_category_by_id(category_id)
            if not topic_category:
                rsp['msg'] = '分类不存在'

            cate_info = {
            'category_url':topic_category.Fimg_url if topic_category.Fimg_url else '',
            'category_name':topic_category.Fname,
            'category_desc':topic_category.Fdescription,
            'topic_count':topic_category.Ftopic_count,
            'page_view':self.get_page_view('t_topic_category',category_id,topic_category.Fpage_view)
            }
        else:
            cate_info = {}

        data = {}
        data['category_id'] = category_id
        data['is_essence'] = 1 if self.get_argument('is_essence', '') == '3' else 0
        data['order_by'] = 'Fis_top desc, Fis_essence desc, Fcreate_time desc' if type_num == '1' else 'Fis_top desc, Fis_essence desc, Flast_reply_time desc' if type_num == '2' else 'Fcreate_time'
        lst_new = [] #最新发布

        topic_services.check_end_date_topics()
        topics = topic_services.query_topics_all( **data)
        page_data = self.get_page_data(topics, int(self.get_argument('page_size', PAGE_SIZE)))
        is_admin = True if self.current_user and 'admin' in self.current_user['Frole_codes'] else False
        for topic in page_data.result:
                user = user_serveces.get_user_by_id(topic.Fuser_id)
                lst_new.append({
                    'Fid':topic.Fid,
                    'Fuser_id':topic.Fuser_id,
                    'Ftitle':topic.Ftitle,
                    'Fcontent':topic.Fcontent,
                    'Fis_top':topic.Fis_top,
                    'Fis_essence':topic.Fis_essence,
                    'Ftotal_assess':topic.Ftotal_assess,
                    'Fpraise':topic.Fpraise,
                    'Fpage_view':self.get_page_view('t_topics',topic.Fid,topic.Fpage_view),
                    'imgs': '',#[[image.Fid, self.img_compression(image.Fimg_url,image.Fimg_size)] for image in topic_services.query_topic_imgs(topic.Fid).limit(5)],
                    'photo':1 if topic.Ftotal_img else 0,
                    'nick_name':user.Fnick_name,
                    'head_url': user.Fphoto_url,
                    'time':time_passed(topic.Fcreate_time),
                    'is_admin': is_admin,
                })

        rsp['stat'] = 'ok'
        rsp['cate_info'] = cate_info
        rsp['list'] = lst_new
        rsp['total_page'] = page_data.page_num
        rsp['cur_page'] = int(self.get_argument('page', 1))
        rsp['has_more'] = True if rsp['total_page'] > rsp['cur_page'] else False

        return self.write(ujson.dumps(rsp))


class TopicDetailHandler(BaseHandler):

    def get(self,topic_id,user_id):


        topic_services.set_db(self.db)
        user_serveces.set_db(self.db)
        user = user_serveces.get_user_by_id(user_id)
        try:
            topic = topic_services.get_topic_by_id(topic_id, user_id)
            topic_images = topic_services.get_topic_images_list(topic_id, user_id)
            if not topic:
                return self.redirect('/404')
            lst_topic_images = []
            for topic_image in topic_images:
                lst_topic_images.append({'topic_img':topic_image.Fimg_url})
            order = ' Fcreate_time desc' if self.get_argument('new', '') else ' Fcreate_time asc'
            topic_replys = topic_services.get_topic_reply_list(topic_id, order_by=order)
            page_data = self.get_page_data(topic_replys, PAGE_SIZE)

            lst_reply = []

            user_db = UserMsgCache(self.db)
            index = 0
            for reply in page_data.result:
                index += 1
                user_reply = user_db.get_user_msg(reply.Fuser_id)
                images = topic_services.get_reply_images_list(reply.Fid,reply.Fuser_id) #回复照片

                lst_images = [{'img':image.Fimg_url} for image in images]
                reply_info = {
                    'Fuser_id': reply.Fuser_id,
                    'nick_name':user_reply.get('Fnick_name'),
                    'head_url':user_reply.get('Fphoto_url'),
                    'content':reply.Fcontent,
                    'index': index,
                    'Fpraise':reply.Fpraise,
                    'images':lst_images,
                    'time':time_passed(reply.Fcreate_time),
                    'Fid':reply.Fid,
                    #'vote_judge':1 if not self.current_user else 0 if get_topic_user_sns(self.db,self.current_user['Fid'],reply.Fid,2 ) else 1,
                    'parent': ''
                }
                # print 'f_id %s  %s' % (reply.Fid, reply_info['vote_judge'])
                total_count, reply_list = topic_services.get_reply_of_reply(reply.Fid)
                tmp_replses=[]
                for r in reply_list:
                    parent_user_id = r.Fparent_user_id
                    tmp_replses.append({
                        'reply_id':r.Fid,
                        'nick_name':user_db.get_user_msg(r.Fuser_id,).get('Fnick_name'),
                        'user_id':r.Fuser_id,
                        'content':r.Fcontent,
                        'has_parent': True if parent_user_id and parent_user_id != reply.Fuser_id else False,
                        'parent_user_id': parent_user_id if parent_user_id and parent_user_id != reply.Fuser_id else '',
                        'parent_nick_name': user_db.get_user_msg(parent_user_id).get('Fnick_name') if parent_user_id and parent_user_id != reply.Fuser_id else '',
                       'time': time_passed(r.Fcreate_time)
                    })

                reply_info['has_child'] = True if total_count>0 else False
                reply_info['replies']={
                        'total_count':total_count,
                        'replies':tmp_replses
                }

                lst_reply.append(reply_info)
            topic_cate = topic_services.query_topic_category_one(id=topic.Fcotegory_id).scalar()
            if not topic_cate:
                return self.redirect('/404')
            self.set_page_view('t_topics',topic.Fid,0)
            self.set_page_view('t_topic_category', topic.Fcotegory_id)

        except Exception,e:
            self.log_exception(*sys.exc_info())
            pass
            return self.redirect('/500')

        #热门话题
        hot_topic = topic_services.query_topics_all(order_by=' Ftotal_assess desc').limit(5)
        #活跃榜
        top_week, top_month = topic_services.get_top_active_user_topic()

        self.title = '最火的结婚交流社区-网友互助爆料!'
        self.keywords = '结婚求互'
        self.description = ''
        #url= 'new_topic_detail.html
        self.echo('view/qa/new_topic_detail.html',{
            'topic':topic,
            'nick_name':user.Fnick_name,
            'topic_images':lst_topic_images,
            'topic_cate': topic_cate,
            'user_photo':user.Fphoto_url,
            'reply_list':lst_reply,
            'total_page':page_data.page_num,
            'hot_topic': hot_topic,
            'top_week': top_week,
            'top_month': top_month,
            'user_db': UserMsgCache(self.db),
            'cur_type': 'topic',
            'time_passed': time_passed,
        })

    def post(self, *args, **kwargs):
        #生成二维码
        rsp = {}
        url = self.request.full_url()
        import qrcode
        q=qrcode.main.QRCode()
        q.add_data(url)
        q.make(fit=True)
        img = q.make_image()
        output = StringIO.StringIO()
        img.save(output)
        img_data = output.getvalue()
        output.close()

        rsp['stat'] = 'ok'
        rsp['data'] = base64.b64encode(img_data)

class TopicCreateHandler(BaseHandler):#创建话题操作

    @tornado.web.authenticated
    def get(self,category_id=None):
        topic_services.set_db(self.db)
        topic_cate = []
        topic_categorys = topic_services.query_topic_category()
        for topic_category in topic_categorys:
            cate_info = {'id':topic_category.Fid,'name':topic_category.Fname,
                            'url':topic_category.Fimg_url+'@200h.jpg' if topic_category.Fimg_url else _TOPIC_CATEGORY_DEFAULT_URL,
                            'desc':topic_category.Fdescription,'topic_count':topic_category.Ftopic_count,
                            'page_view':self.get_page_view('t_topic_category',topic_category.Fid,topic_category.Fpage_view)}
            topic_cate.append(cate_info)

        self.echo('view/qa/topic_public.html', {
            'topic_cate': topic_cate,
            'cur_type': 'topic',
        })

    @tornado.web.authenticated
    def post(self,category_id=0):
        self.get_paras_dict()
        body = self.qdict
        title_len = len(re.sub(r'<img src="/static/skin/js/plug/face/\d+.gif" border="0">', '1', body.get('title', '').decode('utf-8')))

        print 'title_len',len(body.get('title',''))

        if  not title_len or not body.get('content'):
            return self.write_json({'stat':'err','msg':'标题和内容不能为空'})
        if title_len > 25 or title_len < 2:
            return self.write_json({'stat':'err','msg':'标题在2-25个字符之间'})

        user_id = self.get_current_user().get('Fid')
        body['user_id'] = user_id
        body['category_id'] = category_id
        topic_services.set_db(self.db)
        try:
            imgs = [x for x in ujson.loads(self.get_argument('img', '[]')) if x ]
            body['total_img'] = len(imgs)
            topic = topic_services.create_topic(**body)
            for img in imgs:
                topic_services.create_topic_img(topic.Fid,user_id,img['url'].split('@')[0],'topic',img['size'],img['id'])
        except Exception,e:
            pass
            return self.write_json({'stat':'err','msg':'exception:'+e.message})
        self.write_json({'stat':'ok','msg':'','topic_id':topic.Fid, 'topic_user_id': topic.Fuser_id})

class TopicEditHandler(BaseHandler):#创建话题操作

    @tornado.web.authenticated
    def get(self,topic_id=None):
        topic_services.set_db(self.db)
        topic = topic_services.get_topic_by_id(topic_id, self.current_user['Fid'])
        if not topic:
            return self.redirect('/404')
        topic_images = topic_services.get_topic_images_list(topic_id, self.current_user['Fid'])
        lst_topic_images = []
        for topic_image in topic_images:
            lst_topic_images.append({'url':topic_image.Fimg_url, 'img_size': topic_image.Fimg_size,'img_id':topic_image.Fimg_id})

        topic_cate = []
        topic_categorys = topic_services.query_topic_category()
        for topic_category in topic_categorys:
            cate_info = {'id':topic_category.Fid,'name':topic_category.Fname,
                            'url':topic_category.Fimg_url+'@200h.jpg' if topic_category.Fimg_url else _TOPIC_CATEGORY_DEFAULT_URL,
                            'desc':topic_category.Fdescription,'topic_count':topic_category.Ftopic_count,
                            'page_view':self.get_page_view('t_topic_category',topic_category.Fid,topic_category.Fpage_view)}
            topic_cate.append(cate_info)

        self.echo('view/qa/topic_edit.html', {
            'topic_cate': topic_cate,
            'cur_type': 'topic',
            'topic': topic,
            'topic_image': lst_topic_images,
        })

    @tornado.web.authenticated
    def post(self,topic_id=0):
        self.get_paras_dict()
        body = self.qdict
        user_id = self.get_current_user().get('Fid')
        body['user_id'] = user_id
        topic_services.set_db(self.db)
        topic = topic_services.get_topic_by_id(topic_id, user_id)
        if not topic:
            return self.write_json({'stat': 'err', 'msg': '非法请求'})
        try:
            imgs = [x for x in ujson.loads(self.get_argument('img', '[]')) if x ]
            kwargs = {
                'Fcotegory_id': topic.Fcotegory_id,
                'Ftitle': topic.Ftitle,
                'Fcontent': re.sub(r'\n', '<br/>', body.get('content', '')),
                'Fedit_times': topic.Fedit_times + 1,
                'Fmodify_time': yyyydddddatetime(),
                'Flast_edit_time': yyyydddddatetime(),
                }
            topic_services.update_topic(topic_id,**kwargs)
            topic_services.delete_topic_img(topic.Fid,user_id)
            for img in imgs:
                topic_services.update_topic_img(topic.Fid,user_id,img['url'].split('@')[0],'topic',img['size'],img['id'])
        except Exception,e:
            self.log_exception(*sys.exc_info())
            pass
            return self.write_json({'stat':'err','msg':'exception:'+e.message})
        self.write_json({'stat':'ok','msg':'','topic_id':topic.Fid, 'topic_user_id': topic.Fuser_id})


class TopicReplyCreateHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,topic_id,parent_id):
        pass

    @tornado.web.authenticated
    def post(self,topic_id,parent_id=0):
        parent_id = int(parent_id)
        user_id = self.get_current_user().get('Fid')
        self.get_paras_dict()
        body = self.qdict
        topic_services.set_db(self.db)
        if not body.get('content'):
            return self.write_json({'stat':'err','msg':'内容不能为空'})
        if parent_id:
            body['parent_id'] = parent_id
            parent_reply = topic_services.get_topic_reply(parent_id) #父级帖子
            body['Fparent_user_id'] = parent_reply.Fuser_id
        else:
            body['Fparent_user_id'] = topic_services.query_topics_all(topic_id=topic_id).scalar().Fuser_id
        try:
            body['topic_id'] = topic_id
            body['user_id'] = user_id
            topic_reply = topic_services.create_topic_reply(**body)
            data = {}
            if topic_reply.Fparent_id:
                data['Ffull_parent_id'] = str(parent_reply.Ffull_parent_id)+'/'+str(topic_reply.Fid)
            else:
                data['Ffull_parent_id'] = '/'+str(topic_reply.Fid)

            topic_services.update_topic_reply(topic_reply.Fid,**data)
            self.set_reply_count('t_topics',topic_reply.Fid)

            imgs = [x for x in ujson.loads(self.get_argument('img', '[]')) if x ]
            for img in imgs:
                topic_services.create_topic_img(topic_reply.Fid, user_id, img['url'].split('@')[0],'reply',img['size'])

            user_db = UserMsgCache(self.db)

            #调用celery, 创建评论的消息
            msg_link = self.request.headers.get('Referer') + '#%s' % topic_reply.Fid
            msg_data = {
                'text_type': 'private',
                'info_type': 1,
                'sender_id': user_id,  #发送者id
                'receiver_id': body['Fparent_user_id'], #接受者id  可以为list
                'title': '结婚社区', #消息标题
                'link': msg_link , #消息链接
                'data': '%s 评论了您: %s' % (user_db.get_user_msg(user_id).get('Fnick_name'),body['content'])  #消息内容
            }
            create_user_message.apply_async(kwargs=msg_data)

            #返回回复所需信息
            reply_list = []
            user_reply = user_db.get_user_msg(topic_reply.Fuser_id)

            reply_info = {

                    'user_id': topic_reply.Fuser_id,
                    'nick_name':user_reply.get('Fnick_name'),
                    'head_url':user_reply.get('Fphoto_url'),
                    'content':topic_reply.Fcontent,
                    'index': topic_services.query_topic_reply(topic_id= topic_id,parent_id=0).count() if not parent_id else 0,
                    'Fpraise':topic_reply.Fpraise,
                    'images':[{'img':x['url'].split('@')[0]} for x in imgs],
                    'time':time_passed(topic_reply.Fcreate_time),
                    'reply_id':topic_reply.Fid,
                    'parent_user_id': body['Fparent_user_id'],
                    'parent_nick_name': user_db.get_user_msg(body['Fparent_user_id']).get('Fnick_name'),
                    'has_child': False,
                    'has_parent': False if not parent_id or not parent_reply.Fparent_id else True,
                }
            reply_list.append(reply_info)

        except Exception,e:
            self.log_exception(*sys.exc_info())
            pass
            return self.write_json({'stat':'err','msg':'exception:'+ ''})
        self.write_json({'stat':'ok','topic_reply_id':topic_reply.Fid, 'reply_list': reply_list})

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


class TopicReplyQueryHandler(BaseHandler):#查询回复

    #@login_control()
    def get(self,topic_id,user_id):
        topic_services.set_db(self.db)
        try:
            order = ' Fcreate_time desc' if self.get_argument('new', '') else ' Fcreate_time asc'
            topic_replys = topic_services.get_topic_reply_list(topic_id, order_by=order)
            page_data = self.get_page_data(topic_replys, PAGE_SIZE)

            lst_reply = []
            # parent_reply = ''
            user_db = UserMsgCache(self.db)
            index = (int(self.get_argument('page', 1)) - 1) * PAGE_SIZE
            for reply in page_data.result:
                index += 1
                user_reply = user_db.get_user_msg(reply.Fuser_id)
                images = topic_services.get_reply_images_list(reply.Fid,reply.Fuser_id) #回复照片
                # lst_images = [{'img':self.img_compression(image.Fimg_url,image.Fimg_size)} for image in images]
                lst_images = [{'img':image.Fimg_url} for image in images]
                reply_info = {
                    'Fuser_id': reply.Fuser_id,
                    'nick_name':user_reply.get('Fnick_name'),
                    'head_url':user_reply.get('Fphoto_url'),
                    'content':reply.Fcontent,
                    'index': index,
                    'Fpraise':reply.Fpraise,
                    'images':lst_images,
                    'time':time_passed(reply.Fcreate_time),
                    'reply_id':reply.Fid,
                    'vote_judge':1 if not self.current_user else 0 if get_topic_user_sns(self.db,self.current_user['Fid'],reply.Fid,2 ) else 1,
                    'parent': '',
                }

                total_count, reply_list = topic_services.get_reply_of_reply(reply.Fid)
                tmp_replses=[]
                for r in reply_list:
                    parent_user_id = r.Fparent_user_id
                    tmp_replses.append({
                        'reply_id':r.Fid,
                        'nick_name':user_db.get_user_msg(r.Fuser_id,).get('Fnick_name'),
                        'user_id':r.Fuser_id,
                        'content':r.Fcontent,
                        'has_parent': True if parent_user_id and parent_user_id != reply.Fuser_id else False,
                        'parent_user_id': parent_user_id if parent_user_id and parent_user_id != reply.Fuser_id else '',
                        'parent_nick_name': user_db.get_user_msg(parent_user_id).get('Fnick_name') if parent_user_id and parent_user_id != reply.Fuser_id else '',
                        'time': time_passed(r.Fcreate_time)
                    })

                reply_info['has_child'] = True if total_count>0 else False

                reply_info['replies']={
                        'total_count':total_count,
                        'replies':tmp_replses
                }

                lst_reply.append(reply_info)

        except Exception,e:
            pass
            return self.write_json({'stat':'err','msg':'exception:'+e.message})
        self.write_json({'stat':'ok','msg':'','reply_list':lst_reply, 'total_page': page_data.page_num, 'cur_page': self.get_argument('page', 1)})

    def post(self,topic_id,user_id):
        pass


class TopicDeleteHandler(BaseHandler):#删除话题

    @tornado.web.authenticated
    def get(self,topic_id):
        topic_services.set_db(self.db)
        try:
            data = {}
            data['Fdeleted'] = 1
            topic_services.update_topic(topic_id,**data)
        except Exception,e:
            pass
            return self.write_json({'stat':'PAGE_SIZE01','msg':'exception:'+e.message})
        self.write_json({'stat':'PAGE_SIZE00','msg':''})


class TopicSnsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,topic_id,sns_type,topic_type,db_operation):
        '''
        :param topic_id: 话题id或者话题回复id
        :param sns_type: 收藏还是点赞 (点赞1,2)
        :param topic_type: 话题or回复 (1,2)
        :param db_operation:删除还是新增 取消0,点赞1
        :return:
        '''
        try:
            if int(sns_type) not in (1,2) or int(topic_type) not in (1,2) or int(db_operation) not in (0,1):
                raise SiteError('参数类型不正确')
            topic_services.set_db(self.db)
            user_id = self.get_current_user().get('Fid')
            res = topic_services.create_topic_sns(topic_id,user_id,int(sns_type),int(topic_type),operation=int(db_operation))
            data={'stat':'ok','msg':'操作成功'} if res else {'stat':'err','msg':'操作非法'}
            if res:
                topic_sns_db = TopicUserSnsCache(self.db)
                topic_sns_db.refresh_user_sns_msg(self.current_user['Fid'])
        except Exception,e:
            pass
            data={'stat':'err','msg':'exception:'+e.message}
        self.write_json(data)

class TopicReplyMoreHandler(BaseHandler):
    def get(self, reply_id):
        topic_services.set_db(self.db)
        user_db = UserMsgCache(self.db)
        reply = topic_services.get_topic_reply(reply_id)
        total_count, reply_list = topic_services.get_reply_of_reply(reply.Fid)
        tmp_replses=[]
        for r in reply_list.offset(5):
            parent_user_id = r.Fparent_user_id
            tmp_replses.append({
                'reply_id':r.Fid,
                'nick_name':user_db.get_user_msg(r.Fuser_id,).get('Fnick_name'),
                'user_id':r.Fuser_id,
                'content':r.Fcontent,
                'has_parent': True if parent_user_id != reply.Fuser_id else False,
                'parent_user_id': parent_user_id if parent_user_id != reply.Fuser_id else '',
                'parent_nick_name': user_db.get_user_msg(parent_user_id).get('Fnick_name') if parent_user_id != reply.Fuser_id else '',
                'time': time_passed(r.Fcreate_time)
            })
        self.write_json({'stat': 'ok', 'reply_list': tmp_replses})


def get_topic_user_sns(db, user_id, topic_id,topic_type, sns_type = 1):
    '''
    db 数据库
    user_id
    topic_id 话题或回复的id
    topic_type  1话题 2回复
    sns_type 1点赞
    '''
    topic_sns_db = TopicUserSnsCache(db)
    sns_dict = topic_sns_db.get_user_sns_msg(user_id)
    key = '%s_%s_%s' % (topic_id, sns_type, topic_type)
    return sns_dict.get(key)