#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from services.ablums.photos_service import PhotosServices
from models.order_do import Orders
from models.album_do import Albums
from conf.ablum_conf import _ABLUM_STATUS
from utils.error_util import Error
import ujson

photo_service = PhotosServices()

class QueryPhotosHandler(AdminBaseHandler):
    def get(self,album_id,merchant_id):
        try:
            photo_service.set_db(self.db)
            query = photo_service.query_photos(album_id,merchant_id)
            page_data = self.get_page_data(query)
            order_id = self.db.query(Albums.Forder_id).filter(Albums.Fid == album_id).scalar()
            context = {'page_data':page_data,'page_html':page_data.render_page_html(),
                       'order_id':order_id,'album_id':album_id,'album_status':_ABLUM_STATUS,'merchant_id':merchant_id,'album_id':album_id}
            self.echo('ops/albums/photos_list.html',context)
        except Exception,e:
            raise
    def post(self,album_id,merchant_id):
        self.get(album_id,merchant_id)
        # self.get_paras_dict()
        # import pdb
        # pdb.set_trace()
        # print '------------------------'
        # print merchant_id
        # print self.qdict.get('img_id')
        # print self.qdict.get('_xsrf')
        # #self.redirect('/gzh/ops/delete/photo/'+merchant_id+self.qdict.get('img_id'))

    def get_order_by_id(self,order_id):
        return self.db.query(Orders).filter(Orders.Fdeleted == 0,Orders.Fid == order_id).scalar()

    def get_album_by_id(self,album_id):
        return self.db.query(Albums).filter(Albums.Fdeleted == 0,Albums.Fid == album_id).scalar()

class DeletePhotoHandler(AdminBaseHandler):
    def get(self):
        rsg = {
            'stat':'error',
            'msg':''
        }
        self.get_paras_dict()
        # import pdb
        # pdb.set_trace()
        photo_service.set_db(self.db)
        try:
            for photo_id in self.qdict.get('img_id').split(','):
                photo_service.delete_photo_by_photo_id(merchant_id=self.qdict.get('merchant_id'),photo_id=int(photo_id))
        except Exception,e:
            print e
            if self.settings.get('debug'):
                self.write(str(e))
                raise
            err_msg = "add failed"
            self.write(Error(2, err_msg).__dict__)
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))


