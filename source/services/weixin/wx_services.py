# encoding:utf-8

__author__ = 'sunlifeng'

from sqlalchemy import func, or_
from models.app_do import WeixinMenu

from utils.date_util import yyyydddddatetime

class WxService(object):
    def __init__(self, db=None):
        self.db = db

    def set_db(self, db):
        self.db = db

    def query_menus(self):
        query = self.db.query(WeixinMenu).filter().all()
        return query

    def query_by_code(self, code):
        query = self.db.query(WeixinMenu).filter(WeixinMenu.code == code).scalar()
        return query

    def query_name_by_code(self, code):
        query = self.db.query(WeixinMenu).filter(WeixinMenu.code == code).scalar()
        return query.name