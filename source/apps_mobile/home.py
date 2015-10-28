#encoding:utf-8
__author__ = 'wangjinkuan'

from apps_mobile.mobile_base import MobileBaseHandler
from common.cache_base import AppCacheHandler
import sys

class AppIndexHandler(MobileBaseHandler,AppCacheHandler):

    def get(self, *args, **kwargs):

        try:
            m_banner_first = self.get_banner('m_banner_first')
            m_banner_second = self.get_banner('m_banner_second')
            m_banner_third = self.get_banner('m_banner_third')
            lst_shares = self.get_user_share_info()

            self.write_json({'stat':'ok',
                             'data':{'banner_first':m_banner_first,
                                     'banner_second':m_banner_second,
                                     'banner_third':m_banner_third,
                                     'shares':lst_shares
                                    },
                             'info':''
                           })
        except Exception,e:
            print e.message
