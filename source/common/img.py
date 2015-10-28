#encoding:utf-8
__author__ = 'zhaowenpeng'

import tornado.ioloop
import tornado.web
import random
import string
import os
import json
import time
from utils.upload_utile import upload_to_oss
from setting import IMG_BUCKET
from tornado.options import options

from base import BaseHandler


def img_compression(img_size=0, img_type=''):
    '''
        jpg格式压缩
        原图:876K
        80q压缩:134
        43q压缩:70
        30q压缩:55
    '''
    img_size = img_size/1000
    if img_size > 4000:
        return '@50q_0r.jpg'
    elif img_size > 3000:
        return '@60q_0r.jpg'
    elif img_size > 2000:
        return '@65q_0r.jpg'
    elif img_size > 1000:
        return '@70q_0r.jpg'
    elif img_size > 500:
        return '@90q_0r.jpg'
    elif img_size < 300:
        return ''  # '@100q_0r.jpg'
    else:
        return '@80q_0r.jpg'


def upload_img_localhost(app_name,file_metas):
    for meta in file_metas:
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        filename=meta['filename']
        if not os.path.exists('static/'+app_name):
            os.makedirs('static/'+app_name)
        filepath=os.path.join('static/'+app_name,salt+filename)
        with open(filepath,'wb') as up:             #有些文件需要已二进制的形式存储，实际中可以更改
            up.write(meta['body'])
        request_url = os.path.join('/static/'+app_name,salt+filename)
        return request_url

class ImgHandler(BaseHandler):
    """
        单图上传
    """
    #@tornado.apps_crm.authenticated
    def post(self,code):
        app_name="company_logos"
        file_metas=self.request.files.get('imgFile')       #提取表单中‘name’为‘file’的文件元数据
        data={}
        try:
            #request_url = upload_img_localhost(app_name,file_metas)
            img_url,img=None,None
            is_ok,files = upload_to_oss(self,IMG_BUCKET,param_name='imgFile',file_type='undefine',file_prex=code)
            print is_ok,files
            if is_ok:
                img_url = options.IMG_DOMAIN+'/'+files[0].get('full_name')+img_compression(files[0].get('size'))
               # img = Images.create_image(code,files[0].get('size'),img_url,files[0].get('full_name'))
                #  files.append({'size':len(meta['body']),
                #     'full_name':save_name,
                #     'file_name':filename,
                #     'content_type':meta['content_type'],
                #
                # })
            else:
                data['error']=1
                data['message']=files
                data['url']=''
                data['img_id']=''
                return self.write(json.dumps(data))
        except Exception,e:
            data['error']=1
            data['message']=e.message
            data['url']=''
            data['img_id']=''
            return self.write(json.dumps(data))

        data['error']=0
        data['message']=''
        data['url']=img_url
        self.write(json.dumps(data))

        #{"error":0,"message":".....","url":"/img/1111.gif"}


class ImgFileHandler(tornado.web.RequestHandler):

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

import re

udir = os.path.join(os.path.dirname(__file__))[0:-7] + "../static/attached"

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        upload = {
        "moveup_dir_path" : "",
        "current_dir_path" : "",
        "current_url" : "/static/attached/",
        "file_list" : [],
        }

        for dirfile in glob.glob(udir + '/*'):
            filesize = os.path.getsize(dirfile)
            filetype = os.path.splitext(dirfile)[-1].lower()
            filename = os.path.basename(dirfile)
            datetime = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getctime(dirfile)))
            if re.match('\.gif|\.jpg|\.jpeg|\.png|\.bmp',filetype):
                is_photo = True
            else:
                is_photo = False
            file_list = {
            "is_dir" : False,
            "has_file" : False,
            "filesize" : filesize,
            "dir_path" : "",
            "is_photo" : is_photo,
            "filetype" : filetype,
            "filename" : filename,
            "datetime" : datetime,
            }
            upload["file_list"].append(file_list)
            upload = json.dumps(upload)
            self.write(upload)


    def post(self):
        if self.request.files:
            for f in self.request.files["imgFile"]:
                try:
                    rawname = f['filename']
                    rename = str(int(time.time()))+'.'+rawname.split('.').pop()
                    dstname = udir + "/" + rename
                    fbody = f["body"]
                    (lambda f, d: (f.write(d), f.close()))(open(dstname, 'wb'), fbody)
                    info = {
                    "error" : 0,
                    "url" : "/static/attached/" + rename
                     }
                except Exception,ex:
                    info = {
                    "error" : 1,
                    #"message" : "文件上传失败！"
                    "message" : str(ex)
                    }


        else:
            info = {
            "error" : 1,
            "message" : "您没有上传任何文件！"
        }
        info = json.dumps(info)
        self.write(info)

