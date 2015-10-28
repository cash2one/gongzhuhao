#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from conf.ablum_conf import _URL_ALBUM_COVER_DEFAULT
from services.ablums.photos_service import PhotosServices

photo_service = PhotosServices()

class AlbumsListHandler(AdminBaseHandler):
    def get(self,merchant_id):
        self.get_paras_dict()
        photo_service.set_db(self.db) #Don't forget push the code after jinkuan commit the code, when the system reject jinkuan ,please pull the project from the old version
        query = photo_service.query_albums(merchant_id,**self.qdict)
        page_data = self.get_page_data3(query)
        self.echo('ops/albums/albums_list_all.html',{'page_data':page_data,'page_html':page_data.render_page_html(),
                                                     'default_url':_URL_ALBUM_COVER_DEFAULT})




