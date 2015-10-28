#encoding:utf-8
__author__ = 'wangjinkuan'

from common.cache_base import MobileCacheHandler
from apps_mobile.mobile_base import MobileBaseHandler
from services.share.share_service import ShareService
from services.orders.order_services import OrderServices
from services.schedules.schedules_service import ScheduleService
from conf.order_conf import _ORDER_STATUS,EVALUATION_CODES
import sys
import time

share_service = ShareService()
order_service = OrderServices()
schedule_service = ScheduleService()
PAGE_SIZE = 100

class ShareHandlerList(MobileBaseHandler,MobileCacheHandler):

    def get(self,page):
        '''
        todo:获取分享列表
        :return:
        '''
        share_service.set_db(self.db)
        if not page or int(page) < 1:
            page = 1
        try:
            query = share_service.get_share_list()
            shares = self.get_page_data(query,page_size=PAGE_SIZE,page=page)
            if int(page) > 1:
                return self.other_pages(shares)
            self.echo('views/share/share_page.html',{'shares':shares},layout='views/share/index.html')
        except Exception,e:
            pass
            return self.echo('views/500.html')

    def other_pages(self,shares):
        _html = self.render('views/share/share_page.html',{'shares':shares})
        self.write_json({'stat':1000,'data':_html,'info':''})

    def get_user(self,user_id):
        '''
        todo:获取用户信息
        :param user_id:
        :return:
        '''
        user = self.get_user_info(user_id)
        return user.get('nick_name'),user.get('photo_url') and user.get('photo_url') or '/static/images/avatar.png'

class ShareDetailHandler(MobileBaseHandler,MobileCacheHandler):

    def get(self,share_id):
        '''
        todo:分享detail
        :param share_id:
        :return:
        '''
        share_service.set_db(self.db)
        order_service.set_db(self.db)
        schedule_service.set_db(self.db)
        try:
            share = share_service.get_share_list(share_id = share_id).scalar()
            share_images = self.get_share_images(share_id)

            company_dict = self.get_company_info(share.Fmerchant_id)
            user = self.get_user_info(share.Fuser_id)
            order = order_service.get_order_by_id(order_id=share.Forder_id).scalar()

            lst_evaluation = []
            for code in EVALUATION_CODES:
                evaluation_dict = self.get_evaluation(order.Fid,code)
                if evaluation_dict:
                    lst_evaluation.append(evaluation_dict),

            if self.request.uri.startswith('/api/json/'):
                self.write_json({'stat':'ok',
                                 'data':{
                                         'order':{'order_status':_ORDER_STATUS[order.Fstatus],'time':order.Fcreate_time.strftime("%Y-%m-%d %H:%M:%S")},
                                         'evaluations':lst_evaluation,
                                         'share_images':share_images,
                                         'user':user,
                                         'company':company_dict
                                        },
                                 'info':''
                                })
            else:
                self.echo('views/share/details.html',
                          {'company':company_dict,
                           'user':user,
                           'order_status':_ORDER_STATUS[order.Fstatus],
                           'evaluations':lst_evaluation,
                           'share_images':share_images,
                           'time':order.Fcreate_time.strftime("%Y-%m-%d %H:%M:%S"),
                           'title':share.Ftitle
                          })
        except Exception,e:
            print e.message
            pass
            return self.echo('views/500.html')

    def get_total_score(self,fitting,shot,dressing,choose,final,give):
        '''
        todo:计算平均分
        :param fitting:
        :param shot:
        :param dressing:
        :param choose:
        :param final:
        :param give:
        :return:
        '''
        total_score = float(fitting+shot+dressing+choose+final+give)
        return int(round(total_score/6))










