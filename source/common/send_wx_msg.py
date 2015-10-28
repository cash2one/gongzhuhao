__author__ = 'binpo'


owner_user_id = project_info.owner_user_id
user_db = UserServices(self.db)
owner_user_info = user_db.get_user_by_id(owner_user_id)
open_id = owner_user_info.weixin
if open_id:
    keyword1 = time.strftime("%Y-%m-%d", time.localtime()) + '-' + str(proj_remark.id)
    keyword2 = ''
    if proj_remark.category == 'remark':
        keyword2 = '变更备案'
    elif proj_remark.category == 'report':
        keyword2 = '进度汇报'
    elif proj_remark.category == 'notice':
        keyword2 = '通知'
    elif proj_remark.category == 'up_photo':
        keyword2 = '工地检查'
    keyword3 = proj_remark.evaluation
    keyword4 = cache_table.get_decorate_stage(stage_id=project_info.stage_id) if project_info.stage_id else ''  #装修阶段
    open_id = str(open_id.strip())
    keyword1 =  str(keyword1.strip())
    keyword2 =  str(keyword2.strip())
    keyword3 =  str(keyword3.strip())
    keyword4 =  str(keyword4.strip())
    wx_util.send_msg_to_owner(access_token, open_id, keyword1, keyword2, keyword3, keyword4)