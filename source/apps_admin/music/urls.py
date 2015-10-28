#encoding:utf-8
__author__ = 'frank'

from apps_admin.music.music_handler import UploadMusicHandler,MusicListHandler,MusicDeleteHandler

handlers = [
    (r'/gzh/ops/upload/music/',UploadMusicHandler),
    (r'/gzh/ops/music/list/',MusicListHandler),
    (r'/gzh/ops/delete/music/([\w\W]*)',MusicDeleteHandler),
]
