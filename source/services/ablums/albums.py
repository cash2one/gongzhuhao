# encoding:utf-8
from models.order_do import Orders
from models.album_do import Albums, Photos, AdornPhotos
from utils.error_util import Error
from sqlalchemy import func


class ShowServices(object):
    def __init__(self, db):
        self.db = db

    def get_albums_list(self, uid_mct):
        """获取相册列表"""
        fetch_entities = (
            Orders.Fid.label('Forder_id'),
            Orders.Fcreate_time,
            Orders.Fuser_name,
            Orders.Fuser_mobi,
            Albums.Fid.label('Falbum_id'),
            Albums.Furl_pic_cover,
            Albums.Fablum_name,
            Albums.Ftotal
            )
        res_q = self.db.query(*fetch_entities).filter(
            Orders.Fuid_mct == uid_mct,
            Orders.Fid == Albums.Forder_id,
            Orders.Fdeleted == 0,
            Albums.Fdeleted == 0).all()

        results = [i._asdict() for i in res_q]
        for idx, item in enumerate(results):
            pic_num = self.db.query(func.count('*')).filter(
                Photos.Falbum_id == item['Falbum_id'],
                Photos.Fdeleted == 0
                ).scalar()
            results[idx]["pic_num"] = pic_num
        return results

    def get_photos_list(self, uid_mct, album_id):
        """获取照片（原图）列表"""
        res_qry = self.db.query(Albums.Fid).filter(
            Albums.Fuid_mct == uid_mct,
            Albums.Fid == album_id,
            Albums.Fdeleted == 0).scalar()
        if not res_qry:
            raise Error(300, "user check error!")

        result = self.db.query(Photos).filter(
            Photos.Falbum_id == album_id,
            Photos.Fdeleted == 0).all()
        return result

    def get_adorn_photos_list(self, uid_mct, album_id):
        """获取照片（精修图）列表"""
        res_qry = self.db.query(Albums.Fid).filter(
            Albums.Fuid_mct == uid_mct,
            Albums.Fid == album_id,
            Albums.Fdeleted == 0).scalar()
        if not res_qry:
            raise Error(300, "user check error!")

        result = self.db.query(AdornPhotos).filter(
            AdornPhotos.Falbum_id == album_id,
            AdornPhotos.Fdeleted == 0).all()
        return result























