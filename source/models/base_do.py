#encoding:utf-8

__author__ = 'zhaowenpeng'


from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
from sqlalchemy.sql.functions import now
from sqlalchemy.orm.interfaces import MapperExtension
from utils.date_util import yyyydddddatetime


class ModelMixin(object):

    @classmethod
    def get_by_id(cls, session, id, columns=None, lock_mode=None):
        if hasattr(cls, 'id'):
            scalar = False
            if columns:
                if isinstance(columns, (tuple, list)):
                    query = session.query(*columns)
                else:
                    scalar = True
                    query = session.query(columns)
            else:
                query = session.query(cls)
            if lock_mode:
                query = query.with_lockmode(lock_mode)
            query = query.filter(cls.id == id)
            if scalar:
                return query.scalar()
            return query.first()
        return None

    @classmethod
    def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
        if columns:
            if isinstance(columns, (tuple, list)):
                query = session.query(*columns)
            else:
                query = session.query(columns)
                if isinstance(columns, str):
                    query = query.select_from(cls)
        else:
            if hasattr(cls, 'deleted'):
                query = session.query(cls).filter(cls.deleted==0)
            else:
                query = session.query(cls)
        if order_by is not None:
            if isinstance(order_by, (tuple, list)):
                query = query.order_by(*order_by)
            else:
                query = query.order_by(order_by)
        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.all()


    @classmethod
    def count_all(cls, session, lock_mode=None):
        query = session.query(func.count('*')).select_from(cls)
        if lock_mode:
            query = query.with_lockmode(lock_mode)
        return query.scalar()


    @classmethod
    def exist(cls,session,**kargs):

        query = session.query(func.count('*')).select_from(cls)
        for key in kargs.keys():
            key=kargs.get(key)
            if hasattr(cls, key):
                query = query.filter_by()
        # if hasattr(cls, 'id'):
        #    .filter(cls.id == id)
            # if lock_mode:
            #     query = query.with_lockmode(lock_mode)
        return query.scalar() > 0
        #return False

    @classmethod
    def set_attr(cls, session, id, attr, value):
        if hasattr(cls, 'Fid'):
            session.query(cls).filter(cls.Fid == id).update({
                attr: value,
                'Fmodify_time':yyyydddddatetime()
            })
            session.commit()


    @classmethod
    def set_attrs(cls, session, id, **attrs):
        if hasattr(cls, 'Fid'):
            attrs['Fmodify_time'] = yyyydddddatetime()
            session.query(cls).filter(cls.Fid == id).update(attrs)
            session.commit()

    @classmethod
    def set_attrs2(cls, session,id,order_id, **attrs):
        if hasattr(cls, 'Fid'):
            attrs['Fmodify_time'] = yyyydddddatetime()
            session.query(cls).filter(cls.Fid == id,cls.Forder_id == order_id).update(attrs)
            session.commit()


Base = declarative_base(cls=ModelMixin)

# class Base(BaseModel):
#     __abstract__ = True
#

class DataUpdateExtension(MapperExtension):

    def before_update(self, mapper, connection,instance):
        print 'before update obj--------------------'
        if hasattr(instance,'gmt_modified'):
            instance.gmt_modified = now()


class ChoiceType(types.TypeDecorator):

    impl = types.String

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(ChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]

# class ModelMixin(object):
#     @classmethod
#     def get_by_id(cls, session, id, columns=None, lock_mode=None):
#         if hasattr(cls, 'id'):
#             scalar = False
#             if columns:
#                 if isinstance(columns, (tuple, list)):
#                     query = session.query(*columns)
#                 else:
#                     scalar = True
#                     query = session.query(columns)
#             else:
#                 query = session.query(cls)
#             if lock_mode:
#                 query = query.with_lockmode(lock_mode)
#             query = query.filter(cls.id == id)
#             if scalar:
#                 return query.scalar()
#             return query.first()
#         return None
#     BaseModel.get_by_id = get_by_id
#
#     @classmethod
#     def get_all(cls, session, columns=None, offset=None, limit=None, order_by=None, lock_mode=None):
#         if columns:
#             if isinstance(columns, (tuple, list)):
#                 query = session.query(*columns)
#             else:
#                 query = session.query(columns)
#                 if isinstance(columns, str):
#                     query = query.select_from(cls)
#         else:
#             query = session.query(cls)
#         if order_by is not None:
#             if isinstance(order_by, (tuple, list)):
#                 query = query.order_by(*order_by)
#             else:
#                 query = query.order_by(order_by)
#         if offset:
#             query = query.offset(offset)
#         if limit:
#             query = query.limit(limit)
#         if lock_mode:
#             query = query.with_lockmode(lock_mode)
#         return query.all()
#     BaseModel.get_all = get_all
#
#     @classmethod
#     def count_all(cls, session, lock_mode=None):
#         query = session.query(func.count('*')).select_from(cls)
#         if lock_mode:
#             query = query.with_lockmode(lock_mode)
#         return query.scalar()
#     BaseModel.count_all = count_all
#
#     @classmethod
#     def exist(cls, session, id, lock_mode=None):
#         if hasattr(cls, 'id'):
#             query = session.query(func.count('*')).select_from(cls).filter(cls.id == id)
#             if lock_mode:
#                 query = query.with_lockmode(lock_mode)
#             return query.scalar() > 0
#         return False
#     BaseModel.exist = exist
#
#     @classmethod
#     def set_attr(cls, session, id, attr, value):
#         if hasattr(cls, 'id'):
#             session.query(cls).filter(cls.id == id).update({
#                 attr: value
#             })
#             session.commit()
#     BaseModel.set_attr = set_attr
#
#     @classmethod
#     def set_attrs(cls, session, id, attrs):
#         if hasattr(cls, 'id'):
#             session.query(cls).filter(cls.id == id).update(attrs)
#             session.commit()
#     BaseModel.set_attrs = set_attrs



