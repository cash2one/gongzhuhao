#encoding:utf-8
__author__ = 'morichounami'
from models.user_do import *
from services.base_services import *

class MerchantsServices(BaseService):
    def query_all_merchants(self):
        self.db.query(Users).filter(Users.Fdeleted==0,Users.Frole_codes.like('%merchant%'))

    def update_fuid_by_fid(self,fid,**data):
        '''
        更新商户的Fuid
        :param fid: 商户Fid
        :param data: 保存着商户Fuid
        :return
        '''
        # query = self.db.query(Merchants).filter(Merchants.Fid==fid,
        #         Merchants.Fdeleted==False)
        # query.update(data)
        # self.db.commit()

    def get_merchant_by_fid(self,fid):
        '''
        :param fid:
        :return:对应fid的商户对象
        '''
        # return self.db.query(Merchants).filter(Merchants.Fid==fid,
        #         Merchants.Fdeleted==False).scalar()

    def merchant_format(self,merchant):
        '''
        :param merchant:商户对象
        :return:该对象的cookie
        '''
        # keys = ['Fid','Fuid','Fuser_mobi','Fuser_name','Fmct_name','Fmct_address']
        # cookies = {}
        # for key in keys:
        #     if merchant.__dict__.get(key,None):
        #         cookies[key] = merchant.__dict__.get(key,None)
        #     else:
        #         cookies=''
        # return cookies

    def check_merchant_passwd(self,username,passwd):
        '''
        验证商户密码
        :param username: 商户的用户名
        :param passwd:商户密码
        :return:
        '''
        # merchant = self.db.query(Merchants).filter(Merchants.Fuser_name==username,
        #         Merchants.Fdeleted==False).scalar()
        # if merchant:
        #     if merchant.Fuser_pwd == passwd:
        #         return True, merchant
        #     else:
        #         return False,'账号或密码错误'
        # else:
        #     return False, '账号或密码错误'
        #
        #















