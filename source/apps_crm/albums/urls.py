# encoding:utf-8

from albums_handler import CHandlerAlbumsList, \
    CHandlerPhotosList, CHandlerAdornPhotosList
from photos_handler import PhotoUploadHandler,PhotosDeleteHandler,MerchantProductUploadHandler


handlers = [
    (r'/merchant/albums/', CHandlerAlbumsList),
    (r'/merchant/photos/([\d]{1,9})/', CHandlerPhotosList),
    (r'/merchant/photos/adorn/([\d]{1,9})/', CHandlerAdornPhotosList),
    (r'/merchant/album/photo/upload/([\d]*)/([\w\W]*)', PhotoUploadHandler),  # 图片上传

    (r'/merchant/photos/delete/([\d]*)', PhotosDeleteHandler),  # 图片上传

    (r'/merchant/product/upload/([\w\W]*)', MerchantProductUploadHandler),  #商家产品图片上传


]
