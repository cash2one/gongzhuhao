#-*- coding: utf-8 -*-
import os
import tempfile
try:
    from PIL import Image
except:
    pass

import sys
import logging
import urllib
import traceback
from oss_file_deal import upload_by_userinput,delete_file

from utils.random_utils import get_chars
from utils.datetime_util import datetime_format
from tornado.options import options



LOG = logging.getLogger(__name__)
__author__ = 'binpo'


WATER_IMG_SIZE=()


try:
    import Image
    import ImageFile
except:
    try:
        from PIL import Image as image
        from PIL import ImageFile
    except:
        pass

#import Image as image

def clip_img(im,sf_w,sf_h,x,y,x1,y1):

    # args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    # arg = {}
    # for key in args_key:
    #     if key in args:
    #         arg[key] = args[key]
    #
    # im = Image.open(arg['ori_img'])
    # ori_w,ori_h = im.size
    #
    # dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    # ori_scale = float(ori_h) / ori_w #原高宽比
    #
    # if ori_scale >= dst_scale:
    #     #过高
    #     width = ori_w
    #     height = int(width*dst_scale)
    #
    #     x = 0
    #     y = (ori_h - height) / 3
    #
    # else:
    #     #过宽
    #     height = ori_h
    #     width = int(height*dst_scale)
    #
    #     x = (ori_w - width) / 2
    #     y = 0
    # im = im.resize((int(float(sf_w)),int(float(sf_h))), Image.ANTIALIAS)

    # 原来将图片resize到传入大小，根据传入坐标裁剪 图片会模糊
    #现在将根据传入大小重新计算坐标  在原图上面根据计算后坐标 裁剪
    # real_w,real_h = im.size
    # w_percent = real_w/float(sf_w)
    # h_percent = real_h/float(sf_h)
    # #裁剪
    # box = (int(float(x)*w_percent),int(float(y)*h_percent),int(float(x1)*w_percent) if int(float(x1)*w_percent) < real_w else real_w,int(float(y1)*h_percent) if int(float(y1)*h_percent) < real_h else real_h)
    # #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    # #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    # newIm = im.crop(box)
    # #newIm.save('t1.png')
    # return newIm

    real_w,real_h = im.size
    w_percent = real_w/float(sf_w)
    h_percent = real_h/float(sf_h)
    #裁剪
    box = (int(float(x)*w_percent),int(float(y)*h_percent),int(float(x1)*w_percent) if int(float(x1)*w_percent) < real_w else real_w,int(float(y1)*h_percent) if int(float(y1)*h_percent) < real_h else real_h)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    #newIm.save('t.png')
    return newIm

#等比例压缩图片
def resizeImg(im,**args):
    args_key = {'ori_img':'','dst_img':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    # im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size
    arg['dst_w'] = ori_w
    arg['dst_h'] = ori_h

    widthRatio = heightRatio = None
    ratio = 1
    if (ori_w and ori_w > arg['dst_w']) or (ori_h and ori_h > arg['dst_h']):
        if arg['dst_w'] and ori_w > arg['dst_w']:
            widthRatio = float(arg['dst_w']) / ori_w #正确获取小数的方式
        if arg['dst_h'] and ori_h > arg['dst_h']:
            heightRatio = float(arg['dst_h']) / ori_h

        if widthRatio and heightRatio:
            if widthRatio < heightRatio:
                ratio = widthRatio
            else:
                ratio = heightRatio

        if widthRatio and not heightRatio:
            ratio = widthRatio
        if heightRatio and not widthRatio:
            ratio = heightRatio

        newWidth = int(ori_w * ratio)
        newHeight = int(ori_h * ratio)
    else:
        newWidth = ori_w
        newHeight = ori_h

    im.resize((newWidth,newHeight),image.ANTIALIAS)#.save(arg['dst_img'],quality=arg['save_q'])
    return im

    '''
    image.ANTIALIAS还有如下值：
    NEAREST: use nearest neighbour
    BILINEAR: linear interpolation in a 2x2 environment
    BICUBIC:cubic spline interpolation in a 4x4 environment
    ANTIALIAS:best down-sizing filter
    '''

#裁剪压缩图片
def clipResizeImg(**args):

    args_key = {'ori_img':'','dst_img':'','dst_w':'','dst_h':'','save_q':75}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]

    im = image.open(arg['ori_img'])
    ori_w,ori_h = im.size

    dst_scale = float(arg['dst_h']) / arg['dst_w'] #目标高宽比
    ori_scale = float(ori_h) / ori_w #原高宽比

    if ori_scale >= dst_scale:
        #过高
        width = ori_w
        height = int(width*dst_scale)

        x = 0
        y = (ori_h - height) / 3

    else:
        #过宽
        height = ori_h
        width = int(height*dst_scale)

        x = (ori_w - width) / 2
        y = 0

    #裁剪
    box = (x,y,width+x,height+y)
    #这里的参数可以这么认为：从某图的(x,y)坐标开始截，截到(width+x,height+y)坐标
    #所包围的图像，crop方法与php中的imagecopy方法大为不一样
    newIm = im.crop(box)
    im = None

    #压缩
    ratio = float(arg['dst_w']) / width
    newWidth = int(width * ratio)
    newHeight = int(height * ratio)
    newIm.resize((newWidth,newHeight),image.ANTIALIAS)
    return newIm
    #save(arg['dst_img'],quality=arg['save_q'])


#水印(这里仅为图片水印)
def waterMark(im,**args):
    args_key = {'ori_img':'','dst_img':'','mark_img':'','water_opt':''}
    arg = {}
    for key in args_key:
        if key in args:
            arg[key] = args[key]


    #im = image.open(arg['ori_img'])

    ori_w,ori_h = im.size

    mark_im = image.open(arg['mark_img'])
    mark_w,mark_h = mark_im.size
    option ={'leftup':(0,0),'rightup':(ori_w-mark_w,0),'leftlow':(0,ori_h-mark_h),
             'rightlow':(ori_w-mark_w,ori_h-mark_h)
             }


    im.paste(mark_im,option[arg['water_opt']],mark_im.convert('RGBA'))
    #im.save(arg['dst_img'])
    return im

#
#Demon
#源图片
#水印标

#水印位置(右下)
water_opt = 'leftlow'
#目标图片
dst_img = 'python_2.jpg'
#目标图片大小
dst_w = 94
dst_h = 94
#保存的图片质量
save_q = 70
#裁剪压缩
#clipResizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q = save_q)
#等比例压缩
#resizeImg(ori_img=ori_img,dst_img=dst_img,dst_w=dst_w,dst_h=dst_h,save_q=save_q)
#水印
#waterMark(ori_img=ori_img,dst_img=dst_img,mark_img=mark_img,water_opt=water_opt)

def format_img_name(img_name):

    '''
    :todo 格式化图片名称
    :param img_name:
    :return:
    '''

    # if img_name[::-1].find('@')!=-1:
    #     img_name = img_name[:img_name[::-1].find('@')]
    return img_name


def upload_to_oss(http_handle,bucket,param_name='imgFile',file_type='img',file_prex=None,max_size=100,water_mark=False,is_apps=False,is_sort=False):

    """上传文件到OSS
    :param http_handle
    :param bucket  oss namespace
    :param_name form 参数名称
    :param max_size 上传文件的最大容量 单位M
    :file_prex 文件前缀  example xxx/dd
    """
    data={}
    file_metas=http_handle.request.files.get(param_name)
    if http_handle.request.files == {} or param_name not in http_handle.request.files:
        return False,'参数不存在'
    avatar_file = http_handle.request.files[param_name][0]
    print avatar_file['content_type']
    if file_type=='img':
        image_type_list = ['image/gif', 'image/jpeg', 'image/pjpeg', 'image/bmp', 'image/png', 'image/x-png','application/octet-stream']
        if avatar_file['content_type'] not in image_type_list:
            return False,'仅支持jpg,jpeg,bmp,gif,png格式的图片！'

    elif file_type=='pdf':
        pdf_type_list = ['application/pdf']
        if avatar_file['content_type'] not in pdf_type_list:
            return False,'仅支持pdf格式文件'
    if len(avatar_file['body'])/1024/1024 > max_size:
            return False,'图片%s 过大,请使用%sM以内图片上传,'%(avatar_file['filename'],max_size)
    files=[]
    try:
        if is_apps:
            name_prefix=''
        else:name_prefix = datetime_format(format='%H%M%S')+get_chars()
        for meta in file_metas:
            filename = name_prefix+format_img_name(meta['filename'])
            if file_prex:
                save_name=''.join((file_prex,'/',name_prefix+format_img_name(meta['filename'])))
            else:
                save_name = name_prefix+format_img_name(meta['filename'])

            if is_sort:
                files.append(
                        {'size':len(meta['body']),
                        'full_name':save_name,
                        'name':filename,
                        'type':meta['content_type'],
                        "url": options.IMG_DOMAIN+'/'+save_name
                })
                file_ids = http_handle.album_service.album_add_photos(http_handle.album_Fid,http_handle.merchant_id,http_handle.user_id,files,is_exquisite=False)
                files[0]['file_ids'] = file_ids
            file_stream = meta['body']
            contents = file_stream
            is_ok = upload_by_userinput(bucket,filename,save_name,contents)
            if is_ok=='OK':
                if not is_sort:
                    files.append(
                        {'size':len(meta['body']),
                        'full_name':save_name,
                        'file_name':filename,
                        'content_type':meta['content_type'],
                    })
            else:
                try:
                    if is_sort:
                        http_handle.album_service.delete_photo_by_photo_id(http_handle.merchant_id,file_ids[0])
                except Exception,e:
                    print 'e.message:',e.message
                    pass
                return  False,'Upload oss failure'
    except Exception:
        e = sys.exc_info()[0](traceback.format_exc())
        LOG.exception(e)
    return True,files

def upload_resize(http_handle,bucket,img_url,file_prex=None,**kargs):

    """上传文件到OSS 压缩水印处理
    :param http_handle
    :param bucket  oss namespace
    :param_name form 参数名称
    :file_prex 文件前缀  example xxx/dd
    """
    img_url = img_url.split('@')[0]
    names = img_url.split('/')
    files=[]

    try:
        name_prefix = datetime_format(format='%H%M%S')+get_chars()
        # #for meta in file_metas:
        filename = name_prefix+names[-1].replace('%', '').replace('%', '')
        if file_prex:
            save_name=''.join((file_prex,'/',name_prefix+names[-1].replace('%', '')))
        else:
            save_name = name_prefix+names[-1].replace('%', '')
        print 'filename:',filename
        parser = ImageFile.Parser()
        #for chunk in file_stream.chunks():
        print img_url
        file_stream = urllib.urlopen(img_url.strip()).read()#'http://img.zenmez.com/album/member/c1d5736e-f85d-30a6-95c7-7a5042a1a560/默认相册/20141230/tjyg.jpg')

        parser.feed(file_stream)
        width,height = parser.image.size

        img = parser.close()
        #print file_stream
        #oss_write = clip_img(img,width,height,kargs.get('x'),kargs.get('y'),kargs.get('x1'),kargs.get('y1'))#缩放 前切
        oss_write = clip_img(img,kargs.get('sf_w'),kargs.get('sf_h'),kargs.get('x'),kargs.get('y'),kargs.get('x1'),kargs.get('y1'))#缩放 前切

        FILE_FORMAT={'image/gif':'GIF', 'image/jpeg':'JPEG', 'image/jpg':'JPEG', 'image/pjpeg':'PJEGP', 'image/bmp':'BMP', 'image/png':'PNG', 'image/x-png':'PNG'}
        content_type = None
        file_type = names[-1].split('.')[-1].lower()
        #print file_type
        for key in FILE_FORMAT.keys():
            if file_type in key:
                content_type = key
                break
        if not content_type:
             return  False,'图片格式不正确'
        #图片转换成字符流输出到内存  然后会写oss
        import StringIO
        output = StringIO.StringIO()
        oss_write.save(output,format=FILE_FORMAT[content_type])
        contents = output.getvalue()
        output.close()
        #print contents
        #
        # else:
        #     contents = file_stream

        #response_time = (timeit.default_timer() - stat_time) % 1000
        #print 'img_ys:',response_time
        #print filename,save_name
        is_ok = upload_by_userinput(bucket,filename,save_name,contents)

        #response_time = (timeit.default_timer() - stat_time) % 1000
        #print 'write_oss:',response_time
        #print filename,save_name
        if is_ok=='OK':
            files.append(
                {'size':len(file_stream),
                'full_name':save_name,
                'file_name':filename,
                'content_type':''
            })
        else:return  False,'Upload oss failure'
    except Exception,e:
        e = sys.exc_info()[0](traceback.format_exc())
        LOG.exception(e)
        return  False,'Upload oss failure'

    return True,files


def delete_from_oss(bucket,file_name):

    """删除文件 from bucket空间
    :param http_handle
    :param bucket  oss namespace
    :param_name form 参数名称
    :file_prex 文件前缀  example xxx/dd
    """
    #res = oss.delete_object('zenmez', 'user/hello/IMG_0663.JPG')
    #res = oss.delete_object(bucket,file_name)
    delete_file(bucket,file_name)
    #if res.status != 204:
    #    print "delete part ", 'user/hello/IMG_0663.JPG', " in bucket:", 'zenmez', " failed!"
    #else:
    #    print "delete part ", 'user/hello/IMG_0663.JPG', " in bucket:", 'zenmez', " ok"


