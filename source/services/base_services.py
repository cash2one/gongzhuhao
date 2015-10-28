# from myshop.services.db_manager import DBManager


class BaseService(object):
    def __init__(self, db=None):
       self.db = db

    def set_db(self, db):
        self.db = db

