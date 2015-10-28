#encoding:utf-8
__author__ = 'binpo'

import sys,ujson
from common.base import BaseApiHandler
from services.work.work_services import WorkServices
from services.company.company_services import CompanyServices

product_service = WorkServices()
company_service = CompanyServices()

class ProductQueryHandler(BaseApiHandler):

    def get(self):
        pass




class ProductDetailHandler(BaseApiHandler):

    def get(self,product_id, **kwargs):
        try:
            product_service.set_db(self.db)
            company_service.set_db(self.db)
            product,images = product_service.get_product_by_id(product_id)
            recent_products = product_service.query_work(merchant_id=product.Fmerchant_id,order_by='Fcreate_time').limit(3).offset(0)
            company = company_service.get_company_by_uid(product.Fmerchant_id)  #公司信息
            company_gift = company_service.get_gift(product.Fmerchant_id,1).scalar()       #到店礼
            order_gift = company_service.get_gift(product.Fmerchant_id,2).scalar()       #y优惠
            #1.商户订单,2.套系订单 3.作品订单
            order_url = '/order/create/3/'+str(product_id)+'/'+str(company.Fuser_id)
            self.echo('view/work/work_detail.html',
                         {'product':product,
                          'images':images,
                          'recent_products':recent_products,
                          'company':company,
                          'order_gift':order_gift,
                          'company_gift':company_gift,
                          'order_url':order_url
                          })
        except Exception,e:
            print e.message

            #raise HTTPError(500)

