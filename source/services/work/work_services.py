#encoding:utf-8
__author__ = 'sunli'

from sqlalchemy.sql.functions import now

from services.base_services import BaseService
from models.product_do import WeddingPhotoProduct,WeddingPhotoProductImages
from models.album_do import Photos
import ujson

class WorkServices(BaseService):
    '''
     :查询作品
    '''
    def query_work(self,**kwargs):
        if kwargs.get('code',''):
            query = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted == 1)
        else:
            query = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted==0)
        if kwargs.get('product_type',''):
            query = query.filter(WeddingPhotoProduct.Fproduct_type == kwargs.get('product_type'))
        if kwargs.get('id',''):
            query = query.filter(WeddingPhotoProduct.Fid == kwargs.get('id',''))

        if kwargs.get('merchant_id',''):
            query = query.filter(WeddingPhotoProduct.Fmerchant_id == kwargs.get('merchant_id',''))
        if kwargs.get('name',''):
            name = kwargs.get('name', '')
            name = name.strip()
            query = query.filter(WeddingPhotoProduct.Fname.like('%'+name+'%'))

        if kwargs.get('style',''):
            query = query.filter(WeddingPhotoProduct.Fstyle_code == kwargs.get('style'))
        if kwargs.get('scene'):
            query = query.filter(WeddingPhotoProduct.Fshot_scene_code == kwargs.get('scene'))

        if kwargs.get('shot_space',''):
            query = query.filter(WeddingPhotoProduct.Fshot_space == kwargs.get('shot_space'))
        if kwargs.get('mode_style',''):
            query = query.filter(WeddingPhotoProduct.Fmode_style_code == kwargs.get('mode_style'))
        if kwargs.get('start_date',''):
            query = query.filter(WeddingPhotoProduct.Fcreate_time >= kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(WeddingPhotoProduct.Fcreate_time <= kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('order_by','Fcreate_time'):
            query = query.order_by(kwargs.get('order_by','Fcreate_time'))
        return query

    def create_work(self,**kargs):
        '''
         :创建作品
        '''
        work = WeddingPhotoProduct()

        work.Fmerchant_id = kargs.get('Fmerchant_id', None)              #:商家ID 装修公司
        work.Fuser_id = kargs.get('Fuser_id', None)
        work.Fproduct_type= kargs.get('Fproduct_type', None)             #产品类型

        work.Fshot_space= kargs.get('Fshot_space', None)                 #拍摄地点
        work.Fshot_space_name = kargs.get('shot_space_name', None)

        work.Fname      = kargs.get('Fname', None)                       #名称
        work.Fstyle_code  = kargs.get('Fstyle_code', None)               #风格ID
        work.Fstyle_name= kargs.get('Fstyle_name', None)                 #风格名称

        work.Fshot_scene_code = kargs.get('Fshot_scene_code', None)      #拍摄场景ID
        work.Fshot_scene_name = kargs.get('Fshot_scene_name', None)      #拍摄场景名称
        work.Fmode_style_code = kargs.get('Fmode_style_code', None)      #造型特色ID
        work.Fmode_style_name = kargs.get('Fmode_style_name', None)      #造型特色名称

        work.Fsale_price= kargs.get('Fsale_price', None)                 #起拍价

        work.Ftitle     = kargs.get('Ftitle', None)                      #标题
        work.Fdescription = kargs.get('Fdescription', None)              #描述
        work.Fcover_img = kargs.get('Fcover_img', None)                  #封面图

        self.db.add(work)
        self.db.commit()

        self.add_work_images(work.Fid,kargs.get('images'))
        return True, work

    def add_work_images(self,Fid,images):

        data = ujson.loads(images)

        for key in data.keys():
            img = WeddingPhotoProductImages()
            img.Fwedding_photo_product_id = Fid
            img.Fimg_id = data[key].get('id')
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==data[key].get('id')).scalar()
            img.Fdescription = data[key].get('desc')
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)
        self.db.commit()

    def update_word_images(self,Fid,images):
        '''
        :todo 修改图片
        :param Fid:
        :param images:
        :return:
        '''
        data = ujson.loads(images)

        images = self.db.query(WeddingPhotoProductImages).\
            filter(WeddingPhotoProductImages.Fdeleted==0,WeddingPhotoProductImages.Fwedding_photo_product_id==Fid)

        new_images = [data[key].get('id') for key in data.keys() if int(data[key].get('id')) not in [i.Fimg_id for i in images]]

        for key in new_images:
            img = WeddingPhotoProductImages()
            img.Fwedding_photo_product_id = Fid
            img.Fimg_id = key
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==key).scalar()
            self.db.add(img)

        #图片排序
        for key in data.keys():
            img = self.db.query(WeddingPhotoProductImages).\
                  filter(WeddingPhotoProductImages.Fdeleted==0,WeddingPhotoProductImages.Fimg_id==data[key].get('id')).scalar()
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)

        self.db.commit()


    def update_work(self, work, **kargs):
        '''
        :todo 修改产品
        :param work_id:
        :param kargs:
        :return:
        '''
        work.Fuser_id = kargs.get('Fuser_id', None)
        work.Fproduct_type= kargs.get('Fproduct_type', None)             #产品类型

        work.Fshot_space= kargs.get('Fshot_space', None)                 #拍摄地点
        work.Fshot_space_name = kargs.get('shot_space_name', None)

        work.Fname = kargs.get('Fname', None)                       #名称
        work.Fstyle_code  = kargs.get('Fstyle_code', None)               #风格ID
        work.Fstyle_name= kargs.get('Fstyle_name', None)                 #风格名称

        work.Fshot_scene_code = kargs.get('Fshot_scene_code', None)      #拍摄场景ID
        work.Fshot_scene_name = kargs.get('Fshot_scene_name', None)      #拍摄场景名称
        work.Fmode_style_code = kargs.get('Fmode_style_code', None)      #造型特色ID
        work.Fmode_style_name = kargs.get('Fmode_style_name', None)      #造型特色名称

        work.Fsale_price= kargs.get('Fsale_price', None)                 #起拍价

        work.Ftitle = kargs.get('Ftitle', None)                      #标题
        work.Fdescription = kargs.get('Fdescription', None)              #描述
        work.Fcover_img = kargs.get('Fcover_img', None)                  #封面图

        self.update_word_images(work.Fid,kargs.get('images'))
        self.db.add(work)
        self.db.commit()

        return True, work


    def query_works(self,merchant_id,**kwargs):
        query = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted == 0)
        if merchant_id:
            query = query.filter(WeddingPhotoProduct.Fmerchant_id == merchant_id)
        if kwargs.get('product_type',''):
            query = query.filter(WeddingPhotoProduct.Fproduct_type==kwargs.get('product_type'))
        if kwargs.get('start_date',''):
            query = query.filter(WeddingPhotoProduct.Fcreate_time > kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(WeddingPhotoProduct.Fcreate_time < kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('type',''):
           query = query.filter(WeddingPhotoProduct.Fproduct_type == kwargs.get('type'))
        if kwargs.get('search_text',''):
            content = kwargs.get('search_text')
            query = query.filter(WeddingPhotoProduct.Fname.like('%'+content+'%'))
        if kwargs.get('order_by',''):
            query = query.order_by(kwargs.get('order_by',''))
        return query

    def get_work_iamges_by_id(self,work_id):
        '''
        :todo 获取图片
        :param work_id:
        :return:
        '''
        return self.db.query(WeddingPhotoProductImages).\
            filter(WeddingPhotoProductImages.Fdeleted==0,WeddingPhotoProductImages.Fwedding_photo_product_id==work_id).order_by('Fsort')


    def get_product_by_id(self,product_id):
        '''
        :根据ID获取产品信息
        :param product_id:
        :return:
        '''
        product  = self.db.query(WeddingPhotoProduct).filter(WeddingPhotoProduct.Fdeleted==0,WeddingPhotoProduct.Fid==product_id).scalar()
        images = self.get_work_iamges_by_id(product_id)
        return product,images

    def delete_work(self,work,merchant_id):
        '''
        todo:删除作品
        :param work_id:
        :return:
        '''
        query = self.db.query(WeddingPhotoProduct).\
            filter(WeddingPhotoProduct.Fdeleted == 0,WeddingPhotoProduct.Fid == work.Fid,WeddingPhotoProduct.Fmerchant_id == merchant_id)
        query.update({'Fdeleted':1})
        query_images = self.db.query(WeddingPhotoProductImages).\
            filter(WeddingPhotoProductImages.Fdeleted == 0,WeddingPhotoProductImages.Fwedding_photo_product_id == work.Fid)
        for image in query_images:
            image.Fdeleted= 1
            self.db.add(image)
        self.db.commit()