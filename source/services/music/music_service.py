#encoding:utf-8
__author__ = 'frank'

from services.base_services import BaseService
from models.share_do import ShareMusic
from utils.upload_utile import delete_from_oss
from tornado.options import options


class MusicServices(BaseService):
    def create_share_music(self,**kwargs):
        '''
        todo:新增一首背景歌曲
        :param kwargs:
        :return:
        '''
        share_music = ShareMusic()
        share_music.Fmusic_name = kwargs.get('music_name')
        share_music.Fmusic_url = kwargs.get('request_url')
        self.db.add(share_music)
        self.db.commit()
        return share_music

    def query_share_music(self,**kwargs):
        '''
        todo:查询背景歌曲
        :param kwargs:
        :return:
        '''
        query = self.db.query(ShareMusic).filter(ShareMusic.Fdeleted == 0)
        if kwargs.get('start_date',''):
            query = query.filter(ShareMusic.Fcreate_time > kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(ShareMusic.Fcreate_time < kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('music_name',''):
            query = query.filter(ShareMusic.Fmusic_name.like('%'+kwargs.get('music_name')+'%'))
        return query

    def delete_music(self,music_id):
        '''
        todo:删除背景歌曲
        :param music_id: 歌曲id
        :return:
        '''
        query = self.db.query(ShareMusic).filter(ShareMusic.Fdeleted == 0,ShareMusic.Fid == music_id)
        filename = query.scalar().Fmusic_url[34:]
        data = {}
        data['Fdeleted'] = 1
        query.update(data)
        self.db.commit()
        delete_from_oss(options.MEDIA_BUCKET,filename)



