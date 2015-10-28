# coding=utf-8
from sqlalchemy import and_
from models.location_do import Country, Province, City, Area
from services.base_services import BaseService


class CountryService(BaseService):
    """ 国家列表 """

    def get_country_list(self):
        """
        获取所有属性列表
        """
        # query=self.db.query.option().offset(10).limit(100).all()
        return self.db.query(Country).filter()


class ProvinceService(BaseService):
    """ 属性配置服务 """
    def __init__(self, db):
        self.db = db

    def get_province_list(self):
        """
        获取所有属性列表
        """
        return self.db.query(Province).filter(Province.Fdeleted == 0)

    def get_province_list_by_id(self,id):
        return self.db.query(Province).filter(Province.Fdeleted==0,Province.Fid==id).first()


class CityService(BaseService):
    """
    属性配置服务
    """

    def __init__(self, db):
        self.db = db

    def get_city_list_length(self):
        return  self.db.query(City).count()

    def get_city_list(self):
        """
        获取所有属性列表
        """
        query = self.db.query(City, Province.Fprovince_name).filter(
            Province.Fid == City.Ffather)  # offset(offset).limit(limit)
        return query

    def get_city_list_by_province_id(self, province=''):
        """
        获取所有属性列表,包含删除掉的商品
        """
        if province:
            return self.db.query(
                and_(City.Ffather == province, City.Fdeleted == 0)).all()
        return []


class AreaService(BaseService):
    """
    属性配置服务
    """

    def get_area_list(self):
        """
        获取所有属性列表
        """

        return self.db.query(Area).filter()
    # Area.Fdeleted == 0

    def get_city_list_by_province_id(self, city_id=''):
        """
        获取所有属性列表,包含删除掉的商品
        """
        if city_id:
            return self.db.query(and_(Area.father == city_id, Area.Fdeleted == 0)).all()
        return []


class LocationServices(BaseService):

    def get_location_name_list(self, type, father_id=0):
        '''
        :param type: 查询的地区登记  province,city,area
        :param father_id:
        :return: 地址id和名称
        '''
        if type == 'city':
            return self.db.query(City.Fid, City.Fcity_name).filter(
                City.Ffather == father_id, City.Fdeleted==0)
        if type == 'area':
            return self.db.query(Area.Fid, Area.Farea_name).filter(
                Area.Ffather == father_id, Area.Fdeleted==0)
        if type == 'province':
            return self.db.query(Province.Fid, Province.Fprovince_name).filter(
                Province.Fdeleted==0)

    def get_city_area_list(self, province_id=0, city_id=0):
        '''
        :param type: 查询的地区登记  province,city,area
        :param father_id:
        :return: 地址id和名称
        '''
        city = self.db.query(City.Fid, City.Fcity_name).filter(
            City.Ffather == province_id,
            City.Fdeleted == 0)
        area = self.db.query(Area.Fid, Area.Farea_name).filter(
            Area.Ffather == (city_id if city_id else city.first().Fid if city.first() else 0),
            Area.Fdeleted == 0)
        return city, area

    def get_location_name_by_id(self, type, id):
        '''
         根据省市id查询省市名称
         :param type: 查询的地区登记  province,city,area
         :param father_id:
          :return: 地址id和名称
        '''
        if type == 'city':
            return self.db.query(City.Fcity_name).filter(City.Fid == id, City.Fdeleted==0).scalar()
        if type == 'area':
            return self.db.query(Area.Farea_name).filter(Area.Fid == id, Area.Fdeleted==0).scalar()
        if type == 'province':
            return self.db.query(Province.Fprovince_name).filter(Province.Fid==id , Province.Fdeleted==0).scalar()
