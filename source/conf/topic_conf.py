#encoding:utf-8
__author__ = 'wangjinkuan'

_TOPIC_ORDER = [
    {'num':0,'code':'Fcreate_time desc','name':'创建时间'},
    {'num':1,'code':'Flast_reply_time desc','name':'最后回复时间'}
]

TOPIC_KEYS = ['Fid','Fuser_id','Fcotegory_id','Ftitle',
              'Fcontent',
              'Ftotal_img',
              'Fis_top',
              'Ftop_end_date',
              'Fis_essence',
              'Fessence_expire_time',
              'Fis_hot',
              'Ftags',
              'Fis_lock',
              'Fpage_view',
              'Ftotal_assess',
              'Fpraise',
              'Fis_recommend',
              'Fedit_times',
              'Flast_edit_time',
              'Flast_reply_time'
             ]

TOPIC_CATEGORY_KES = [
                'Fid','Fname','Fcode',
                'Fparent_id',
                'Flevel',
                'Fsort',
                'Fimg_url',
                'Fdescription',
                'Fpage_view',
                'Ftopic_count'
               ]

BANNERS = ['Fid','Fbanner_type','Ftitle','Fimg_url','Flink_url','Finvalid_date']