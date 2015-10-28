# encoding:utf_8
__author__ = 'morichounami'
from services.base_services import *
from models.staffer_do import *
import tempfile
from conf.merchant import _MERCHANG_DEPARTMENT_TITLES
from PIL import Image

class StafferServices(BaseService):
    def upload_to_server(http_handler, param_name, file_prex=None):
        '''
        员工头像上传
        :param http_handler:
        :param param_name:参数名
        :param file_prex:前缀
        :return:
        '''
        files = []
        file_metas = http_handler.request.files.get(param_name)
        for meta in file_metas:
            filename = meta['filename']  # 文件名(和桌面上的文件名相同)
            if file_prex:  # 如果有前缀 file_prex是指定好的，便于在服务器端建立文件夹
                save_name = ''.join((file_prex, '/', meta['filename']))
            else:
                save_name = meta['filename']
            #save_name=str(int(time.time()))+'.'+filename.split('.').pop() #将file_prex,'/',meta['filename'](filename)以‘’连接成一个字符串,并将值赋给save_name(图片上传的保存名)
            file_stream = meta['body']
            tf = tempfile.NamedTemporaryFile()
            tf.write(file_stream)
            tf.seek(0)
            try:
                UPLOAD_IMG_PATH = 'static/'
                img = Image.open(tf.name)
                img.thumbnail((100,100),resample=1)
                img.save(UPLOAD_IMG_PATH+save_name)
                tf.close()
            except Exception, e:
                print e
                return False, []
            files.append({'size':len(meta['body']),
                'full_name':UPLOAD_IMG_PATH+save_name,
                'file_name':filename,
                'content_type':meta['content_type'],
                })
        return True,files


    def get_staffers(self, uid_mct):
        """ 获取所有用户列表"""
        return self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fuid_mct == uid_mct)

    def get_staffer_by_id_(self, stf_id):
        return self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fid == stf_id).scalar()

    def get_staffer_by_id(self, uid_mct, stf_id):
        return self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fuid_mct == uid_mct,
            Staffers.Fid == stf_id).scalar()

    def update_staffer_by_id(self, stf_id, **kwargs):
        query = self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fid == stf_id)
        query.update(kwargs,synchronize_session=False)
        self.db.commit()

    def update_staffer_full_depart_name(self, dpt_id, dpt_name):
        query = self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fdepartment_id == dpt_id)
        dic_up = {'Fdepartment_name':dpt_name}
        query.update(dic_up,synchronize_session=False)
        self.db.commit()

    def delete_staffer_by_id(self, uid_mct, stf_id):
        staff = self.db.query(Staffers).filter(
            Staffers.Fdeleted == 0,
            Staffers.Fuid_mct == uid_mct,
            Staffers.Fid == stf_id).scalar()
        staff.Fdeleted=1
        self.db.add(staff)
        self.db.commit()

    def get_staffers_by_department_id(self, user_id, department_id):
        '''
        pass
        :param id:
        :return:
        '''
        if department_id:
            return self.db.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==user_id,Staffers.Fdepartment_id==str(department_id))
        else:
            return self.db.query(Staffers).filter(Staffers.Fdeleted==0,Staffers.Fuid_mct==user_id)


    def add_department_staff(self,user_id,department,username,phone,email,title):
        '''
        添加部门员工成
        :param user_id:     商户ID
        :param department:  商户的部门
        :param username:    用户名
        :param phone:       电话
        :param email:       邮件
        :param title:       职称
        :return:
        '''
        staffer = Staffers()
        staffer.Fuid_mct = user_id
        staffer.Fdepartment_id = department.Fid
        staffer.Fdepartment_name = department.Ffull_department_name
        staffer.Fname = username
        staffer.Fmobi = phone
        staffer.Femail = email
        staffer.Ftitle = title
        self.db.add(staffer)
        self.db.commit()
        return staffer

    def query_staffers(self,merchant_id=None,dept_id=None,**kwargs):
        query = self.db.query(Staffers).filter(Staffers.Fdeleted == 0)
        if merchant_id:
            query = query.filter(Staffers.Fuid_mct == merchant_id)
        if dept_id:
            query = query.filter(Staffers.Fdepartment_id == dept_id)
        if kwargs.get('start_date',''):
            query = query.filter(Staffers.Fcreate_time >= kwargs.get('start_date'))
        if kwargs.get('end_date',''):
            query = query.filter(Staffers.Fcreate_time <= kwargs.get('end_date')+' 23:59:59')
        if kwargs.get('staffer_name',''):
            content = kwargs.get('staffer_name')
            query = query.filter(Staffers.Fname.like('%'+content+'%'))
        if kwargs.get('staffer_title',''):
            index = kwargs.get('staffer_title')
            query = query.filter(Staffers.Ftitle == _MERCHANG_DEPARTMENT_TITLES[int(index)])
        return query


    def get_department_id_by_user(self,ids):
        return self.db.query(Staffers.Fdepartment_id).filter(Staffers.Fdeleted==0,Staffers.Fid.in_(ids))
    #     self.db.query(Department.Fid).filter()
    #
    #






