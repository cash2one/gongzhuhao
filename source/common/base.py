#encoding:utf-8

import timeit
import tornado.web
import ujson
from tornado.options import options
from services.pagination.page import Paginator
import urlparse
import urllib
from services.topics.topic_services import TopicServices
from services.users.user_services import UserServices
from services.work.work_services import WorkServices
from services.series.series_services import SeriesServices
from services.company.company_services import CompanyServices
from services.home.home_service import HomeService
from services.banner.banner_service import BannerService
from models.product_do import WeddingPhotoProduct,ShotPackage
from models.company_do import Company
from tenjin_base import WebTenjinBase,MobileTenjinBase,ViewsTenjinBase
import re
import sys
from common.permission_control import admin_permission_access
from utils.error_util import Error
import math
import datetime

topic_services = TopicServices()
user_service = UserServices()
work_service = WorkServices()
series_servie = SeriesServices()
company_service = CompanyServices()
home_servie = HomeService()
banner_service = BannerService()
stat_time = 0.0

class SiteError(Exception):
    def __init__(self, value):
        self.message = value
    def __str__(self):
        return repr(self.message)

class BaseHandler(WebTenjinBase):

    STATIC_DOMAIN = ''

    @property
    def db(self):
        return self.application.db

    @property
    def mcache(self):
        return self.application.mcache

    @property
    def rcache(self):
        return self.application.rcache

    def echo(self, template, context=None, globals=None,layout='crm/common/base.html'):
        data = self.render(template, context, globals,layout)
        self.write(data)

    def echoQ(self, template, context=None, globals=None, layout=''):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        json = self.get_secure_cookie("loginuser",None)
        info = ujson.loads(json) if json else None
        if info:
            return info
        else:
            return None

    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台

        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX

        global stat_time
        stat_time = timeit.default_timer()
        user_agent = self.request.headers.get('User-Agent')
        print 'userAgent:',user_agent
        # if self.request.method == "GET" and CACHED and \
        #    not self.request.path.startswith("/admin"):
        #
        #     # 尝试获取当前页面的缓存
        #     cache = self.mcache.get(self.request.uri)
        #     # 获取缓存则输出页面,结束请求
        #     if cache:
        #         return self.finish(cache)

    def on_finish(self):
        if self.db:
            self.db.close()
        global stat_time

        # """ 重写结束请求前的方法函数 """
        # if self.request.method == "POST":
        #     # 如果遇到POST提交则清空缓存
        #     self.mcache.flush()

        response_time = 0
        response_time = (timeit.default_timer() - stat_time) % 1000
        if response_time > 0:
            print '---------------------------RT---------------------------------'
            print '-> Current url   : ', self.request.uri
            print '-> Response time : ', response_time, ' s'
            print '--------------------------------------------------------------'

        # self.response_time = response_time

    def get_error_html(self, status_code=500, log_message='', *args, **kwargs):
        pars = {
           'log_message':log_message,
           'args':args,
           'kwargs':kwargs,
           }
        if status_code==400:
            return self.echo('apps_crm/common/404.html')
        return self.echo("apps_crm/common/error.html", **pars)

    def get_page_data(self,query,page_size=None,page=None):
        if not page_size:
            page_size =  int(self.get_argument("page_size",50))
        if not page:
            page = int(self.get_argument("page", 1))
        page = int(page)
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def check_arg(self, name, rgx, default=None):
        val = self.get_argument(name) if default==None else self.get_argument(name, default)
        if val == default:
            return default
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return val
        else:
            raise Error('2000', name, "参数错误")

    def check_arg_2(self,name,rgx):
        val = self.get_argument(name)
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return True,''
        else:
            return False,name+'参数错误'

    def get_view_count(self,table_name,object_id,current_db_count_views=0):
        '''
        获取object 浏览量
        :param table_name:
        :param object_id:
        :param current_db_count_views:
        :return:
        '''
        result_counts=0
        try:
            view_count = self.rcache.hget(str(table_name),int(object_id))
            print 'view_count:',view_count
            if current_db_count_views and view_count:
                result_counts = current_db_count_views+view_count
            elif current_db_count_views and not view_count:
                result_counts = current_db_count_views
            elif not view_count and not current_db_count_views:
                count_sql = 'select Fpage_view from {0} where Fid={1}'
                results = self.db.execute(count_sql.format(table_name,int(object_id))).scalar()
                result_counts = results
        except Exception,e:
            print e.message
            pass
            # self.rcache.hset(table_name+'_v',object_id,1)
            view_count=1
        if not view_count or view_count=='None':
            result_counts=1
        return result_counts

    def get_page_view(self,table_name,object_id,current_db_count_views=0):
        '''
        获取object 浏览量
        :param table_name:
        :param object_id:
        :param current_db_count_views:
        :return:
        '''
        result_counts = 1
        try:

            view_count = self.rcache.hget(str(table_name),object_id)
            result_counts = int(0 if not view_count else view_count) + int(current_db_count_views)

        except Exception,e:
            pass
        return result_counts

    def _handle_request_exception(self, e):
        try:
            if self._finished:
                # Extra errors after the request has been finished should
                # be logged, but there is no reason to continue to try and
                # send a response.
                return
            self.log_exception(*sys.exc_info())

            try:
                self.db.close()
            except:
                pass
            # return self.redirect('/404')

            pass
            self.echo('crm/500.html',layout='')
            self.finish()
        except:
            self.send_error(500, exc_info= sys.exc_info())

    def update_company_price(self,merchant_id):
        '''
        :todo 更新店铺最小和最大价格
        :param merchant_id:
        :param price:
        :return:
        '''

        company = self.db.query(Company).filter(Company.Fuser_id==merchant_id).scalar()

        query_work = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted == 0,WeddingPhotoProduct.Fmerchant_id == merchant_id)
        query_series = self.db.query(ShotPackage).filter(ShotPackage.Fdeleted == 0,ShotPackage.Fmerchant_id == merchant_id)

        lst_sale_price = []
        for obj in query_work.all()+query_series.all():
            lst_sale_price.append(obj.Fsale_price)

        if len(lst_sale_price) == 0:
            company.Fcheapest = 0
            company.Fmost_expensive = 0
        else:
            company.Fcheapest = min(lst_sale_price)
            company.Fmost_expensive = max(lst_sale_price)
        self.db.add(company)
        self.db.commit()

    def delete_product_count(self,merchant_id):
        '''
        todo:删除商户作品数量
        :param merchant_id:
        :return:
        '''
        my_key = 'product_count_'+str(merchant_id)
        count = self.mcache.get(my_key)
        if count:
            self.mcache.delete(my_key)

    def delete_package_count(self,merchant_id):
        '''
        todo:删除套系数量
        :param merchant_id:
        :return:
        '''
        my_key = 'package_count_'+str(merchant_id)
        count = self.mcache.get(my_key)
        if count:
            self.mcache.delete(my_key)

    def delete_essence(self):
        '''
        todo:
        :return:
        '''
        lst_series = self.mcache.get('essence_series')
        lst_series_group = self.mcache.get('essence_group')
        if lst_series:
            self.mcache.delete('essence_series')
        if lst_series_group:
            self.mcache.delete('essence_group')


class AdminBaseHandler(WebTenjinBase):

    STATIC_DOMAIN = ''
    CDN_DOMAIN=''

    # fenxiaolog=FenXiaoLogger()
    # logger = fenxiaolog.getLogger()

    @property
    def db(self):
        return self.application.db

    @property
    def mcache(self):
        return self.application.mcache

    @property
    def rcache(self):
        return self.application.rcache

    def echo(self, template, context=None, globals=None, layout='ops/base.html'):
        self.write(self.render(template, context, globals, layout))

    def get_current_user(self):
        json = self.get_secure_cookie("loginuser",None)
        info = ujson.loads(json) if json else None
        if info:
            return info
        else:
            return None

    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])

    stat_time = 0.0

    @tornado.web.authenticated
    @admin_permission_access()
    def prepare(self):
        self.STATIC_FILE_DOMAIN = options.STATIC_FILE_DOMAIN
        self.IMG_DOMAIN='http://image.python-libs.com'
        global stat_time
        stat_time = timeit.default_timer()

    def on_finish(self):
        if self.db:
            self.db.close()
        global stat_time
        response_time = 0
        if not stat_time:
            stat_time = timeit.default_timer()
        response_time = (timeit.default_timer() - stat_time) % 1000
        if response_time > 0:
            print '---------------------------RT---------------------------------'
            print '-> Current url   : ', self.request.uri
            print '-> Response time : ', response_time, ' s'
            print '--------------------------------------------------------------'

        # self.response_time = response_time

    def get_page_data(self, query):
        """
            获取分页数据
        """
        page_size = int(self.get_argument("page_size",30))
        page = int(self.get_argument("page", 1))
        if page<=0:
            page=1
        offset = (page - 1) * page_size #从数据库查询数据的起始位置
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_url(self, page,form_id=None):

        """参数解析
        :page 页号
        :form_id
        """
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        qdict={}
        if self.request.method=='GET':
            query = self.request.query
            #qdict =
            for k, v in urlparse.parse_qs(query).items():
                if isinstance(v, list):
                    qdict[k] = v and v[0] or ''
                #else:self.qdict[k] = v and v[0] or ''
            qdict['page'] = page
        else:
            qdict={}
            query = self.request.arguments
            for key in query.keys():
                qdict[key]=len(query[key])==1 and (query[key][0] and query[key][0] or '') or query[key]
        return path + '?' + urllib.urlencode(qdict)

    def _handle_request_exception(self, e):
        try:
            if self._finished:
                # Extra errors after the request has been finished should
                # be logged, but there is no reason to continue to try and
                # send a response.
                return
            print e
            self.log_exception(*sys.exc_info())

            try:
                self.db.close()
            except:
                pass
            # return self.redirect('/404')
            pass
            self.echo('ops/500.html', layout='')
            self.finish()
        except:
            self.send_error(500, exc_info= sys.exc_info())

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

class MobileBaseHandler(MobileTenjinBase):

    STATIC_DOMAIN = ''

    @property
    def db(self):
        return self.application.db

    @property
    def mcache(self):
        return self.application.mcache

    @property
    def rcache(self):
        return self.application.rcache

    def echo(self, template, context=None, globals=None,layout=None):
        data = self.render(template, context, globals,layout)
        self.write(data)

    def echoQ(self, template, context=None, globals=None, layout=''):
        data = self.render(template, context, globals, layout)
        self.write(data)

    def get_current_user(self):
        json = self.get_secure_cookie("loginuser",None)
        info = ujson.loads(json) if json else None
        if info:
            return info
        else:
            return None

    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台

        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX

        global stat_time
        stat_time = timeit.default_timer()
        user_agent = self.request.headers.get('User-Agent')

    def on_finish(self):
        if self.db:
            self.db.close()
        global stat_time

        # """ 重写结束请求前的方法函数 """
        # if self.request.method == "POST":
        #     # 如果遇到POST提交则清空缓存
        #     self.mcache.flush()

        response_time = 0
        response_time = (timeit.default_timer() - stat_time) % 1000
        if response_time > 0:
            print '---------------------------RT---------------------------------'
            print '-> Current url   : ', self.request.uri
            print '-> Response time : ', response_time, ' s'

    def get_error_html(self, status_code=500, log_message='', *args, **kwargs):
        pars = {
           'log_message':log_message,
           'args':args,
           'kwargs':kwargs,
           }
        if status_code==400:
            return self.echo('apps_crm/common/404.html')
        return self.echo("apps_crm/common/error.html", **pars)

    def get_page_data(self,query,page_size=None,page=None):
        if not page_size:
            page_size = int(self.get_argument("page_size",50))
        if not page:
            page = int(self.get_argument("page", 1))
        page=int(page)
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def check_arg(self, name, rgx, default=None):
        val = self.get_argument(name) if default==None else self.get_argument(name, default)
        if val == default:
            return default
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return val
        else:
            raise Error('2000', name, "参数错误")

    def check_arg_2(self,name,rgx):
        val = self.get_argument(name)
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return True,''
        else:
            return False,name+'参数错误'

    def get_page_view(self,table_name,object_id,current_db_count_views=0):
        '''
        获取object 浏览量
        :param table_name:
        :param object_id:
        :param current_db_count_views:
        :return:
        '''
        result_counts=0
        try:
            view_count = self.rcache.hget(str(table_name),int(object_id))
            if current_db_count_views and view_count:
                result_counts = int(current_db_count_views)+int(view_count)
            elif current_db_count_views and not view_count:
                result_counts = current_db_count_views
            elif not view_count and not current_db_count_views:
                count_sql = 'select Fpage_view from {0} where Fid={1}'
                results = self.db.execute(count_sql.format(table_name,int(object_id))).scalar()
                result_counts = results
        except Exception,e:
            pass
            view_count=1
        if not view_count or view_count=='None':
            result_counts=1
        return result_counts

    def _handle_request_exception(self, e):
        try:
            if self._finished:
                # Extra errors after the request has been finished should
                # be logged, but there is no reason to continue to try and
                # send a response.
                return
            self.log_exception(*sys.exc_info())

            try:
                self.db.close()
            except:
                pass
            # return self.redirect('/404')

            pass
            self.echo('crm/500.html', layout='')
            self.finish()
        except:
            self.send_error(500, exc_info= sys.exc_info())

    def get_page_url(self, page,form_id=None):

        """参数解析
        :page 页号
        :form_id
        """
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        qdict={}
        if self.request.method=='GET':
            query = self.request.query
            #qdict =
            for k, v in urlparse.parse_qs(query).items():
                if isinstance(v, list):
                    qdict[k] = v and v[0] or ''
                #else:self.qdict[k] = v and v[0] or ''
            qdict['page'] = page
        else:
            qdict={}
            query = self.request.arguments
            for key in query.keys():
                qdict[key]=len(query[key])==1 and (query[key][0] and query[key][0] or '') or query[key]
        return path + '?' + urllib.urlencode(qdict)

class BaseApiHandler(ViewsTenjinBase):

    data={}

    @property
    def db(self):
        return self.application.db

    @property
    def mcache(self):
        return self.application.mcache

    @property
    def rcache(self):
        return self.application.rcache

    def get_current_user(self):
        json = self.get_secure_cookie("loginuser",None)
        info = ujson.loads(json) if json else None
        if info:
            return info
        else:
            return None

    def get_photo_url(self, user, size="normal"):
        if not user:
            return self.static_url("default.png")

        photo = "photo_url" if size == "normal" else "middle_photo_url"
        if photo not in user and user[photo]:
            photo = "photo_url"

        if not user[photo]:
            return self.static_url("images/default.png")
        if "open" in user and user["open"] != "google":
            if user[photo].startswith("http"):
                return user[photo]
        return self.static_url("icons/%s" % user[photo])

    stat_time = 0.0

    def prepare(self):

        # super(BaseHandler, self).prepare()
        # 如果请求是GET方法,而且不是请求后台

        self.STATIC_DOMAIN = options.STATIC_FILE_DOMAIN
        #self.STATIC_FILE_PREFIX = options.STATIC_FILE_PREFIX

        global stat_time
        stat_time = timeit.default_timer()
        user_agent = self.request.headers.get('User-Agent')
        print 'userAgent:',user_agent
        # if self.request.method == "GET" and CACHED and \
        #    not self.request.path.startswith("/admin"):
        #
        #     # 尝试获取当前页面的缓存
        #     cache = self.mcache.get(self.request.uri)
        #     # 获取缓存则输出页面,结束请求
        #     if cache:
        #         return self.finish(cache)

    def on_finish(self):
        if self.db:
            self.db.close()
        global stat_time

        # """ 重写结束请求前的方法函数 """
        # if self.request.method == "POST":
        #     # 如果遇到POST提交则清空缓存
        #     self.mcache.flush()

        response_time = 0
        response_time = (timeit.default_timer() - stat_time) % 1000
        if response_time > 0:
            print '---------------------------RT---------------------------------'
            print '-> Current url   : ', self.request.uri
            print '-> Response time : ', response_time, ' s'
            print '--------------------------------------------------------------'

        # self.response_time = response_time

    def get_error_html(self, status_code=500, log_message='', *args, **kwargs):
        pars = {
           'log_message':log_message,
           'args':args,
           'kwargs':kwargs,
           }
        if status_code==400:
            return self.echo('apps_crm/common/404.html')
        return self.echo("apps_crm/common/error.html", **pars)

    def get_page_data(self,query,page_size=None,page=None):
        if not page_size:
            page_size =  int(self.get_argument("page_size",50))
        if not page:
            page = int(self.get_argument("page", 1))
        page = int(page)
        offset = (page - 1) * page_size
        result = query.limit(page_size).offset(offset)
        page_data = Paginator(self.get_page_url, page, query.count(), page_size)
        page_data.result = result
        return page_data

    def get_page_url(self, page,form_id=None):
        if form_id:
            return "javascript:goto_page('%s',%s);" %(form_id.strip(),page)
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def check_arg(self, name, rgx, default=None):
        val = self.get_argument(name) if default==None else self.get_argument(name, default)
        if val == default:
            return default
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return val
        else:
            raise Error('2000', name, "参数错误")

    def check_arg_2(self,name,rgx):
        val = self.get_argument(name)
        patt = re.compile(rgx)
        match = patt.match(val)
        if match and match.group():
            return True,''
        else:
            return False,name+'参数错误'

    def echo(self, template, context=None, globals=None,layout='view/common/base.html'):
        data = self.render(template, context, globals,layout)
        self.write(data)

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

    def write_json(self,data):
        '''
        :todo 返回json数据
        :param data:
        :return:
        '''
        return self.write(ujson.dumps(data))

    def get_page_list(self,lstdata,page_size=None,page=None):
        page = int(page)
        offset = (page-1)*page_size
        return lstdata[offset:offset+page_size]

    def get_total_page(self,lst,page_size):
        total_page = (len(lst) % page_size==0) and (len(lst)/page_size) or int(math.ceil(len(lst) / page_size))+1
        return total_page

    def execute_datetime(self,inputtime):
        execute_time = (datetime.datetime.now()-inputtime)
        total_seconds = execute_time.total_seconds()
        if total_seconds<60:
            return str(total_seconds)+'秒前'
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

    def get_page_view(self,table_name,object_id,current_db_count_views=0):
        '''
        获取object 浏览量
        :param table_name:
        :param object_id:
        :param current_db_count_views:
        :return:
        '''
        result_counts = 1
        try:
            view_count = self.rcache.hget(str(table_name),object_id)
            result_counts = int(0 if not view_count else view_count) + int(current_db_count_views)
        except Exception,e:
            pass
        return result_counts

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
        data = self.mcache.get(key)
        if not data:
            user_service.set_db(self.db)
            user = user_service.get_user_by_id(key)
            data = {'nick_name':user.Fnick_name,'photo_url':user.Fphoto_url}
            self.mcache.set(key,data)
        return data

    def _handle_request_exception(self, e):
        try:
            if self._finished:
                # Extra errors after the request has been finished should
                # be logged, but there is no reason to continue to try and
                # send a response.
                return
            self.log_exception(*sys.exc_info())

            try:
                self.db.close()
            except:
                pass
            # return self.redirect('/404')

            pass
            self.echo('crm/500.html', layout='')
            self.finish()
        except:
            self.send_error(500, exc_info= sys.exc_info())

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

    def get_series_info(self,series_id):
        '''
        todo:获取套系信息
        :param series_id:
        :return:
        '''
        my_key = 'single_series_'+str(series_id)
        series = self.mcache.get(my_key)
        if not series:
            series_servie.set_db(self.db)
            data = {}
            data['id'] = series_id
            query = series_servie.query_series(**data)
            series = query.scalar()
            self.mcache.set(my_key,series,86400)
        return series

