 #encoding:utf-8

handlers=[]


from photo_upload_handler import *


handlers.extend([


    (r'/album/photo/qa/upload/', PhotoQAUploadHandler), #问答图片上传
    (r'/album/photo/topic/upload/',PhotoTopicUploadHandler),

])