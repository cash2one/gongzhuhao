#encoding:utf-8

__author__ = 'binpo'

import sys
import ujson
import base64
import tornado
from common.base import BaseApiHandler as BaseHandler
from utils.upload_utile import upload_to_oss
from tornado.options import options
from tornado.web import HTTPError

from utils.datetime_util import datetime_format

Default_Album_Name = 'DefaultAlbum'   #默认相册文件夹的名称

try:
    import Image
    import ImageFile
except:
    from PIL import Image
    from PIL import ImageFile



IMAGE_TYPES={'image/png':'.png',
    'image/jpg':'.jpg',
    'image/jpeg':'.jpg',
    'image/pjpeg':'.jpg',
    'image/gif':'.gif',
    'image/bmp':'.bmp',
    'image/x-png':'.png'
}

FILE_FORMAT={'image/gif':'GIF', 'image/jpeg':'JPEG', 'image/pjpeg':'PJEGP', 'image/bmp':'BMP', 'image/png':'PNG', 'image/x-png':'PNG'}

def img_compression(img_size=0,img_type=''):
    '''
        jpg格式压缩
        原图:876K
        80q压缩:134
        43q压缩:70
        30q压缩:55
    '''
    paras=''
    img_size = img_size/1000
    if img_size>4000:
        return '@50q_0r.jpg'
    elif img_size>3000:
        return  '@60q_0r.jpg'
    elif img_size>2000:
        return  '@65q_0r.jpg'
    elif  img_size>1000:
        return  '@70q_0r.jpg'
    elif  img_size>500:
        return  '@90q_0r.jpg'
    elif img_size<300:
        return ''#'@100q_0r.jpg'
    else:
        return '@80q_0r.jpg'

def img_qulities_compression(img_size=0,img_type=''):
    '''
        质量压缩率处理
    '''
    img_size = img_size/1000
    if img_size>4000:
        return '50'
    elif img_size>3000:
        return  '60'
    elif img_size>2000:
        return  '65'
    elif  img_size>1000:
        return  '70'
    elif  img_size>500:
        return  '90'
    elif img_size<300:
        return '100'#'@100q_0r.jpg'
    else:
        return '80'


class PhotoQAUploadHandler(BaseHandler):
    """
        问答相片上传
    """
    @tornado.web.authenticated
    def post(self):
        """
        :todo 上传图片
        """

        date_format_prefix = datetime_format(format='%Y%m%d')
        try:

            rsp={'files':[],'stat':'err','msg':''}

            file_prex = '/'.join(['topics',str(self.get_current_user().get('Fid')),date_format_prefix])

            is_ok,filenames = upload_to_oss(self,options.IMG_BUCKET,param_name='files',file_type='img',file_prex=file_prex,max_size=3)

            if is_ok:
                for f in filenames:
                    rsp['files'].append(
                            {
                            "name": f.get('file_name'),
                            "size": f.get('size'),
                            "type": f.get('content_type'),
                            "url": options.IMG_DOMAIN+'/'+f.get('full_name')+img_compression(f.get('size')),
                            "full_name":f.get('full_name'),
                        }
                    )
                rsp['stat'] = 'ok'

                rsp['files'][0]['id'] = '0'
            else:
                rsp['stat'] = 'err'
                rsp['msg'] = filenames
        except Exception,e:
            pass
        return self.write(ujson.dumps(rsp))

class PhotoTopicUploadHandler(BaseHandler):
    """
        话题富文本图片上传
    """
    @tornado.web.authenticated

    def post(self):
        """
        :todo 上传图片
        """

        date_format_prefix = datetime_format(format='%Y%m%d')
        try:

            rsp={'filelink':'','stat':'err','msg':''}

            file_prex = '/'.join(['topics',str(self.get_current_user().get('Fid')),date_format_prefix])

            is_ok,filenames = upload_to_oss(self,options.IMG_BUCKET,param_name='file',file_type='img',file_prex=file_prex,max_size=3)

            if is_ok:
                for f in filenames:
                    rsp['filelink'] = options.IMG_DOMAIN+'/'+f.get('full_name')+img_compression(f.get('size'))
                rsp['stat'] = 'ok'
            else:
                rsp['stat'] = 'err'
                rsp['msg'] = filenames
        except Exception,e:
            pass
        print '返回图片结果：',rsp
        return self.write(ujson.dumps(rsp))