#encoding: utf-8
__author__ = 'hongjiongteng'

import ujson
from sqlalchemy import func
from sqlalchemy.orm import aliased
from services.base_services import BaseService
from models.product_do import WeddingCompanyShotPackage, WeddingCompanyShotPackageImage, WeddingCompanyPhotoProduct, WeddingCompanyPhotoProductImages
from models.company_do import Company
from models.album_do import Photos


class WeddingCompanySeriesService(BaseService):

    def series_common_query(self, query, **kwargs):
        if kwargs.get('between_price'):
            kwargs['start_price'], kwargs['end_price'] = kwargs.get('between_price').split('-')

        if kwargs.get('start_price'):
            query = query.filter(WeddingCompanyShotPackage.Fsale_price >= float(kwargs.get('start_price').strip()))

        if kwargs.get('end_price'):
            query = query.filter(WeddingCompanyShotPackage.Fsale_price <= float(kwargs.get('end_price').strip()))

        if kwargs.get('series_id'):
            query = query.filter(WeddingCompanyShotPackage.Fid == kwargs.get('series_id'))

        if kwargs.get('merchant_id'):
            query = query.filter(WeddingCompanyShotPackage.Fmerchant_id == kwargs.get('merchant_id'))

        if kwargs.get('order_by', 'Fcreate_time'):
            try:
                query = query.order_by(getattr(WeddingCompanyShotPackage, kwargs.get('order_by', 'Fcreate_time')))
            except Exception, e:
                query = query.order_by(kwargs.get('order_by', 'Fcreate_time'))

        return query

    def query_series(self, **kwargs):
        '''
        todo: 查询婚纱礼服的套系
        return: 循环query, 结果是(对象WeddingCompanyShotPackage, ...)
        '''
        query = self.db.query(WeddingCompanyShotPackage).filter(WeddingCompanyShotPackage.Fdeleted==0)

        return self.series_common_query(query, **kwargs)

    def query_series_and_company_name(self, **kwargs):
        '''
        todo: 查询婚纱礼服的套系
        return: 循环query, 结果是( (对象WeddingCompanyShotPackage, 字符串company_name), (..., ...),... )
        '''
        query = self.db.query(WeddingCompanyShotPackage, Company.Fcompany_name).\
                    filter(WeddingCompanyShotPackage.Fdeleted==0).join(Company, WeddingCompanyShotPackage.Fmerchant_id==Company.Fuser_id)

        return self.series_common_query(query, **kwargs)

    def add_series(self, **kwargs):
        t = WeddingCompanyShotPackage()

        t.Fpackage_name = kwargs.get('package_name')
        t.Fmerchant_id  = kwargs.get('merchant_id')
        t.Fuser_id      = kwargs.get('user_id')
        t.Fprice        = kwargs.get('price')
        t.Fsale_price   = kwargs.get('sale_price')
        t.Fwelcome_area = kwargs.get('welcome_area')

        t.Fceremony_area = kwargs.get('ceremony_area')
        t.Freception_area = kwargs.get('reception_area')
        t.Fequipment = kwargs.get('equipment')
        t.Farrangement_extra = kwargs.get('arrangement_extra')

        t.Fmeetingplace = kwargs.get('meetingplace')
        t.Fbridegroom = kwargs.get('bridegroom')
        t.Fbride = kwargs.get('bride')
        t.Fvip = kwargs.get('vip')
        t.Fflower_extra = kwargs.get('flower_extra')

        t.Fwedding_ceremony = kwargs.get('wedding_ceremony')
        t.Fbanquet_ceremony = kwargs.get('banquet_ceremony')
        t.Fceremony_extra = kwargs.get('ceremony_extra')

        t.Fmaster = kwargs.get('master')
        t.Fmakeup = kwargs.get('makeup')
        t.Fphotography = kwargs.get('photography')
        t.Fcamera = kwargs.get('camera')
        t.Fservice_extra = kwargs.get('service_extra')

        t.Fextra = kwargs.get('extra')
        t.Fcover_img = kwargs.get('cover_img')

        self.db.add(t)
        self.db.commit()
        self.add_series_images(t.Fid, kwargs.get('images'))

    def add_series_images(self, series_id, images):
        data = ujson.loads(images)

        for key in data.keys():
            img = WeddingCompanyShotPackageImage()
            img.Fshot_package_id = series_id
            img.Fimg_id = data[key].get('id')
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==data[key].get('id')).scalar()
            img.Fdescription = data[key].get('desc')
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)

        self.db.commit()

    def query_series_images(self, **kwargs):
        query = self.db.query(WeddingCompanyShotPackageImage).filter(WeddingCompanyShotPackageImage.Fdeleted==0)

        if kwargs.get('series_id'):
            query = query.filter(WeddingCompanyShotPackageImage.Fshot_package_id==kwargs.get('series_id'))

        if kwargs.get('img_id'):
            query = query.filter(WeddingCompanyShotPackageImage.Fimg_id==kwargs.get('img_id'))

        if kwargs.get('order_by', 'Fsort'):
            query = query.order_by(kwargs.get('order_by', 'Fsort'))

        return query

    def delete_series_images(self, **kwargs):
        query = self.db.query(WeddingCompanyShotPackageImage).filter(WeddingCompanyShotPackageImage.Fdeleted==0)

        if kwargs.get('series_id'):
            query = query.filter(WeddingCompanyShotPackageImage.Fshot_package_id==kwargs.get('series_id'))
            query.update({WeddingCompanyShotPackageImage.Fdeleted: 1})

        if kwargs.get('img_id'):
            query = query.filter(WeddingCompanyShotPackageImage.Fimg_id==kwargs.get('img_id'))
            query.update({WeddingCompanyShotPackageImage.Fdeleted: 1})

        self.db.commit()

    def update_series(self, series_id, **kwargs):
        if series_id:
            t = {}

            t['Fpackage_name'] = kwargs.get('package_name')
            t['Fmerchant_id']  = kwargs.get('merchant_id')
            t['Fuser_id']      = kwargs.get('user_id')
            t['Fprice']        = kwargs.get('price')
            t['Fsale_price']   = kwargs.get('sale_price')
            t['Fwelcome_area'] = kwargs.get('welcome_area')

            t['Fceremony_area'] = kwargs.get('ceremony_area')
            t['Freception_area'] = kwargs.get('reception_area')
            t['Fequipment'] = kwargs.get('equipment')
            t['Farrangement_extra'] = kwargs.get('arrangement_extra')

            t['Fmeetingplace'] = kwargs.get('meetingplace')
            t['Fbridegroom'] = kwargs.get('bridegroom')
            t['Fbride'] = kwargs.get('bride')
            t['Fvip'] = kwargs.get('vip')
            t['Fflower_extra'] = kwargs.get('flower_extra')

            t['Fwedding_ceremony'] = kwargs.get('wedding_ceremony')
            t['Fbanquet_ceremony'] = kwargs.get('banquet_ceremony')
            t['Fceremony_extra'] = kwargs.get('ceremony_extra')

            t['Fmaster'] = kwargs.get('master')
            t['Fmakeup'] = kwargs.get('makeup')
            t['Fphotography'] = kwargs.get('photography')
            t['Fcamera'] = kwargs.get('camera')
            t['Fservice_extra'] = kwargs.get('service_extra')

            t['Fextra'] = kwargs.get('extra')
            t['Fcover_img'] = kwargs.get('cover_img')

            query = self.db.query(WeddingCompanyShotPackage).filter(WeddingCompanyShotPackage.Fdeleted==0).filter(WeddingCompanyShotPackage.Fid==series_id)
            if query.scalar():
                query.update(t)
                self.db.commit()
                self.delete_series_images(series_id=series_id)
                self.add_series_images(series_id, kwargs.get('images'))

    def delete_series(self, series_id):
        if series_id:
            query = self.db.query(WeddingCompanyShotPackage).filter(WeddingCompanyShotPackage.Fdeleted==0).filter(WeddingCompanyShotPackage.Fid==series_id)
            query.update({WeddingCompanyShotPackage.Fdeleted: 1})
            self.db.commit()
            self.delete_series_images(series_id=series_id)

    def min_and_max_price(self, merchant_id):
        query = self.db.query(func.min(WeddingCompanyShotPackage.Fsale_price), func.max(WeddingCompanyShotPackage.Fsale_price)).\
                        filter(WeddingCompanyShotPackage.Fmerchant_id==merchant_id).filter(WeddingCompanyShotPackage.Fdeleted==0)

        return query.one()

    def get_essence_series(self):
        return self.db.query(WeddingCompanyShotPackage).\
                       filter(WeddingCompanyShotPackage.Fdeleted == 0,WeddingCompanyShotPackage.Fcover_img != '').limit(4).offset(0)


class WeddingCompanyWorkService(BaseService):

    def work_common_query(self, query, **kwargs):
        if kwargs.get('category'):
            query = query.filter(WeddingCompanyPhotoProduct.Fcategory == kwargs.get('category'))

        if kwargs.get('color'):
            query = query.filter(WeddingCompanyPhotoProduct.Fcolor == kwargs.get('color'))

        if kwargs.get('style'):
            query = query.filter(WeddingCompanyPhotoProduct.Fstyle == kwargs.get('style'))

        if kwargs.get('merchant_id'):
            query = query.filter(WeddingCompanyPhotoProduct.Fmerchant_id == kwargs.get('merchant_id'))

        if kwargs.get('work_id'):
            query = query.filter(WeddingCompanyPhotoProduct.Fid == kwargs.get('work_id'))

        if kwargs.get('order_by', 'Fcreate_time'):
            try:
                query = query.order_by(getattr(WeddingCompanyPhotoProduct, kwargs.get('order_by', 'Fcreate_time')))
            except Exception, e:
                query = query.order_by(kwargs.get('order_by', 'Fcreate_time'))

        return query

    def query_work(self, **kwargs):
        '''
        todo: 查询婚庆公司的作品
        return: 循环query, 结果是(对象WeddingCompanyShotPackage, ...)
        '''
        query = self.db.query(WeddingCompanyPhotoProduct).filter(WeddingCompanyPhotoProduct.Fdeleted==0)

        return self.work_common_query(query, **kwargs)

    def query_work_and_company_name(self, **kwargs):
        '''
        todo: 查询婚庆公司的作品
        return: 循环query, 结果是( (对象WeddingCompanyPhotoProduct, 字符串company_name), (..., ...),... )
        '''
        query = self.db.query(WeddingCompanyPhotoProduct, Company.Fcompany_name).\
                    filter(WeddingCompanyPhotoProduct.Fdeleted==0).join(Company, WeddingCompanyPhotoProduct.Fmerchant_id==Company.Fuser_id)

        return self.work_common_query(query, **kwargs)

    def add_work(self, **kwargs):
        t = WeddingCompanyPhotoProduct()

        t.Fname = kwargs.get('name')
        t.Fmerchant_id  = kwargs.get('merchant_id')
        t.Fuser_id      = kwargs.get('user_id')
        t.Fcategory     = kwargs.get('category')
        t.Fcolor        = kwargs.get('color')
        t.Fstyle        = kwargs.get('style')
        t.Fsale_price   = kwargs.get('sale_price')
        t.Fdescription  = kwargs.get('description')
        t.Fcover_img    = kwargs.get('cover_img')

        self.db.add(t)
        self.db.commit()
        self.add_work_images(t.Fid, kwargs.get('images'))

    def add_work_images(self, work_id, images):
        data = ujson.loads(images)

        for key in data.keys():
            img = WeddingCompanyPhotoProductImages()
            img.Fphoto_product_id = work_id
            img.Fimg_id = data[key].get('id')
            img.Furl = self.db.query(Photos.Fimage_url).filter(Photos.Fid==data[key].get('id')).scalar()
            img.Fdescription = data[key].get('desc')
            try:
                img.Fsort = int(key)
            except ValueError:
                img.Fsort = 0
            self.db.add(img)

        self.db.commit()

    def delete_work_images(self, **kwargs):
        query = self.db.query(WeddingCompanyPhotoProductImages).filter(WeddingCompanyPhotoProductImages.Fdeleted==0)

        if kwargs.get('work_id'):
            query = query.filter(WeddingCompanyPhotoProductImages.Fphoto_product_id==kwargs.get('work_id'))
            query.update({WeddingCompanyPhotoProductImages.Fdeleted: 1})

        if kwargs.get('img_id'):
            query = query.filter(WeddingCompanyPhotoProductImages.Fimg_id==kwargs.get('img_id'))
            query.update({WeddingCompanyPhotoProductImages.Fdeleted: 1})

        self.db.commit()

    def query_work_images(self, **kwargs):
        query = self.db.query(WeddingCompanyPhotoProductImages).filter(WeddingCompanyPhotoProductImages.Fdeleted==0)

        if kwargs.get('work_id'):
            query = query.filter(WeddingCompanyPhotoProductImages.Fphoto_product_id==kwargs.get('work_id'))

        if kwargs.get('img_id'):
            query = query.filter(WeddingCompanyPhotoProductImages.Fimg_id==kwargs.get('img_id'))

        if kwargs.get('order_by', 'Fsort'):
            query = query.order_by(kwargs.get('order_by', 'Fsort'))

        return query

    def update_work(self, work_id, **kwargs):
        if work_id:
            t = {}

            t['Fname'] = kwargs.get('name')
            t['Fmerchant_id']  = kwargs.get('merchant_id')
            t['Fuser_id']      = kwargs.get('user_id')
            t['Fcategory']     = kwargs.get('category')
            t['Fcolor']        = kwargs.get('color')
            t['Fstyle']        = kwargs.get('style')
            t['Fsale_price']   = kwargs.get('sale_price')
            t['Fdescription']  = kwargs.get('description')
            t['Fcover_img']    = kwargs.get('cover_img')

            query = self.db.query(WeddingCompanyPhotoProduct).filter(WeddingCompanyPhotoProduct.Fdeleted==0).filter(WeddingCompanyPhotoProduct.Fid==work_id)
            if query.scalar():
                query.update(t)
                self.db.commit()
                self.delete_work_images(work_id=work_id)
                self.add_work_images(work_id, kwargs.get('images'))

    def delete_work(self, work_id):
        if work_id:
            query = self.db.query(WeddingCompanyPhotoProduct).filter(WeddingCompanyPhotoProduct.Fdeleted==0).filter(WeddingCompanyPhotoProduct.Fid==work_id)
            query.update({WeddingCompanyPhotoProduct.Fdeleted: 1})
            self.db.commit()
            self.delete_work_images(work_id=work_id)

    def min_and_max_price(self, merchant_id):
        query = self.db.query(func.min(WeddingCompanyPhotoProduct.Fsale_price), func.max(WeddingCompanyPhotoProduct.Fsale_price)).\
                        filter(WeddingCompanyPhotoProduct.Fmerchant_id==merchant_id).filter(WeddingCompanyPhotoProduct.Fdeleted==0)

        return query.one()
