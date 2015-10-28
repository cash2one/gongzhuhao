__author__ = 'frank'

from apps_admin.albums.photos_handler import QueryPhotosHandler,DeletePhotoHandler
from apps_admin.albums.albums_handler import AlbumsListHandler

handlers = [
    (r'/gzh/ops/company/albums/list/([\w\W]*)',AlbumsListHandler),
    (r'/gzh/ops/photo/list/([\w\W]*)/([\w\W]*)',QueryPhotosHandler),
    (r'/gzh/ops/delete/photo/',DeletePhotoHandler),

]
