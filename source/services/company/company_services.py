# encoding:utf-8
__author__ = 'frank'

from services.base_services import *
from models.company_do import Company, CompanyUsers, CompanyAdditionInfo,CompanyGift
from models.user_do import Users, Permission, UserRoles
from models.staffer_do import Staffers, Department
from utils.md5_util import create_md5
import uuid

class CompanyServices(BaseService):

    def create_company(self,user_id,**kargs):
        '''
        todo:创建商户
        :param user_id: 商户id
        :param user: 商户联系人
        :param name: 商户名
        :param addr: 商户联系地址
        :return:
        '''
        # kargs.get('merchant_name'),
        # kargs.get('merchant_addr'),
        # kargs.get('phone'),
        # kargs.get('email'),
        # kargs.get('user_name'),
        # Fprovince=kargs.get('Fprovince',None),
        # Fcity=kargs.get('Fprovince',None),
        # Farea=kargs.get('Fprovince',None)
        company = Company()

        company.Fcompany_name = kargs.get('merchant_name')
        #company.Fcontact = nick_name
        company.Fdetail_address  = kargs.get('merchant_addr')
        company.Fuser_id = user_id
        company.Fphone = kargs.get('phone','')
        company.Fmail = kargs.get('email')
        company.Fcontact = kargs.get('user_name','')
        if kargs.get('Fprovince',None):
            company.Fprovince = kargs.get('Fprovince')
        if kargs.get('Fcity',None):
            company.Fcity = kargs.get('Fcity')
        if kargs.get('Farea',None):
            company.Farea = kargs.get('Farea')
        if kargs.get('Fphoto_url',None):
            company.Fphoto_url = kargs.get('Fphoto_url')
        if kargs.get('Fqq',None):
            company.Fqq = kargs.get('Fqq')
        self.db.add(company)
        self.db.commit()
        return company

    def get_companys(self,**kwargs):
        '''
        todo：根据条件查询所有的公司
        :param kwargs:
        :return:
        '''
        query = self.db.query(Company).filter(Company.Fdeleted == 0)
        if kwargs.get('company_name', ''):
            query = query.filter(Company.Fcompany_name.like('%'+kwargs.get('company_name')+'%'))
        if kwargs.get('user_name', ''):
            content = kwargs.get('user_name', '')
            user_id = self.db.query(Users.Fid).filter(Users.Fnick_name.like('%'+kwargs.get('user_name','')+'%'))
            query = query.filter(Company.Fuser_id.in_(user_id))
        if kwargs.get('area',''):
            query = query.filter(Company.Farea==kwargs.get('area'))
        if kwargs.get('price_between',''):
            start,end = kwargs.get('price_between').split('-')
            if start:
                query = query.filter(Company.Fcheapest>=start)
            if end:
                query = query.filter(Company.Fmost_expensive<=end)
        if kwargs.get('style',''):
            query = query.filter(Company.Fstyle_tags.like(('%'+kwargs.get('style')+'%')))
        if kwargs.get('user_id',''):
            query = query.filter(Company.Fuser_id == kwargs.get('user_id'))

        if kwargs.get('order','Fcreate_time'):
                query = query.order_by(kwargs.get('order','Fcreate_time'))
        return query

    def get_company_by_uid(self, uid_mct):
        return self.db.query(Company).filter(
            Company.Fuser_id == uid_mct,
            Company.Fdeleted == 0).scalar()

    def get_company_by_id(self, company_id):
        '''
        todo:根据公司id查询公司对象
        :param company_id:公司id
        :return:
        '''
        company = self.db.query(Company).filter(Company.Fdeleted == 0,Company.Fid == company_id).scalar()
        return company

    def update_company_by_uid(self, uid_mct, **kwargs):
        '''
        todo:根据公司id修改公司对象
        :param uid_mct:商户id
        :return:
        '''
        query = self.db.query(Company).filter(
            Company.Fuser_id == uid_mct,
            Company.Fdeleted == 0)
        query.update(kwargs)
        self.db.commit()

    def update_company_by_id(self,company_id,**kwargs):
        '''
        todo:根据公司id修改公司对象
        :param company_id:公司id
        :return:
        '''
        if kwargs.get('nick_name','') or kwargs.get('user_mobi',''):
            company = self.get_company_by_id(company_id)
            query_user = self.db.query(Users).filter(Users.Fid == company.Fuser_id,Users.Fdeleted == 0)
            data = {}
            data['Fnick_name'] = kwargs.get('nick_name')
            data['Fuser_mobi'] = kwargs.get('user_mobi')
            query_user.update(data)
            self.db.commit()
            kwargs.pop('nick_name')
            kwargs.pop('user_mobi')
            kwargs.pop('_xsrf')
        query = self.db.query(Company).filter(Company.Fid == company_id,Company.Fdeleted == 0)
        query.update(kwargs)
        self.db.commit()

    def delete_company_by_id(self,company_id):
        '''
        todo:根据公司id删除公司对象
        :param company_id:公司id
        :return:
        '''
        data = {}
        data['Fdeleted'] = 1
        query = self.db.query(Company).filter(Company.Fdeleted == 0,Company.Fid == company_id)
        query.update(data)
        self.db.commit()

    def get_staffers_by_user_id(self,user_id):
        '''
        todo:根据公司的user_id（所属商户id）查询该公司下所有的员工
        :param user_id:公司的user_id
        :return:
        '''
        query = self.db.query(Staffers).filter(Staffers.Fdeleted == 0,Staffers.Fuid_mct == user_id)
        return query

    def get_departments_by_user_id(self,user_id,department_id):
        '''
        todo:根据商户id查询该商户的所有级别部门
        :param user_id:商户id
        :param department_id:部门id
        :return:
        '''
        if not department_id:
            query = self.db.query(Department).filter(Department.Fdeleted == 0,Department.Fuid_mct == user_id,
                                                     Department.Fdepartment_father == 0)
        else:
            query = self.db.query(Department).filter(Department.Fdeleted == 0,Department.Fuid_mct == user_id,
                                                     Department.Fdepartment_father == department_id)
        return query

    def create_login_account(self,mct_id,**kwargs):
        '''
        todo:创建商户可登录用户
        :param mct_id:商户id
        :param kwargs:
        :return:
        '''
        is_success,info = self.account_check_exist(**kwargs)
        if not is_success:
            return is_success,info
        user = Users()
        user.Fuid = self.user_uid(username = kwargs.get('user_name'))
        user.Fuser_name = kwargs.get('user_name')
        user.Fuser_pwd = self.user_passed(kwargs.get('user_pwd'),user.Fuid)
        user.Fnick_name = kwargs.get('nick')
        user.Fstatus = kwargs.get('status','normal')
        if kwargs.get('permission',None):
            permissions = self.db.query(Permission).filter(Permission.Fdeleted == 0,Permission.Fid.in_(kwargs.get('permission')))
            if permissions:
                user.Fpermission = ','.join([p.Fcode for p in permissions])
        user.Femail = kwargs.get('email')
        user.Fuser_mobi = kwargs.get('phone')
        self.db.add(user)
        self.db.commit()

        company_user = CompanyUsers()
        company_user.Fuid_mct = mct_id
        company_user.Fuser_id = user.Fid
        company_user.Fcompany_id = self.get_company_by_uid(mct_id).Fid
        if kwargs.get('permission',None):
            permissions = self.db.query(Permission).filter(Permission.Fdeleted == 0,Permission.Fid.in_(kwargs.get('permission')))
            company_user.Fpermission = ','.join([p.Fcode for p in permissions])
        self.db.add(company_user)
        self.db.commit()
        return True

    def account_check_exist(self,**kargs):

        """注册检测  用户名手机是否已经被占用
        """
        if kargs.get('user_name')and self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_name == kargs.get('user_name')).count()>0:
            return False,'用户名:'+kargs.get('user_name')+' 已经存在'
        if kargs.get('email') and self.db.query(Users).filter(Users.Fdeleted==0,Users.Femail == kargs.get('email')).count()>0:
            return False,'邮箱:'+kargs.get('email')+' 已经存在'
        if kargs.get('phone') and self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi == kargs.get('phone')).count()>0:
            return False,'手机号:'+kargs.get('phone')+' 已经存在'
        return True,''

    def user_uid(self,**kwargs):
        '''
        创建用户uuid
        :param kwargs:
        :return:
        '''
        name = ''
        if kwargs.get('user_name',None):
            name = kwargs.get('user_name')
        elif kwargs.get('phone',None):
            name = kwargs.get('phone')
        elif kwargs.get('email',None):
            name = kwargs.get('email')
        uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS,str(name))
        return str(uuid_str)

    def user_passed(self,passwd,uuid):
        """密码验证"""
        return create_md5(create_md5(passwd+uuid))

    def get_gift(self,merchant_id,type):
        '''
        todo:获取到店礼；订单礼
        :param merchant_id:
        :return:
        '''
        query = self.db.query(CompanyGift).\
            filter(CompanyGift.Fdeleted == 0,CompanyGift.Fuid_mct == merchant_id,CompanyGift.Fgift_type == type)
        return query

    def create_gift(self,**kwargs):
        '''
        todo:创建到店礼，订单礼
        :return:
        '''
        merchant_id = kwargs.get('merchant_id','')
        type = kwargs.get('type','')
        content = kwargs.get('content','')
        query = self.get_gift(merchant_id,type)
        if query.count():
            query.update({'Fcontent':content})
            self.db.commit()
        else:
            cg = CompanyGift()
            cg.Fgift_type = type
            cg.Fcontent = content
            cg.Fuid_mct = merchant_id
            self.db.add(cg)
            self.db.commit()

    def get_companys_by_role(self, role_code, **kwargs):
        query = self.db.query(Company).join(Users, Company.Fuser_id==Users.Fid).\
                                       filter(Users.Frole_codes.like('%'+role_code+'%')).\
                                       filter(Company.Fdeleted==0)

        if kwargs.get('between_price'):
            kwargs['start_price'], kwargs['end_price'] = kwargs.get('between_price').split('-')

        if kwargs.get('start_price'):
            query = query.filter(Company.Fcheapest >= float(kwargs.get('start_price').strip()))

        if kwargs.get('end_price'):
            query = query.filter(Company.Fmost_expensive <= float(kwargs.get('end_price').strip()))

        if kwargs.get('area',''):
            query = query.filter(Company.Farea==kwargs.get('area'))

        if kwargs.get('order_by', 'Fcreate_time'):
            try:
                query = query.order_by(getattr(Company, kwargs.get('order_by', 'Fcreate_time')))
            except Exception, e:
                query = query.order_by(kwargs.get('order_by', 'Fcreate_time'))

        return query

    def update_range_price(self, merchant_id, *args):
        # args为属于公司的套系、作品等对象, 每个对象都有min_and_max_price函数
        # x和y同时存在或不存在
        min_price, max_price = None, None
        for obj in args:
            x, y = obj.min_and_max_price(merchant_id)
            if x and y:
                if min_price and max_price:
                    min_price, max_price = min(min_price, x), max(max_price, y)
                else:
                    min_price, max_price = x, y  # 第一个同时存在x和y

        if min_price and max_price:
            self.db.query(Company).\
                    filter(Company.Fdeleted==0).\
                    filter(Company.Fuser_id==merchant_id).\
                    update({Company.Fcheapest: min_price, Company.Fmost_expensive: max_price})
            self.db.commit()


class CompanyUserServices(BaseService):

    def query_users(self, uid_mct):
        company_users = self.db.query(CompanyUsers).\
            filter(CompanyUsers.Fuid_mct == uid_mct,CompanyUsers.Fdeleted == 0)
        id_list = [company_user.Fuser_id for company_user in company_users]
        if id_list:
            users = self.db.query(Users).filter(Users.Fdeleted == 0,Users.Fid.in_(id_list))
        else:
            users=[]
        return users
        #     lstdata.append(user)
        # return lstdata

    def edit_users(self, uid_mct, user_id, **kwargs):
        qry = self.db.query(Users).filter(
            Users.Fid == user_id,
            Users.Fdeleted == 0
            )
        qry.update(kwargs)
        if "Fpermission" not in kwargs.keys():
            return
        qry_c = self.db.query(CompanyUsers).filter(
            CompanyUsers.Fuser_id == user_id,
            CompanyUsers.Fuid_mct == uid_mct,
            CompanyUsers.Fdeleted == 0
            )
        qry_c.update({"Fpermission": kwargs['Fpermission']})
        self.db.commit()

    def delete_users(self, uid_mct, user_id):
        qry = self.db.query(Users).filter(
            Users.Fid == user_id,
            Users.Fdeleted == 0
            )
        qry.update({'Fdeleted': 1})
        qry_c = self.db.query(CompanyUsers).filter(
            CompanyUsers.Fuid_mct == uid_mct,
            CompanyUsers.Fuser_id == user_id,
            CompanyUsers.Fdeleted == 0)
        qry_c.update({'Fdeleted': 1})
        self.db.commit()

    def add_users(self,**kwargs):
        user = Users()
        user.Fuser_mobi = kwargs.get('Fuser_mobi','')
        user.Fuid = kwargs.get('Fuid')
        user.Fuser_pwd = kwargs.get('Fuser_pwd')
        user.Fnick_name = kwargs.get('Fuser_name','')
        user.Femail = kwargs.get('Femail','')
        user.Fpermission = kwargs.get('Fpermission','')
        self.db.add(user)
        self.db.commit()
        return user

    def add_company_user(self,user,uid_mct,**kwargs):
        com_user = CompanyUsers()
        com_user.Fuser_id = user.Fid
        com_user.Fuid_mct = uid_mct
        com_user.Fcompany_id = kwargs['Fcompany_id']
        com_user.Fpermission = kwargs['Fpermission']
        self.db.add(com_user)
        self.db.commit()

class CompanyAdditionInfoServices(BaseService):
    """处理公司附加信息"""
    def update_info(self, uid_mct, **kwargs):
        if 'Fid' in kwargs:
            qry = self.db.query(CompanyAdditionInfo).filter(
                CompanyAdditionInfo.Fid == kwargs['Fid'],
                CompanyAdditionInfo.Fdeleted == 0)
            qry.update(kwargs)
        else:
            info = CompanyAdditionInfo()
            info.Finfo_key = kwargs['Finfo_key']
            info.Finfo = kwargs['Finfo']
            info.Fuid_mct = uid_mct
            self.db.add(info)
        self.db.commit()

    def query_info(self, uid_mct, info_key):
        return self.db.query(CompanyAdditionInfo).filter(
            CompanyAdditionInfo.Fuid_mct == uid_mct,
            CompanyAdditionInfo.Fdeleted == 0,
            CompanyAdditionInfo.Finfo_key == info_key)

