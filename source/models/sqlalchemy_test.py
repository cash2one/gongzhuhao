#encoding:utf-8
__author__ = 'binpo'
from models.advertise_do import *
from models.app_do import *

from models.banner_do import *
from models.location_do import *
from models.decoratehelp_do import *
from models.user_do import *
from models.config_do import *

from models.decorate_do import *

from sqlalchemy import create_engine, MetaData,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from models.base_do import Base


#链接数据库
mysql_engine = create_engine('mysql://root:111111@192.168.88.200:3307/decorate?charset=utf8',encoding = "utf-8",echo =True)
# Base.metadata.create_all(mysql_engine)  #建表
Session = sessionmaker(bind=mysql_engine)
session = Session()


# dic={'user_name':'qiuyan.zwp'}
# Users.set_attrs(session,1,dic)
# Users.set_attrs(session,1,user_name='qiuyan')
#
# exit(0)
user = session.query(Users).filter(Users.id==1).scalar()
if user:
    print True
else:
    print False
exit(0)
users = session.query(Users).filter(Users.role_codes.like('%merchant%'))
for u in users:
    print u.id
class TestMessage(object):

    def __init__(self):
        self.session = session

    def add_tag(self):
        tag = Tags()
        tag.tag_type = 3
        tag.tag_name = 'hello'
        tag.gmt_created = now()
        tag.gmt_modified = now()
        tag.deleted = 0
        self.session.add(tag)
        self.session.commit()
        message.pub('tag_dela',tag)
    def get_tag_Tags(self,tag):
        print 'signal message ------------------- :',tag.id,tag.tag_name


user = session.query(Users).filter(Users.id.in_([1,2])).scalar()
print type(user)
if user:
    print type(user)
    print user.id
print '-----------------------分隔符－－－－－－－－－－－－－－－－－'
user = session.query(Users).filter().first()
if user:
    print user.nick
exit(0)
import message
message.sub('tag_dela',TestMessage().get_tag_Tags)


from sqlalchemy import func, or_, not_,and_

#修改obj方法1
def update_example1():
    """
        先查询  再修改
        select XX from Users ....
        update xxx from Users where id=xx

    """
    users = session.query(Users).filter(Users.id==20).scalar()
    users.nick='qiuyan'
    session.add(users)
    session.commit()

    session.query(Users).filter(Users.id==20).update({'nick':'qiuyan'})
    session.commit()

#修改obj方法2
def update_example2():
    '''
        执行一条语句
        update xx from Users where id = xx
    '''
    session.query(Users).filter(Users.id==20).update({'nick':'qiuyan'})
    session.commit()
# 用方法2不用方法一


if __name__ == "__main__":
    #TestMessage().add_tag()
    #   tag = Tags()
#     tag.ag_type = 'hello'
#     tag_name = 'hello'
#     tag.gmt_created = now()
#     tag.gmt_modified = now()
#     tag.deleted = 0
#
#     session.add(tag)
#     def u(**kargs):
#         query = session.query(Tags).filter(Tags.id==1)
#         print kargs
#         query.update(kargs)
#         print query
#         session.commit()
#     u(tag_type=2,tag_name=u'hello 日本人')
#
    query = session.query(Tags).filter(Tags.id==1)#.scalar()
    #print dir(query)
    obj1 = query.scalar()

    print type(obj1)
    obj2 = query.values('tag_type','tag_name')#.scalar()

    print '------------------------end-----------------'
    for o in session.query(Tags.id): #需要什么字段查什么字段
        print o
        print o.id
    print '------------------------end-----------------'

    print type(obj2)
    for o in obj2:
        print type(o)
        print o

    query = session.query(Tags)
    print query # 显示SQL 语句
    print query.statement # 同上
    for Tags in query: # 遍历时查询
        print Tags.tag_name

    print query.all() # 返回的是一个类似列表的对象
    print query.first().tag_name # 记录不存在时，first() 会返回 None    ******
    print query.one().tag_name # 不存在，或有多行记录时会抛出异常        ******


    print query.get(2).tag_name # 以主键获取 等效 query.get(Users.id=2)
    print query.filter('id = 2').first().tag_name # 支持字符串

    print '<<<--------start---------->>'
    obj = query.filter('id=1').first() # 支持字符串
    print type(obj)
    print '---------------------------team-----------------------------'
    obj = query.filter(Tags.id == 2).first()
    print dir(obj)
    print '<<<---------end----------->>'


    query2 = session.query(Tags.tag_name)
    print query2.all() # 每行是个元组
    print query2.limit(1).all() # 最多返回 1 条记录
    print query2.offset(1).all() # 从第 2 条记录开始返回

    """排序   order by  desc"""
    print query2.order_by(Tags.tag_name).all()
    print query2.order_by('tag_name').all()
    print query2.order_by(Tags.tag_name.desc()).all()
    print query2.order_by('tag_name desc').all()
    print session.query(Tags.id).order_by(Tags.tag_name.desc(), Tags.id).all()


    print query2.filter(Tags.id == 1).scalar() # 如果有记录，返回第一条记录的第一个元素
    print session.query('id').select_from(Tags).filter('id = 1').scalar()
    print query2.filter(Tags.id > 1, Tags.tag_name != 'a').scalar() # and
    query3 = query2.filter(Tags.id > 1) # 多次拼接的 filter 也是 and
    query3 = query3.filter(Tags.tag_name != 'a')

    print query3.scalar()

    """or 查询"""
    print query2.filter(or_(Tags.id == 1, Tags.id == 2)).all() # or
    print query2.filter(Tags.id.in_((1, 2))).all() # in

    """null 查询"""
    query4 = session.query(Tags.id)
    print query4.filter(Tags.tag_name == None).scalar()
    print query4.filter('tag_name is null').scalar()
    print query4.filter(not_(Tags.tag_name == None)).all() # not
    print query4.filter(Tags.tag_name != None).all()


    print query4.count()
    print session.query(func.count('*')).select_from(Tags).scalar()
    print session.query(func.count('1')).select_from(Tags).scalar()
    print session.query(func.count(Tags.id)).scalar()
    print session.query(func.count('*')).filter(Tags.id > 0).scalar() # filter() 中包含 Tags，因此不需要指定表
    print session.query(func.count('*')).filter(Tags.tag_name == 'a').limit(1).scalar() == 1 # 可以用 limit() 限制 count() 的返回数
    print session.query(func.sum(Tags.id)).scalar()
    print session.query(func.now()).scalar() # func 后可以跟任意函数名，只要该数据库支持
    print session.query(func.current_timestamp()).scalar()
    print session.query(func.md5(Tags.tag_name)).filter(Tags.id == 1).scalar()

    '''like 查询'''
    session.query(Tags).filter(Tags.tag_name.like('%hello%'))

    '''in 查询'''
    session.query(Tags).filter(Tags.name.in_(['hello',  'hello',  'hello']))

    '''update'''
    query.filter(Tags.id == 1).update({Tags.tag_name: 'c'})
    query.filter(Tags.id == 1).update({Tags.count: Tags.count+1}, synchronize_session=False)
    Tags = query.get(1)
    print Tags.tag_name

    '''事物 '''
    Tags.tag_name = 'd'
    session.flush() # 写数据库，但并不提交
    print query.get(1).tag_name

    session.delete(Tags)
    session.flush()
    print query.get(1)

    session.rollback()
    print query.get(1).tag_name
    query.filter(Tags.id == 1).delete()
    session.commit()
    print query.get(1)


    #简单查询
    print session.query(Users).all()
    print session.query(Users.user_name, Users.email).all()
    print(session.query(Users, Users.user_name).all())

    #带条件查询
    print session.query(Users).filter_by(user_name='qiuyan').all()
    print session.query(Users).filter(Users.user_name == "qiuyan").all()
    print session.query(Users).filter(Users.qiuyan.like("qiuyan%")).all()

    #多条件查询
    print session.query(Users).filter(and_(Users.user_name.like("qiuyan%"), Users.email.like("binpo%"))).all()
    print session.query(Users).filter(or_(Users.user_name.like("qiuyan%"), Users.user_pwd != None)).all()

    #sql过滤    where id >1
    print session.query(Users).filter("id>:id").params(id=1).all()

    #关联查询
    print session.query(Users, UserRoles).filter(Users.id == UserRoles.user_id).all()
    print session.query(Users).join(Users.addresses).all()
    print session.query(Users).outerjoin(Users.addresses).all()

    #聚合查询
    print(session.query(Users.name, func.count('*').label("Users_count")).group_by(Users.name).all())
    print(session.query(Users.name, func.sum(Users.id).label("Users_id_sum")).group_by(Users.name).all())

    #子查询
    stmt = session.query(Address.Users_id, func.count('*').label("address_count")).group_by(Address.Users_id).subquery()
    print(session.query(Users, stmt.c.address_count).outerjoin((stmt, Users.id == stmt.c.Users_id)).order_by(Users.id).all())

    #exists
    print(session.query(Users).filter(exists().where(Address.Users_id == Users.id)))
    print(session.query(Users).filter(Users.addresses.any()))