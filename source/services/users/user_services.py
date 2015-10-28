#encoding:utf-8
__author__ = 'morichounami'
from utils.md5_util import create_md5
from services.base_services import BaseService
from models.user_do import *
import uuid
from utils.unicode_check import is_chinese
from sqlalchemy import func, or_
from services.users.role_services import *
from services.company.company_services import *
from models.company_do import Company, CompanyUsers
from sqlalchemy.sql import or_
from utils.random_util import get_random_char

class UserServices(BaseService):

    def query_users(self,**kwargs):
        query = self.db.query(Users).filter(Users.Fdeleted==0)
        if kwargs.get('start_date',''):
            query = query.filter(Users.Fcreate_time > kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(Users.Fcreate_time < kwargs.get('end_date') + ' 23:59:59')
        if kwargs.get('status',''):
            query = query.filter(Users.Fstatus==kwargs.get('status'))
        if kwargs.get('role',''):
            if kwargs.get('role') == 'user':
                query = query.filter(Users.Frole_codes == '',Users.Fpermission == '')
            else:
                query = query.filter(Users.Frole_codes.like('%'+kwargs.get('role')+'%'))
        if kwargs.get('search_text',''):
            content = kwargs.get('search_text')
            if '@' in content:
                query = query.filter(Users.Femail.like('%'+content+'%'))
            else:
                query = query.filter(or_(Users.Fnick_name.like('%'+content+'%'),Users.Fuser_name.like('%'+content+'%')))
        if kwargs.get('user_mobi',''):
            content = kwargs.get('user_mobi')
            query = query.filter(Users.Fuser_mobi.like('%'+content+'%'))
        if kwargs.get('order_by'):
            query = query.order_by(kwargs.get('order_by'))
        return query

    def create_user(self,**kargs):
        '''
         :todo创建用户
        :param kargs:
        :return:
        '''
        is_ok,info = self.registe_check_exist(**kargs)
        if not is_ok:
            return is_ok,info
        user = Users()
        user.Fuid = self.user_uid(user_name=kargs.get('user_name'),phone=kargs.get('phone'))
        user.Fuser_mobi = kargs.get('phone')
        user.Fuser_name = kargs.get('user_name')
        user.Fnick_name = kargs.get('nick')
        user.Fstatus = kargs.get('status','normal')
        user.Fuser_pwd = self.user_passed(kargs.get('user_pwd'),user.Fuid)
        user.Femail = kargs.get('email','')
        if kargs.get('roles',None):
            user_roles = self.db.query(Roles).filter(Roles.Fid.in_(kargs.get('roles',''))).all()
            if user_roles:
                user.Frole_codes = ','.join([r.Fcode for r in user_roles])
        user.is_employee = kargs.get('is_employee',0)
        self.db.add(user)
        self.db.commit()
        if kargs.get('roles',None):
            self.add_user_roles(user.Fid,kargs.get('roles'))
        if 'merchant' in user.Frole_codes:
            CompanyServices(self.db).create_company(user.Fid,**kargs)

        return True,user

    def check_user_passwd(self,name,passwd):
        '''
        :todo 检测密码
        :param name:
        :param passwd:
        :return:
        '''
        user = self.db.query(Users).filter(Users.Fdeleted==False).filter(Users.Fuser_name==name).scalar()
        if user:
            if user.Fuser_pwd == self.user_passed(passwd,user.Fuid):
                return user
        return False

    def user_format(self,user):
        '''
        :param user: user对象
        :return: 该对象的cookiers
        '''
        keys = ['Fid','Frole_codes','Fnick_name','is_employee','Fuser_name', 'Femail','Fphoto_url','Fpermission','Fuser_mobi']

        return {key: getattr(user, key, '') for key in keys}

    def user_format_app(self,user):
        keys = ['Fid','Fnick_name','Fphoto_url','Frole_codes','Fpermission','Femail','is_employee']

        return {key: getattr(user, key, '') for key in keys}

    def get_user_by_id(self,user_id):
        """根据id查询用户
        :param user_id 用户ID
        """
        user = self.db.query(Users).filter(Users.Fid == user_id,Users.Fdeleted==0).scalar()
        return user


    def user_uid(self,**kargs):
        """
        :todo 生成uuid
        :param name 用户名 如果是手机注册用手机号  微信注册用微信号
        """
        if kargs.get('user_name',None):
            name = kargs.get('user_name')
        elif kargs.get('phone',None):
            name = kargs.get('phone')
        elif kargs.get('email',None):
            name = kargs.get('email')
        uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, str(name))
        return str(uuid_str)

    def user_passed(self,passwd,uuid):
        """密码验证"""
        return create_md5(create_md5(passwd+uuid))

    def login_with_phone(self,phone,passwd):
        '''
        :todo 用户账号登陆
        :param phone:
        :param passwd:
        :return:
        '''
        user = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi==phone).scalar()
        if user:
            if user.Fuser_pwd==self.user_passed(passwd,user.Fuid):
                return user
        return None

    def login_with_username(self,user_name,passwd):
        '''
        :todo 用户名登陆
        :param user_name:
        :param passwd:
        :return:
        '''
        user = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_name==user_name).first()
        if user:
            if user.Fuser_pwd==self.user_passed(passwd,user.Fuid):
                return user
        return None

    def create_merchant_user(self,**kargs):
        pass

    def get_roles(self):
        '''
        获取所有角色shang h
        :return:l
        '''
        return self.db.query(Roles).filter(Roles.Fdeleted==0).all()

    def get_user_by_phone(self,phone):
        '''
        :根据电话获取账户
        :param phone:
        :return:
        '''
        query = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi==phone)
        if query.count()>0:
            return query.first()
        return None

    def registe_check_exist(self,**kargs):

        """注册检测  用户名手机是否已经被占用
        """
        if kargs.get('user_name')and self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_name == kargs.get('user_name')).count()>0:
            return False,'用户名:'+kargs.get('user_name')+' 已经存在'
        if kargs.get('email') and self.db.query(Users).filter(Users.Fdeleted==0,Users.Femail == kargs.get('email')).count()>0:
            return False,'邮箱:'+kargs.get('email')+' 已经存在'
        if kargs.get('phone') and self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi == kargs.get('phone')).count()>0:
            return False,'手机号:'+kargs.get('phone')+' 已经存在'
        return True,''

    def add_user_roles(self,user_id,roles):
        '''
        :todo 用户添加角色
        :param user_id:
        :param roles:
        :return:
        '''
        if roles:
            for r in roles:
                userRoles = UserRoles()
                userRoles.Fuser_id = user_id
                userRoles.Frole_id = r
                self.db.add(userRoles)
            self.db.commit()

    def set_user_roles(self,user_id,roles):
        """
        :todo 用户授权
        :param user_id 用户ID
        :param roles 角色列表
        """
        try:
            self.db.query(UserRoles).filter(UserRoles.Frole_id.in_(roles)).delete(synchronize_session=False) #操作多条数据时使用
            roles_ = self.db.query(Roles).filter(Roles.Fid.in_(roles)).all()
            self.db.query(Users).filter(Users.Fid == user_id).update({'Frole_codes':','.join([r.Fcode for r in roles_])})
            self.add_user_roles(user_id,roles)
        except Exception,e:
            print e

    def reset_passwd(self,user_id,passwd,user=None):
        if not user:
            user = self.get_user_by_id(user_id)
        user.Fuser_pwd = self.user_passed(passwd,user.Fuid)
        self.db.add(user)
        self.db.commit()
        #self.update_user(user_id,Fuser_pwd=self.user_passed(passwd,user.Fuid))


    def update_user(self,item_id,**kwargs):
        '''
        todo:更新对象
        :param user_id:
        :param kwargs:
        :return:
        '''
        query = self.db.query(Users).filter(Users.Fid==item_id)
        if kwargs.get('roles',None):
            roles_ = self.db.query(Roles).filter(Roles.Fdeleted == 0,Roles.Fid.in_(kwargs.get('roles')))
            if roles_:
                kwargs['Frole_codes'] = ','.join([r.Fcode for r in roles_])
            kwargs.pop('roles')
        query.update(kwargs)
        self.db.commit()

    def set_user_reeze(self,user_id):
        '''
        todo：禁用用户
        :param user_id: 用户id
        :return:
        '''
        query = self.db.query(Users).filter(Users.Fdeleted == 0,Users.Fid == user_id)
        data = {}
        data['Fstatus'] = 'reeze'
        query.update(data)
        self.db.commit()

    def get_merchant_id_by_child_acount(self,child_user_id):
        '''
        根据子账号获取公司信息
        :param child_user_id:
        :return:
        '''
        company_user = self.db.query(
            CompanyUsers.Fuid_mct,
            CompanyUsers.Fcompany_id,
            Company.Fcompany_name).filter(
                CompanyUsers.Fdeleted == 0,
                CompanyUsers.Fuser_id == child_user_id,
                CompanyUsers.Fcompany_id == Company.Fid
                ).first()
        data = {}
        if company_user:
            data['Fmerchant_id'] = company_user.Fuid_mct
            data['Fcompany_id'] = company_user.Fcompany_id
            data['Fcompany_name'] = company_user.Fcompany_name
        else:
            data['Fmerchant_id'] = ''
            data['Fcompany_id'] = ''
            data['Fcompany_name'] = ''
        return data

    def get_company_merchant_id(self,merchant_id):
        '''
        根据商户获取公司信息
        :param merchant_id:
        :return:
        '''
        return self.db.query(Company).filter(Company.Fuser_id==merchant_id).scalar()


    def query_user_by_phone(self,phone):
        '''
        :todo 根据电话号码查询用户
        :param phone:
        :return:
        '''
        return self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi==phone).scalar()

    def query_company_user(self,merchant_id,user_id):
        '''
        todo:查询商户的可登陆用户
        :param merchant_id:
        :param user_id:
        :return:
        '''
        return self.db.query(CompanyUsers).\
            filter(CompanyUsers.Fdeleted == 0,CompanyUsers.Fuid_mct == merchant_id,CompanyUsers.Fuser_id == user_id).scalar()

    def query_user_by_userName(self,user_name):
        '''
        todo:检测重复的用户名
        :param user_name:
        :return:
        '''
        return self.db.query(Users).filter(Users.Fuser_name == user_name,Users.Fdeleted == 0).scalar()

    def query_user_by_email(self,email):
        '''
        todo:检测重复的用户邮箱
        :param email:
        :return:
        '''
        return self.db.query(Users).filter(Users.Femail == email,Users.Fdeleted == 0).scalar()

    def create_user_by_order(self,phone,passwd,nick=None):
        '''
        :todo 创建订单生成用户
        :param phone:
        :param passwd:
        :param nick:
        :return:
        '''
        user = self.query_user_by_phone(phone)
        if user:
            return True,False,user
        else:
            user = Users()
            user.Fuid = self.user_uid(user_name=phone)
            user.Fuser_mobi = phone
            user.Fnick_name = nick
            user.Fstatus = 'normal'
            user.Fuser_pwd = self.user_passed(passwd,user.Fuid)
            user.is_employee = 0
            self.db.add(user)
            self.db.commit()
            return True,True,user

    def check_user_login_pwd(self,name, passwd):

        users = self.db.query(Users).filter(Users.Fdeleted == 0, or_(Users.Fuser_name == name, Users.Fuser_mobi == name))
        for user in users:
            if user.Fuser_pwd == self.user_passed(passwd, user.Fuid):
                return True, user
        return False, '账号或密码错误'


    def get_user_by_weixin_id(self,weixin_id):
        '''
        :todo 根据weixinid获取用户
        :param weixin_id:
        :return:
        '''
        return self.db.query(Users).filter(Users.Fdeleted==0,Users.Fweixin==weixin_id).first()

    def create_user_by_phone(self,phone,password=None):
        '''
        :todo 根据电话创建用户
        :param phone:
        :return:
        '''
        user = self.db.query(Users).filter(Users.Fdeleted==0,Users.Fuser_mobi==phone).scalar()
        if user:
            return user
        else:
            if not password:
                password=get_random_char(8)
            user = Users()
            user.Fuser_mobi = phone
            user.Fuid = self.user_uid(phone=phone)
            user.Fuser_pwd = self.user_passed(password,user.Fuid)#随机密码
            self.db.add(user)
            self.db.commit()
            return user


    def get_user_cache_msg_by_id(self, id):
        '''
        获取用户存入缓存信息
        '''
        return self.db.query(Users.Fid,Users.Fnick_name,Users.Fphoto_url,Users.Fuser_name,Users.Frole_codes).filter(Users.Fid == id, Users.Fdeleted == 0).first()

    def get_role(self, id):
        return self.db.query(Users.Frole_codes).filter(Users.Fid==id).scalar()

    # def get_permissions_by_role_code(self,code):
    #     return self.db.query(Permission.Fcode).filter(Roles.code == code, RolePermissionsDO.role_id == Roles.id,Permission.id == RolePermissionsDO.permission_id).all()

        # if users:
        #     return True,users[0]
        # else:
        #     return False,u'用户名或密码错误'
            #self.create_user(phone=phone,user_pwd=passwd)
    #     CompanyUsers()
    # Fid = Column(Integer, primary_key=True)
    # Fuid_mct = Column(String(16), nullable=False, index=True)  # 商户ID
    # Fuser_id = Column(Integer)  # 登陆人员ID
    # Fcompany_id = Column(Integer)  # 公司信息ID
    #
    # Fpermission = Column(String(256), default='')


