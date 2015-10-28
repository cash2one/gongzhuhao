# encoding:utf-8

import tornado
from common.base import BaseHandler
from utils.error_util import Error
from services.ablums.albums import ShowServices
from services.ablums.photos_service import PhotosServices
from conf.ablum_conf import _URL_ALBUM_COVER_DEFAULT
from common.permission_control import company_permission_control
photo_service = PhotosServices()

class CHandlerAlbumsList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('photos_view')
    def get(self):

        # uid_mct = self.get_current_user().get('Fid')
        # db_albums = ShowServices(self.db)
        #albums = db_albums.get_albums_list(uid_mct)
        photo_service.set_db(self.db)
        context = self.get_argument('search_text',None)
        albums = photo_service.query_album_list_by_merchant_id(self.get_current_user().get('Fmerchant_id'),search_context=context)
        _pages = self.get_page_data(albums)
        # page = self.get_argument('page',0)
        # page_url = self.get_page_url(page)
        #
        page_html = _pages.render_page_html()
        self.echo('crm/photo/album_list_py.html', {
            'albums': _pages.result,
            'page_html':page_html,
            'search_text':context,
            'default_url': _URL_ALBUM_COVER_DEFAULT})
            # self.write(str(albums))

    @tornado.web.authenticated
    def post(self):
        self.echo('crm/404.html')


class CHandlerPhotosList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('photos_view')
    def get(self, album_id):
        """原图列表"""
        uid_mct = self.get_current_user().get('Fid')
        db_photos = ShowServices(self.db)
        photos = db_photos.get_photos_list(uid_mct, album_id)
        # self.write(str(photos))
        self.echo('crm/photo/photo_list_py.html', {'photos': photos})

    @tornado.web.authenticated
    def post(self):
        self.echo('crm/404.html')


class CHandlerAdornPhotosList(BaseHandler):
    @tornado.web.authenticated
    @company_permission_control('photos_view')
    def get(self, album_id):
        """精修图列表"""
        uid_mct = self.get_current_user().get('Fid')
        db_photos = ShowServices(self.db)
        photos = db_photos.get_adorn_photos_list(uid_mct, album_id)
        # self.write(str(photos))
        self.echo('crm/photo/photo_list_py.html', {'photos': photos})

    @tornado.web.authenticated
    def post(self):
        self.echo('crm/404.html')
