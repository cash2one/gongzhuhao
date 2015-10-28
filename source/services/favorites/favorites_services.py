#encoding:utf-8
__author__ = 'wangjinkuan'

from services.base_services import BaseService
from models.favorites_do import UsersFavorites

class FavoritesService(BaseService):

    def create_favorite(self,**kwargs):
        '''
        todo:创建收藏
        :param kwargs:
        :return:
        '''

        query = self.db.query(UsersFavorites).filter(UsersFavorites.Fuser_id == kwargs.get('user_id'),
                                                     UsersFavorites.Ffavorites_id == kwargs.get('favorite_id'),
                                                     UsersFavorites.Ffavorites_type == kwargs.get('favorite_type','')
                                                    )
        if query.count() > 0:
            query.update({'Fdeleted':0})
        else:
            user_favorite = UsersFavorites()
            user_favorite.Fuser_id = kwargs.get('user_id','')
            user_favorite.Ffavorites_type = kwargs.get('favorite_type','')
            user_favorite.Ffavorites_id = kwargs.get('favorite_id','')

            self.db.add(user_favorite)

        self.db.commit()


    def query_favorite(self,**kwargs):
        '''
        todo:查询收藏
        :param kwargs:
        :return:
        '''
        query = self.db.query(UsersFavorites).filter(UsersFavorites.Fdeleted == 0)

        if kwargs.get('user_id',''):
            query = query.filter(UsersFavorites.Fuser_id == kwargs.get('user_id'))

        if kwargs.get('favorite_type',''):
            query = query.filter(UsersFavorites.Ffavorites_type == kwargs.get('favorite_type'))

        if kwargs.get('favorite_id',''):
            query = query.filter(UsersFavorites.Ffavorites_id == kwargs.get('favorite_id'))

        return query

    def update_favorite(self,**kwargs):
        '''
        todo:删除收藏
        :param kwargs:
        :return:
        '''
        query = self.query_favorite(**kwargs)
        query.update({'Fdeleted':1})
        self.db.commit()




# if kwargs.get('favorite_type') == 1:
#             self.db.query(Company).\
#                 filter(Company.Fdeleted == 0,Company.Fuser_id == kwargs.get('favorite_id')).\
#                     update({Company.Ffavorite_count:Company.Ffavorite_count+1},synchronize_session = False)
#
# elif kwargs.get('favorite_type') == 2:
#     self.db.query(ShotPackage).\
#         filter(ShotPackage.Fdeleted == 0,ShotPackage.Fid == kwargs.get('favorite_id')).\
#             update({ShotPackage.Ffavorite_count:ShotPackage.Ffavorite_count+1},synchronize_session = False)
#
# elif kwargs.get('favorite_type') == 3:
#     self.db.query(WeddingPhotoProduct).\
#         filter(WeddingPhotoProduct.Fdeleted == 0,WeddingPhotoProduct.Fid == kwargs.get('favorite_id')).\
#             update({WeddingPhotoProduct.Ffavorite_count:WeddingPhotoProduct.Ffavorite_count+1},synchronize_session = False)





