# encoding:utf-8
import tornado
from common.base import BaseHandler
from services.shares.shares_service import ShareServices
from models.share_do import ShareWishes,PotentialCustomer,UserPhotosShare
from models.album_do import Albums
from common.permission_control import company_permission_control

share_service = ShareServices()
class MerchantOrdersShareHandler(BaseHandler):

    @tornado.web.authenticated
    @company_permission_control('share_view')
    def get(self, *args, **kwargs):
        share_service.set_db(self.db)
        query = share_service.query_shares_by_merchant_id(self.get_current_user().get('Fmerchant_id'))
        page_data = self.get_page_data(query)
        page_html = page_data.render_page_html()
        self.echo('crm/merchant/_list.html',{'page_data':page_data,'page_html':page_html},layout='crm/common/base.html')

    def get_potential_customer_count(self,share_id):
        '''
            祝福和潜在客户总数
        '''
        wishes = self.db.query(ShareWishes).filter(ShareWishes.Fuser_photos_share_id==share_id).count()
        customers = self.db.query(PotentialCustomer).filter(PotentialCustomer.Fuser_photos_share_id==share_id).count()
        return wishes,customers

    def get_type_and_share_name(self,share_id):
        '''
        :todo
        :param share_id:
        :return:
        '''
        try:
            album_id = self.db.query(UserPhotosShare.Falbum_id).filter(UserPhotosShare.Fid==share_id).scalar()
            album = self.db.query(Albums).filter(Albums.Fid==album_id).scalar()
            if album:
                return album.Fablum_name,album.Falbum_type
        except:
            return '',''
        #Falbum_id
