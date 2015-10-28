# -*- coding: utf-8 -*-

from sqlalchemy import Integer, Column, String, DateTime, Boolean
from models.base_do import Base
from sqlalchemy.sql.functions import now


__author__ = 'fangshi'

class Country(Base):
    """
        国家信息表
    """
    __tablename__ = 't_country'

    Fid = Column(Integer, primary_key=True)
    Fcode = Column(Integer)
    Fname_chinese = Column(String(128))
    Fname_english = Column(String(128))


    def to_dict(self):
        dic = {}
        dic["id"] = self.Fid
        dic["code"] = self.Fkey_name
        dic["name_chinese"] = self.Fname_chinese
        dic["name_english"] = self.Fname_english
        return dic

class Province(Base):
    """
        省份信息
    """
    __tablename__ = 't_province'

    Fid = Column(Integer, primary_key=True)
    Fprovince_id = Column(Integer)
    Fprovince_name = Column(String(128))                 #省份名称
    Fgmt_created = Column(DateTime,default=now())
    Fgmt_modified = Column(DateTime,default=now())
    Fdeleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["Fprovince_id"] = self.Fprovince_id
        dic["Fprovince_name"] = self.Fprovince_name
        return dic


class City(Base):
    """
    城市信息
    """
    __tablename__ = 't_city'

    Fid = Column(Integer, primary_key=True)
    Fcity_id = Column(Integer)
    Fcity_name = Column(String(128))                 #城市名称
    #zip_code = Column(String(10))
    Ffather = Column(Integer)

    Fgmt_created = Column(DateTime,default=now())
    Fgmt_modified = Column(DateTime,default=now())
    Fdeleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["Fprovince_id"] = self.Ffather
        dic["Fcity_id"] = self.Fcity_id
        dic["Fcity_name"] = self.Fcity_name
        return dic


class Area(Base):
    """
        区域信息
    """
    __tablename__ = 't_area'

    Fid = Column(Integer, primary_key=True)
    Farea_id = Column(Integer)
    Farea_name = Column(String(128))                 #区域名称
    Ffather = Column(Integer)
    Fgmt_created = Column(DateTime,default=now())
    Fgmt_modified = Column(DateTime,default=now())
    Fdeleted = Column(Boolean,default=0)

    def to_dict(self):
        dic = {}
        dic["Farea_id"] = self.Farea_id
        dic["Fcity_id"] = self.Ffather
        dic["Farea_name"] = self.Farea_name
        return dic

# class UserLocation(Base):
#     """
#         用户位置信息
#     """
#     __tablename__="user_location"
#
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     area_id = Column(Integer,nullable=True)
#     city_id = Column(Integer,nullable=True)
#     province_id = Column(Integer,nullable=True)
#
#     gmt_created = Column(DateTime,default=now())
#     gmt_modified = Column(DateTime,default=now())
#     deleted = Column(Boolean,default=0)
#
