#encoding:utf-8
__author__ = 'sunli'

from sqlalchemy.sql.functions import now

from services.base_services import BaseService
from models.product_do import ShotPackage,ShotPackageImages,WeddingPhotoProduct
from models.album_do import Photos
from models.company_do import Company
import ujson

class SeriesServices(BaseService):
    '''
    todo:查询套系
    '''
    def query_series(self,**kwargs):

        if kwargs.get('code',''):
            query = self.db.query(ShotPackage).filter(ShotPackage.Fdeleted == kwargs.get('code'))
        else:
            query = self.db.query(ShotPackage).filter(ShotPackage.Fdeleted==0)

        if kwargs.get('merchant_id',''):
            query = query.filter(ShotPackage.Fmerchant_id == kwargs.get('merchant_id'))

        if kwargs.get('id',''):
            query = query.filter(ShotPackage.Fid == kwargs.get('id',''))

        if kwargs.get('package_name',''):
            package_name = kwargs.get('package_name', '')
            package_name = package_name.strip()

            query = query.filter(ShotPackage.Fpackage_name.like('%'+package_name+'%'))

        if kwargs.get('start_price',''):
            query = query.filter(ShotPackage.Fsale_price >= int(float(kwargs.get('start_price'))))

        if kwargs.get('end_price',''):
            query = query.filter(ShotPackage.Fsale_price <= int(float(kwargs.get('end_price'))))
        if kwargs.get('between_price',''):
            start_price,end_price = kwargs.get('between_price').split('-')
            if start_price:
                query = query.filter(ShotPackage.Fsale_price >= start_price)
            if end_price:
                query = query.filter(ShotPackage.Fsale_price <= end_price)

        if kwargs.get('start_date',''):
            query = query.filter(ShotPackage.Fcreate_time >= kwargs.get('start_date'))

        if kwargs.get('end_date',''):
            query = query.filter(ShotPackage.Fcreate_time < kwargs.get('end_date')+' 23:59:59')

        if kwargs.get('is_activity',''):
            query = query.filter(ShotPackage.Fis_activity == kwargs.get('is_activity'))

        if kwargs.get('order_by','Fcreate_time'):
            query = query.order_by(kwargs.get('order_by','Fcreate_time'))

        return query

    def get_essence_series(self):
        '''
        todo:获取精品推荐
        :return:
        '''
        return self.db.query(ShotPackage).\
            filter(ShotPackage.Fdeleted == 0,ShotPackage.Fcover_img != '').limit(4).offset(0)

    def create_series(self,**kargs):
        '''
         :创建套系
        '''
        series = ShotPackage()

        series.Fmerchant_id = kargs.get('Fmerchant_id', None)
        series.Fuser_id = kargs.get('Fuser_id', None)
        series.Fpackage_name = kargs.get('Fpackage_name', None) #套系名称

        series.Fprice = int(kargs.get('Fprice', None))    #原价
        series.Fsale_price = kargs.get('Fsale_price', None)    #现价

        series.Fbride_style_count = int(kargs.get('Fbride_style_count', None))    #新娘造型X套 单位是套
        series.Fgroom_style_count = int(kargs.get('Fgroom_style_count', None))    #新郎造型X套 单位是套
        series.Fcloth_select_type = kargs.get('Fcloth_select_type', None)    #服装选择区域  #服装选择类型  1.指定区域 2.全场任选
        series.Fcloth_remark = kargs.get('Fcloth_remark', None)    #补充说明

        series.Foutdoor_space = kargs.get('Foutdoor_space', None)    #外景地
        series.Finner_space = kargs.get('Finner_space', None)    #内景地
        series.Fspace_remark = kargs.get('Fspace_remark', None)    #补充说明

        series.Fshot_desc = kargs.get('Fshot_desc', None)    #套系特色
        series.Fphotographer_level = kargs.get('Fphotographer_level', None)    #摄影师级别
        series.Frecommend_photographer = kargs.get('Frecommend_photographer', None)    #推荐摄影师       #多个用空格隔开
        series.Farter_level = kargs.get('Farter_level', None)    #化妆师级别
        series.Frecommend_arter = kargs.get('Frecommend_arter', None)    #推荐化妆师              #多个用空格隔开

        series.Fphoto_album_desc = kargs.get('Fphoto_album_desc', None)    #相册
        series.Fphoto_frame_desc = kargs.get('Fphoto_frame_desc', None)    #相框
        series.Fmv_desc = kargs.get('Fmv_desc', None)    #相框
        series.Fother_desc = kargs.get('Fother_desc', None)    #其他描述

        series.Fdescription = kargs.get('Fdescription', None)    #套系补充说明#
        series.Fother_pay_desc = kargs.get('Fother_pay_desc', None)    #其他收费说明
        series.Fcover_img = kargs.get('Fcover_img',None) #封面图
        series.Fcreate_time = now()
        series.Fmodify_time = now()
        series.Fdeleted = 0

        self.db.add(series)
        self.db.commit()
        self.add_series_images(series.Fid,kargs.get('images'))
        return True, series

    def add_series_images(self,Fid,images):
        data = ujson.loads(images)#.keys()
        for key in data.keys():
            img = ShotPackageImages()
            img.Fshot_package_id = Fid
            img.Fimg_id = data[key].get('id')
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==data[key].get('id')).scalar()
            img.Fdescription = data[key].get('desc')
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)
        self.db.commit()

    def update_series(self, series_id, **kargs):
        '''
         :更新套系
        '''
        if 'images' in kargs:
            self.update_series_images(series_id,kargs.get('images','')) #更新照片
            kargs.pop('images')
        else:
            self.delete_images_by_id(series_id)
        query=self.db.query(ShotPackage).filter(ShotPackage.Fid==series_id,ShotPackage.Fdeleted==0)
        query.update(kargs)
        self.db.commit()
        return True,query.scalar()

    def update_series_images(self,Fid,images):
        '''
        :todo 修改图片
        :param Fid:
        :param images:
        :return:
        '''

        data = ujson.loads(images)

        for key in data.keys():

            img = self.db.query(ShotPackageImages).\
                filter(ShotPackageImages.Fimg_id==data[key].get('id'),ShotPackageImages.Fdeleted == 0).scalar()

            if not img:
                img = ShotPackageImages()

            img.Fshot_package_id = Fid
            img.Fimg_id = data[key].get('id')
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==data[key].get('id')).scalar()
            img.Fdescription = data[key].get('desc')

            #排序
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)

        self.db.commit()

    def get_series_iamges_by_id(self,series_id):
        return self.db.query(ShotPackageImages).filter(ShotPackageImages.Fdeleted == 0,ShotPackageImages.Fshot_package_id == series_id).order_by('Fsort')

    def get_series_by_id(self,series_id):
        '''
        todo 根据ID获取套系ID
        :param series_id:
        :return:
        '''
        return self.db.query(ShotPackage).filter(ShotPackage.Fdeleted==0,ShotPackage.Fid==series_id).scalar()

    def delete_images_by_id(self,series_id):
        '''
        todo:删除套系图片
        :param series_id:
        :return:
        '''
        query_list = self.db.query(ShotPackageImages).\
            filter(ShotPackageImages.Fdeleted == 0,ShotPackageImages.Fshot_package_id == series_id)
        for image in query_list:
            image.Fdeleted = 1
            self.db.add(image)
            self.db.commit()


