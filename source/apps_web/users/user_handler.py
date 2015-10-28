#encoding:utf-8
__author__ = 'binpo'

from common.base import BaseApiHandler
from common.cache_base import WebCacheHandler
from services.users.user_services import UserServices
from services.orders.order_services import OrderServices
from services.shares.shares_service import ShareServices
from services.ablums.photos_service import PhotosServices
from services.topics.topic_services import TopicServices
from services.message.message_service import MessageService
from utils.upload_utile import upload_to_oss,upload_resize
from tornado.options import options
from common.permission_control import login_control
from utils.message.sms import send_phone_msg
from utils.random_utils import create_random_passwd
from conf.msg_conf import PHONE_REG_TEMPLATE,PHONE_LOGIN_TEMPLATE,CHECK_CODE_TEMPLATE
from common.base import SiteError
from utils.regular import Regular
import ujson
import sys
from models.user_do import Users
from models.topic_do import Topics,TopicReply
from datacache.datacache import UserMsgCache
from conf.work_conf import PAGE_SIZE
user_service = UserServices()
order_service = OrderServices()
share_service = ShareServices()
photo_service = PhotosServices()
topic_service = TopicServices()
message_service = MessageService()

class UserIndex(BaseApiHandler):

    def get(self, *args, **kwargs):
        # topic_service.set_db(self.db)
        # topic_service.query_user_topics(self.get_current_user().get('Fid'))
        # topic_service.get_user_replies(self.get_current_user().get('Fid'))
        message_service.set_db(self.db)
        message_service.query_messages()
        self.echo('views/account/index.html',{})


class UserHandler(BaseApiHandler,WebCacheHandler):

    @login_control()
    def get(self, *args, **kwargs):
        user_id = self.get_current_user().get('Fid')
        user_service.set_db(self.db)
        user = user_service.get_user_by_id(user_id)
        data = self.obj_to_dict(user,['Fid','Fnick_name','Fuser_name','Fsex','Fsign_text','Fphoto_url','Fuser_mobi',
                                      'Frole_codes','is_employee'])
        self.write_json(data)

    def options(self, *args, **kwargs):
        return self.write('')

    def reset_cookies(self,user):
        cookies = user_service.user_format(user)
        data = self.child_account_key(user)
        if data:
            cookies.update(data)
        self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=10)

    def put(self, *args, **kwargs):
        '''
        :手机注册账号
        :param args:
        :param kwargs:
        :return:
        '''
        self.get_paras_dict()
        phone = self.qdict.get('phone')
        code = self.qdict.get('code')
        password = self.qdict.get('password')
        user_service.set_db(self.db)
        try:
            for key in ['phone','code']:
                if not self.qdict.get(key):
                    raise SiteError('参数错误')
            cache_code = self.mcache.get(str(self.qdict.get('phone'))+'_code')
            if str(cache_code)==code.strip():
                user = user_service.create_user_by_phone(phone,password=password)
                cookies = user_service.user_format(user)
                open_id = self.get_secure_cookie('wx_login_open_id')
                nick = self.get_secure_cookie('nick')
                photo = self.get_secure_cookie('photo')
                data = self.child_account_key(user)
                if open_id:
                    user.Fweixin=open_id
                if nick and not user.Fnick_name:
                    user.Fnick_name = nick
                if photo and (user.Fphoto_url=='/static/common/images.png' or not user.Fphoto_url):
                    user.Fphoto_url = photo
                if data:
                    cookies.update(data)
                if not user.Fnick_name:
                    user.Fnick_name='公主号_'+create_random_passwd(3)
                self.set_secure_cookie('loginuser',ujson.dumps(cookies),expires_days=10)
                self.db.add(user)
                self.db.commit()
                # url = self.get_cookie('login_regrdiect_url')

                cookies = user_service.user_format(user)
                self.set_secure_cookie('loginuser', ujson.dumps(cookies),expires_days=10)
                data = {'code':200,'data':{'user':cookies},'info':"用户登录成功"}

                #data={'stat':200,'info':'验证通过并登陆','data':{}}
            else:
                data={'stat':'1004','info':'验证码错误'}
        except Exception,e:
            pass
            data={'stat':'1005','info':'程序异常,异常原因是'+e.message}
        self.write_json(data)

    @login_control()
    def post(self, *args, **kwargs):

        self.user_id = self.get_current_user().get('Fid')
        #测试修改
        self.get_paras_dict()
        user_service.set_db(self.db)
        if self.request.files.get('head_photo'): #图片上传
            return self.upload_photo()
        elif self.qdict.has_key('getBounds[]'):#剪切
            return self.head_img_cut()
        elif self.qdict.has_key('passwd'):#修改密码
            return self.modify_passwd()
        elif self.qdict.has_key('phone'):#修改手机号码
            return self.bind_phone()
        elif self.qdict.get('nick',''):
            if not self.qdict.get('nick'):
                return self.write_json({'stat':'1006','info':'昵称不能为空'})
            try:
                from utils.unicode_check import is_chinese
                if is_chinese(self.qdict.get('nick')):
                    if len(self.qdict.get('nick'))>36:
                        return self.write_json({'stat':'1006','info':'昵称最长不能超过12个字'})
                else:
                    if len(str(self.qdict.get('nick').encode('utf-8')))>12:
                        return self.write_json({'stat':'1006','info':'昵称最长不能超过12个字'})
                user_service.update_user(self.user_id,
                                         Fnick_name=self.qdict.get('nick'),
                                         Frealname=self.qdict.get('realname'),
                                         Fsex=self.qdict.get('sex',''),
                                         Fsign_text=self.qdict.get('sign','')
                                         )
                self.delete_user_info(str(self.user_id))
                self.reset_cookies(self.db.query(Users).filter(Users.Fid==self.user_id).scalar())
            except Exception,e:
                pass
                return self.write_json({'stat':'1005','info':'exception:'+e.message})
            self.write_json({'stat':'1000','info':'用户信息更新成功'})
        else:
            self.write_json({'stat':'1006','data':{},'info':'请求不存在,'})

    def modify_passwd(self):
        '''
        todo 修改密码
        :return:
        '''
        #pre_passwd = self.qdict.get('pre_passwd')
        passwd = self.qdict.get('passwd')
        confirm_pwd = self.qdict.get('confirm_pwd')
        if len([key for key in ['passwd','confirm_pwd'] if key in self.qdict.keys()]) < 3:
            return self.write_json({'stat':'1003','data':{},'info':'参数不全'})
        if not passwd or not confirm_pwd:
            return self.write_json({'stat':'1004','info':'密码不能为空'})
        if len(passwd) <6 or len(confirm_pwd) < 6:
            return self.write_json({'stat':'1004','info':'密码长度不能小于6位'})
        if passwd != confirm_pwd:
            return self.write_json({'stat':'1004','info':'新密码两次输入不相同'})
        else:
            user_service.set_db(self.db)
            user = user_service.get_user_by_id(self.user_id)
            #if user.Fuser_pwd == user_service.user_passed(pre_passwd,user.Fuid):
            user_service.reset_passwd(user.Fid,passwd,user)
            return self.write_json({'stat':'1000','data':{},'info':'密码修改成功'})
            # else:
            #     return self.write_json({'stat':'1004','data':{},'info':'原始密码错误'})

    def bind_phone(self):
        '''
        :绑定电话号码
        :return:
        '''
        phone = self.qdict.get('phone')
        code = self.qdict.get('code')
        if len([key for key in ['phone','code'] if key in self.qdict.keys()])<2:
            return self.write_json({'stat':'1003','data':{},'info':'参数不全'})
        if not Regular.check_phone(phone):
            return self.write_json({'stat':'1004','data':{},'info':'手机格式错误'})
        if not self.mcache.get(str(phone)+'_code') or code!=self.mcache.get(str(phone)+'_code'):
            return self.write_json({'stat':'1004','data':{},'info':'验证码错误'})
        user = user_service.get_user_by_phone(phone)
        if user.Fid == self.user_id:
            user.Fuser_mobi = phone
            self.db.add(user)
            self.db.commit()
            return self.write_json({'stat':'1000','info':'电话绑定成功'})
        else:
            return self.write_json({'stat':'1004','info':'电话已绑定其他账号'})

    def head_img_cut(self):
        '''
        头像图片裁剪
        :return:
        '''
        file_prex = '/'.join([str(self.user_id),'head_photo'])
        # bounds = self.qdict.get('bounds').split(',')

        is_ok,filenames = upload_resize(self,options.IMG_BUCKET,self.qdict.get('url'),file_prex=file_prex,
                                   sf_w=self.qdict.get('getBounds[]')[0],
                                   sf_h=self.qdict.get('getBounds[]')[1],
                                   x=self.qdict.get('jcrop[x]'),
                                   y=self.qdict.get('jcrop[y]'),
                                   x1=self.qdict.get('jcrop[x2]'),
                                   y1=self.qdict.get('jcrop[y2]'))

        # is_ok,filenames = upload_resize(self,options.IMG_BUCKET,self.qdict.get('url'),file_prex=file_prex,
        #                                    sf_w=bounds[0],
        #                                    sf_h=bounds[1],
        #                                    x=self.qdict.get('x'),
        #                                    y=self.qdict.get('y'),
        #                                    x1=self.qdict.get('x1'),
        #                                    y1=self.qdict.get('y1'))
        if is_ok:
            user_service.set_db(self.db)
            user = user_service.get_user_by_id(self.user_id)
            url = ''
            for f in filenames:
                url = user.Fphoto_url = options.IMG_DOMAIN+'/'+f.get('full_name')
                self.db.add(user)
                self.db.commit()
                break
            self.reset_cookies(self.db.query(Users).filter(Users.Fid==self.user_id).scalar())
            self.delete_user_info(str(self.user_id))
            UserMsgCache(self.db).refresh_user_msg(str(self.user_id))
            return self.write_json({'stat':'1000','data':{'head_url_thumb':url},'info':'头像设置成功'})
        else:
            return self.write_json({'stat':'1001','info':'头像设置成功'})

    def upload_photo(self):
        '''
        :上传头像图片
        :return:
        '''
        user_id = 1#self.get_current_user().get('Fid')
        head_url = ''
        try:
            file_prefix = '/'.join([str(user_id),'head_photo'])
            is_ok, filenames = upload_to_oss(self, options.IMG_BUCKET,file_prex=file_prefix,param_name='head_photo',file_type='img')
            if is_ok:
                for file in filenames:
                    head_url = options.IMG_DOMAIN+'/'+file.get('full_name')
                    data = {}
                    #data['Fphoto_url'] = head_url
                    #user_service.update_user(user_id,**data)
                    #self.delete_user_info(str(user_id))
                    break
            else:
                return self.write_json({'stat':'1005','data':{},'info':'图片上传失败'})
        except Exception,e:
            pass
            return self.write_json({'stat':'1001','info':'exception:'+e.message})
        self.write_json({'stat':'1000','data':{'head_url':head_url},'info':'头像设置成功'})

class PhoneCodeHandler(BaseApiHandler):

    def get(self,phone,code_type,**kwargs):
        # phone = self.get_argument('phone')
        '''
        :发送手机验证码
        :param phone:
        :param code_type:   _reg:注册(登陆)验证码
        :param kwargs:
        :return:
        '''
        if not phone or not code_type:
            data={'stat':'1001','info':'请求参数错误'}
        else:
            if not Regular.check_phone(phone):
                data={'stat':'1001','info':'手机格式不正确'}
            else:
                cache_key = str(phone)+str(code_type)
                code = create_random_passwd(2)
                if self.mcache.get(cache_key):
                    self.mcache.set(cache_key,self.mcache.get(cache_key),180)
                    data={'stat':'1000','info':'操作成功'}
                else:
                    is_ok = self.mcache.set(cache_key,str(code),180)
                    if code_type=='_reg':
                        content=PHONE_REG_TEMPLATE%(code)
                    elif code_type=='_login':
                        content=PHONE_LOGIN_TEMPLATE%(code)
                    else:content=CHECK_CODE_TEMPLATE%(code)
                    if is_ok:
                        send_phone_msg(str(phone),content)
                        data={'stat':'1000','info':'发送成功'}
                    else:
                        data={'stat':'1001','info':'memcache存储验证码失败'}
        self.write_json(data)

class UserTopicHandler(BaseApiHandler,WebCacheHandler):

    @login_control()
    def get(self,page=1):
        '''
        todo:用户发表的话题
        :param page:页码
        :param kwargs:
        :return:
        '''
        topic_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        user = self.get_user_info(str(user_id))
        lst_topics = []

        if not int(page) or int(page) <= 1:
            page = 1
        #topics_nte = topic_service.query_topics(is_top=0,is_essence=0,user_id=user_id) #非加精置顶
        topics = topic_service.query_user_topics(user_id)
        try:
            page_topics = self.get_page_data(topics,page_size=PAGE_SIZE,page=page)
            self.topic_data_format(page_topics.result,lst_topics)
        except Exception,e:
            pass
            return self.write_json({'stat':'1005','data':{},'info':'exception:'+e.message})
        self.write_json({
                        'code':200,
                        'data':
                              {'topics':lst_topics,
                               'nick_name':user.get('nick_name'),
                               'head_url':user.get('photo_url'),
                               'total_page':page_topics.page_num,
                               'is_page':self.is_page(page_topics.page_num,page)
                              },
                        'info':''
                        })


    def topic_data_format(self,topics,lst):
        '''
        :todo 话题数据格式化
        :param topics:
        :param lst:
        :return:
        '''
        for topic in topics:
            #user = self.get_user_info(str(topic.Fuser_id))
            images = self.get_topic_img(topic.Fid,'topic')
            data = self.obj_to_dict(topic,['Fid','Ftitle','Fcontent','Fcreate_time'])
            data.update({'lst_img':images})
            lst.append(data)

class UserTopicsReplyHandler(BaseApiHandler):

    @login_control()
    def get(self,page=1):
        topic_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        user = self.get_user_info(str(user_id))
        try:
            if not int(page) or int(page) <= 1:
                page = 1
        except:
            page=1
        replies = topic_service.get_user_replies(user_id)
        lst_reply=[]
        try:
            _replies = self.get_page_data(replies,page_size=PAGE_SIZE,page=page)
            self.reply_data_format(_replies.result,lst_reply)
        except Exception,e:
            pass
            return self.write_json({'stat':'1005','data':{},'info':'exception:'+e.message})
        self.write_json({
                        'code':200,
                        'data':
                              {'replies':lst_reply,
                               'nick_name':user.get('nick_name'),
                               'head_url':user.get('photo_url'),
                               'total_page':_replies.page_num,
                               'is_page':self.is_page(_replies.page_num,page)
                              },
                        'info':''
                        })

    def reply_data_format(self,_replies,_rlist):
        for reply in _replies:
            data=self.obj_to_dict(reply,['Fid','Ftitle','Fcontent','Fcreate_time'])
            images = self.get_topic_img(reply.Fid,'reply')
            data.update({'lst_img':images})
            _rlist.append(data)

class UserSnsHandler(BaseApiHandler,WebCacheHandler):

    @login_control()
    def get(self,page):
        if not page or int(page) <= 1:
            page = 1
        user_id = self.get_current_user().get('Fid')
        user = self.get_user_info(user_id)
        lst_topics = []
        try:
            lst_topics_id = self.get_sns_topics_info(user_id,2)
            for topic_id in lst_topics_id:
                lst_topics.append(self.get_topics_info(topic_id,'topic_'))
            topics = self.get_page_list(lst_topics,page_size=2,page=page)
        except Exception,e:
            pass
            return self.write_json({'code':'1005','info':'exception:'+e.message,'data':{}})
        self.write_json({
                        'code':'1000',
                        'info':'',
                        'data':
                              {'topics':topics,
                               'nick_name':user.get('nick_name'),
                               'hear_url':user.get('photo_url'),
                               'is_page':self.is_page(self.get_total_page(lst_topics,page_size=2),page)
                              }
                        })

class UserMessageHandler(BaseApiHandler):

    @login_control()
    def get(self,msg_type='private',page=0, **kwargs):
        message_service.set_db(self.db)
        user_id = self.get_current_user().get('Fid')
        try:
            if not int(page) or int(page) <= 1:
                page = 1
        except:
            page=1
        query = message_service.query_messages(user_id)
        # messages = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
        # message = []
        # for m in messages.result:
        #     message.append({'content':m[4],'id':m[0],'is_read':m[14],'is_pending':m[15]})
        #
        # self.write_json({'code':200,''})

import tornado

class UserInfoHandler(BaseApiHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_service.set_db(self.db)
        user = user_service.get_user_by_id(self.current_user.get('Fid'))
        self.echo('view/account/index.html',{'user':user},layout='')


class UserNotifyHandler(BaseApiHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.echo('view/account/notice/index.html',layout='')


class UserTopicsHandler(BaseApiHandler):

    @tornado.web.authenticated
    def get(self,page=0, **kwargs):

        user_id = self.get_current_user().get('Fid')
        topic_service.set_db(self.db)
        user_topics = topic_service.query_user_topics(user_id)
        data = self.get_page_data(user_topics,page_size=PAGE_SIZE,page=page)
        self.echo('view/account/group/index.html',{'topics':data},layout='')

    def get_images_of_topic(self,topic_id):
        '''
        :获取话题图片
        :param topic_id:
        :return:
        '''
        images = topic_service.get_imgaes_by_topic_id(topic_id)
        if images.count>0:
            return images.limit(5).offset(0)
        else:
            return []

class UserTopicsReplyHandler(BaseApiHandler):

    @tornado.web.authenticated
    def get(self,page=0, **kwargs):

        user_id = self.get_current_user().get('Fid')
        topic_service.set_db(self.db)
        user_topics = topic_service.get_user_replies(user_id)
        data = self.get_page_data(user_topics,page_size=PAGE_SIZE,page=page)
        self.echo('view/account/group/reply.html',{'topics':data},layout='')

    def get_topic_title_and_parent_content(self,topic_id,parent_id):
        '''
        :根据topic name 和parentname
        :param topic_id:
        :return:
        '''
        topic_title = self.db.query(Topics.Ftitle).filter(Topics.Fid==topic_id).scalar()
        if parent_id:
            parent_content = self.db.query(TopicReply.Fcontent).filter(TopicReply.Fid==parent_id).scalar()
        else:parent_content =''
        return topic_title,parent_content


from models.order_do import *
from models.company_do import *
from models.product_do import ShotPackage,WeddingPhotoProduct

class UserOrdersHandler(BaseApiHandler):

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        user_id = self.get_current_user().get('Fid')
        orders = self.db.query(BespeakOrders).filter(BespeakOrders.Fuser_id==user_id).order_by('Fcreate_time desc')
        self.echo('view/account/list/index.html',{'orders':orders},layout='')

    def get_name_by_order_id(self,merchant_id,order_type,refer_id):
        '''
        :param order_id:
        :param order_type: #1.商户订单,2.套系订单 3.作品订单
        :param refer_id:
        :return:
        '''

        if order_type==1:
            company = self.db.query(Company).filter(Company.Fuser_id==merchant_id).scalar()
            img = company and company.Fphoto_url or ''
            name = company and company.Fcompany_name or ''
            link = company and '/merchant/detail/'+str(company.Fid) or ''
        elif order_type==2:
            shot_package = self.db.query(ShotPackage).filter(ShotPackage.Fdeleted==0,ShotPackage.Fid==refer_id).scalar()
            if shot_package:
                img,name,link=shot_package.Fcover_img,shot_package.Fpackage_name,'/series/'+str(shot_package.Fid)
            else:img,name,link = '','',''
        elif order_type==3:
            product = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted==0,WeddingPhotoProduct.Fid==refer_id).scalar()
            if product:
                img,name,link=product.Fcover_img,product.Fname,'/product/'+str(product.Fid)
            else:
                img,name,link= '','',''
        return img,name,link
#index.html



























