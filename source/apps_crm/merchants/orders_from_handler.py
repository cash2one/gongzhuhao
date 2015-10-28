#encoding:utf-8
__author__ = 'binpo'
from common.base import BaseHandler
from models.order_do import OrderFromConf
import ujson
import tornado

class OrdersFromInfoQueryHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        merchant_id = self.get_current_user().get('Fmerchant_id')
        query = self.db.query(OrderFromConf).filter(OrderFromConf.Fdeleted==0,OrderFromConf.Fmerchant_id==merchant_id)
        self.echo('crm/system/orders_from_info.html',{'data':query},layout='crm/common/base.html')

class OrdersFromInfoCreateHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        data={"state":'ok','info':'创建成功'}
        merchant_id = self.get_current_user().get('Fmerchant_id')
        name = self.get_argument('name','')
        from_id = self.get_argument('order_from_id','')
        if not name:
            data={'state':'err','info':'名称不能为空'}
        else:
            if from_id:
                order_from = self.db.query(OrderFromConf).filter(OrderFromConf.Fdeleted==0,OrderFromConf.Fid==from_id).first()
                try:
                    if not order_from:
                        order_from = OrderFromConf()
                    order_from.Fname = name
                    order_from.Fmerchant_id = merchant_id
                    self.db.add(order_from)
                    self.db.commit()
                except Exception,e:
                    data={'state':'err','info':"创建失败:"+e.message}
            else:
                order_from = self.db.query(OrderFromConf).filter(OrderFromConf.Fdeleted==0,OrderFromConf.Fmerchant_id==merchant_id,OrderFromConf.Fname==name).first()
                if order_from:
                    data={'state':'err','info':'来源已经存在'}
                else:
                    order_from = OrderFromConf()
                    order_from.Fname = name
                    order_from.Fmerchant_id = merchant_id
                    self.db.add(order_from)
                    self.db.commit()
        return self.write(ujson.dumps(data))

class OrdersFromInfoDeleteHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self,from_id,**kwargs):
        merchant_id =  self.get_current_user().get('Fmerchant_id')
        self.db.query(OrderFromConf).filter(OrderFromConf.Fid==from_id,OrderFromConf.Fmerchant_id==merchant_id).update({'Fdeleted':1})
        self.write(ujson.dumps({'state':'ok','info':'删除成功'}))

    def post(self, *args, **kwargs):
        pass
