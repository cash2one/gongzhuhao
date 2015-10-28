#encoding:utf-8
__author__ = 'frank'

from common.base import AdminBaseHandler
from utils.datetime_util import datetime_format
from utils.upload_utile import upload_to_oss
from tornado.options import options
from services.music.music_service import MusicServices
import ujson
from models.share_do import ShareMusic

music_service = MusicServices()

class UploadMusicHandler(AdminBaseHandler):
    def get(self):
        self.echo('ops/music/music.html')

    def post(self):
        rsg = {
            'stat':'error',
            'msg':''
        }
        self.get_paras_dict()
        data = {}
        try:
            file_prex = 'music/'+datetime_format(format="%Y%m%d%H%M")
            is_ok,filenames = upload_to_oss(self,options.MEDIA_BUCKET,param_name='background_music',file_type=None,file_prex=file_prex)
            if is_ok:
                request_url = options.MEDIA_DOMAIN+'/'+filenames[0].get('full_name')
        except Exception,e:
            data['error']=1
            data['message']=e.message
            data['url']=''
            raise


        music_service.set_db(self.db)
        data['music_name'] = self.qdict.get('music_name')
        data['request_url'] = request_url
        share_music = music_service.create_share_music(**data)
        if share_music:
            rsg['stat'] = 'success'
            self.write(ujson.dumps(rsg))
        else:
            self.write(ujson.dumps(rsg))

class MusicListHandler(AdminBaseHandler):
    def get(self):
        self.get_paras_dict()
        music_service.set_db(self.db)
        query = music_service.query_share_music(**self.qdict)
        page_data = self.get_page_data(query)
        self.echo('ops/music/music_list.html',{'page_data':page_data,'page_html':page_data.render_page_html()})

class MusicDeleteHandler(AdminBaseHandler):
    def get(self,music_id):
        rsg = {
            'stat':'error',
            'msg':''
        }
        music_service.set_db(self.db)
        try:
            music_service.delete_music(music_id)
        except Exception,e:
            rsg['msg'] = e.message
            raise
        rsg['stat'] = 'success'
        self.write(ujson.dumps(rsg))













