#encoding:utf-8
__author__ = 'frank'

from services.base_services import BaseService
from models.location_do import Province,City,Area


class LocationServices2(BaseService):

    def get_location_name_list(self,type):
        if type == 'province':
            query = self.db.query(Province).filter(Province.Fdeleted == 0)
        if type == 'city':
            query = self.db.query(City).filter(City.Fdeleted == 0)
        if type == 'area':
            query = self.db.query(Area).filter(Area.Fdeleted == 0)
        return query

    def get_city_by_province_id(self,province_id):
        return self.db.query(City).filter(City.Ffather == province_id,Area.Fdeleted == 0)

    def get_area_by_city_id(self,city_id):
        return self.db.query(Area).filter(Area.Ffather == city_id,Area.Fdeleted == 0)
