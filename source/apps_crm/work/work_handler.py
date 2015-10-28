# encoding:utf-8

__author__ = 'sunli'

import tornado
import ujson
from tornado.web import MissingArgumentError
from utils.error_util import Error

from common.base import BaseHandler
from services.work.work_services import WorkServices
from common.permission_control import company_permission_control
import sys
from models.product_do import WeddingPhotoProductImages
work_service = WorkServices()

#风格
from conf.work_conf import _WORK_STYLE as work_style,_SHOOTING_SCENE as shooting_scene,_MODE_STYLE as mode_style,_SHOOTING_SCENE_2 as shooting_scene_traveling,_SHOOTING_SITE


class WorkList(BaseHandler):
    '''
    作品一览Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('work_view')
    def get(self, product_type='wedding'):
        try:
            if 'merchant' in self.get_current_user().get('Frole_codes'):
                uid = self.get_current_user().get('Fid')
            else:
                uid = self.get_current_user().get('Fmerchant_id')

            work_service.set_db(self.db)
            work = work_service.query_work(merchant_id=uid, product_type=product_type)
            html = 'crm/404.html'
            if product_type == 'wedding':
                html = 'crm/work/work_list.html'
            elif product_type == 'traveling':
                html = 'crm/work/work_list_traveling.html'

            self.echo(html,
                      {
                          'work' : work,
                       },layout='crm/common/base.html')

        except Exception, e:
            self.echo('crm/404.html')

class WorkAdd(BaseHandler):
    '''
    作品添加、编辑Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self, work_id=None):
        try:
            if not work_id:   #新增
                work_id = 0
                work = None
                images=[]
            else:   #编辑
                work_id = int(work_id)
                merchant_id = self.current_user.get('Fmerchant_id') #商户id

                work_service.set_db(self.db)
                work = work_service.query_work(id=work_id, merchant_id=merchant_id)
                work = work.first()
                if work:
                    images = work_service.get_work_iamges_by_id(work_id)
                if not work:#检查
                    raise
            self.echo('crm/work/work_add.html',
                      {
                          'work_id' : work_id,
                          'work' : work,
                          'work_style' : work_style,
                          'shooting_scene' : shooting_scene,
                          'mode_style' : mode_style,
                          'shooting_scene_traveling' : shooting_scene_traveling,
                          'images':images,
                          'shoot_site':_SHOOTING_SITE
                      })
        except Exception, e:
            if self.settings.get('debug'):
                self.write(str(e))
                raise

            self.write(Error(2, e.message).__dict__)

    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def post(self, work_id=None):

        self.get_paras_dict()

        try:
            dic_result = {}
            dic_result['stat'] = 'ok'
            dic_result['msg'] = ''

            work_id = int(work_id)

            dic_para = {}
            if not work_id:   #新建时
                dic_para['Fuser_id'] = self.current_user.get('Fid') #子商户id
                dic_para['Fmerchant_id'] = self.current_user.get('Fmerchant_id') #商户id
            else:   #更新时
                dic_para['Fuser_id'] = self.current_user.get('Fid') #子商户id

            product_type = self.qdict.get('product_type', None)             #产品类型
            dic_para['Fproduct_type'] = product_type
            dic_result['product_type'] = product_type

            dic_para['Fname'] = self.qdict.get('name', None)                    #名称

            #----------旅游婚纱拍摄地------------
            shot_code = self.qdict.get('shot_code')
            dic_para['Fshot_space'] =shot_code
            if shot_code=="user_writing":
                dic_para['shot_space_name'] = self.qdict.get('shot_space')
            else:
                for scene in _SHOOTING_SITE:
                    if scene[0] == shot_code:
                        dic_para['shot_space_name'] = scene[1]                #拍摄场景名称
                        break

            dic_para['Fstyle_code'] = self.qdict.get('style_code', None)                  #风格code
            if dic_para.get('Fstyle_code') == 'user_writing':
                dic_para['Fstyle_name'] = self.qdict.get('style_name', None)                #风格名称
            else:
                for style in work_style:
                    if style[0] == dic_para.get('Fstyle_code'):
                        dic_para['Fstyle_name'] = style[1]
                        break

            scene_code = self.qdict.get('shot_scene_code', None)         #拍摄场景code
            dic_para['Fshot_scene_code'] = scene_code
            if product_type == 'wedding':
                indoor = shooting_scene.get('indoor')
                ourdoor = shooting_scene.get('outdoor')
                if scene_code in indoor.keys():
                    if scene_code=="z_indoor_user_writing":
                        dic_para['Fshot_scene_name'] = self.qdict.get('shot_scene_name_indoor')
                    else:
                        for key in indoor:
                            if scene_code==key:
                                dic_para['Fshot_scene_name'] = indoor[key]                #拍摄场景名称
                                break

                elif scene_code in ourdoor.keys():
                    if scene_code=="z_outdoor_user_writing":
                        dic_para['Fshot_scene_name'] = self.qdict.get('shot_scene_name_outdoor')
                    else:
                        for key in ourdoor:
                            if scene_code==key:
                                dic_para['Fshot_scene_name'] = ourdoor[key]                #拍摄场景名称
                                break
            else:
                if scene_code=="user_writing":
                    dic_para['Fshot_scene_name'] = self.qdict.get('scene_traveling_name')
                else:
                    for scene in shooting_scene_traveling:
                        if scene[0] == scene_code:
                            dic_para['Fshot_scene_name'] = scene[1]                #拍摄场景名称
                            break


            mode_style_code = self.qdict.get('mode_style_code', None)    #造型特色code
            mode_style_name = ''    #造型特色名称
            for mode in mode_style:
                if mode_style_code.find(mode[0]) > -1:
                    mode_style_name = mode_style_name + mode[1] + ','
            dic_para['Fmode_style_code'] = mode_style_code.strip(',')         #造型特色code
            dic_para['Fmode_style_name'] = mode_style_name.strip(',')     #造型特色名称

            dic_para['Fsale_price'] = self.qdict.get('sale_price', None)                     #起拍价

            dic_para['Ftitle'] = self.qdict.get('title', None)                     #标题
            dic_para['Fdescription'] = self.qdict.get('description', None)                     #描述
            dic_para['Fcover_img'] = self.qdict.get('cover_url', None)                     #封面图

            dic_para['images'] = self.qdict.get('images', None)                     #作品上传图片

            work_service.set_db(self.db)

            if not work_id:   #新建时
                is_ok,work = work_service.create_work(**dic_para)
                self.delete_product_count(self.current_user.get('Fmerchant_id'))
            else:   #更新时
                work_id = int(work_id)
                work,images = work_service.get_product_by_id(work_id)
                is_ok,work = work_service.update_work(work, **dic_para)

            if is_ok:
                self.update_company_price(work.Fmerchant_id)

            self.write(ujson.dumps(dic_result))

        except Exception, e:
            
            dic_result['stat'] = 'fail'
            dic_result['msg'] = "提交失败"

            self.write(ujson.dumps(dic_result))

class WorkDelete(BaseHandler):
    '''
    作品删除Handler
    '''
    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self, work_id):
        try:
            work_id = int(work_id)
            work_service.set_db(self.db)
            merchant_id = self.current_user.get('Fmerchant_id') #商户id
            work = work_service.query_work(id = work_id).scalar()

            work_service.delete_work(work,merchant_id)

            self.update_company_price(merchant_id)

            self.redirect('/merchant/work/')
        except Exception, e:
            pass


class WorkImageDelete(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('work_edit')
    def get(self,work_img_id):

        try:
            del_img = self.db.query(WeddingPhotoProductImages).\
                filter(WeddingPhotoProductImages.Fdeleted==0,WeddingPhotoProductImages.Fid==work_img_id).scalar()

            if del_img:
                del_img.Fdeleted = 1
                self.db.add(del_img)
            self.db.commit()

        except Exception,e:
            pass
        self.write('ok')
