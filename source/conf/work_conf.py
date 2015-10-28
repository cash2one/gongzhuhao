#encoding:utf-8
__author__ = 'frank'

#类型
_WORK_TYPE = [['wedding','婚纱摄影'],['traveling','旅游婚纱']]

#风格
_WORK_STYLE = [
                ['korean', '韩式'], ['documentary', '纪实风'], ['small_fresh', '小清新'],
                ['sexy', '性感'], ['personality', '个性'], ['court', '宫廷'], ['chinese', '中式'],
                ['magazine', '杂志'],['user_writing','自己写']
]

_WORK_STYLE_WX = {
                'korean':'韩式','documentary':'纪实风','small_fresh':'小清新',
                'sexy':'性感','personality':'个性','court':'宫廷','chinese':'中式',
                'magazine':'杂志'
                }
_WORK_STYLE_APP = [{'key':'korean','value':'韩式'},{'key':'documentary','value':'纪实风'},{'key':'small_fresh','value':'小清新'},
    {'key':'sexy','value':'性感'},{'key':'personality','value':'个性'},{'key':'court','value':'宫廷'},{'key':'chinese','value':'中式'},
    {'key':'magazine','value':'杂志'}]

#拍摄场景
_SHOOTING_SCENE = {
    'indoor':{'solid_color':'纯色背景','green_house':'花房','palace_castle':'宫殿-城堡','home':'居家场景','personality_shop':'个性小店',
              'theatre':'剧院','library':'图书馆','z_indoor_user_writing':'自己写'},
    'outdoor':{
        'green_flower':'绿地花海','church':'教堂','characteristic_building':'特色建筑','street_snap':'街拍','amusement_park':'游乐场',
        'campus':'校园','z_outdoor_user_writing':'自己写'
    }
}

_SHOOTING_SCENE_WX = {
            'solid_color':'纯色背景','green_house':'花房','palace_castle':'宫殿-城堡','home':'居家场景','personality_shop':'个性小店',
            'theatre':'剧院','library':'图书馆','green_flower':'绿地花海','church':'教堂','characteristic_building':'特色建筑',
            'street_snap':'街拍','amusement_park':'游乐场','campus':'校园'
}
_SHOOTING_SCENE_APP = [{'key':'solid_color','value':'纯色背景'},{'key':'green_house','value':'花房'},{'key':'palace_castle','value':'宫殿-城堡'},
    {'key':'home','value':'居家场景'},{'key':'personality_shop','value':'个性小店'},{'key':'theatre','value':'剧院'},{'key':'library','value':'图书馆'},
    {'key':'green_flower','value':'绿地花海'},{'key':'church','value':'教堂'},{'key':'characteristic_building','value':'特色建筑'},
    {'key':'street_snap','value':'街拍'},{'key':'amusement_park','value':'游乐场'},{'key':'campus','value':'校园'}]

#造型特色
_MODE_STYLE = [
                    ['slim','显瘦'], ['cover_the_arm','遮手臂'], ['explicit_face','显脸小'],
                    ['long_leg','显腿长'], ['thin_waist','显腰细'], ['nice','不挑人']
]

#拍摄地
_SHOOTING_SITE = [
    ['sanya','三亚'],['qingdao','青岛'],['shanghai','上海'],['xiamen','厦门'],['lijiang','丽江'],['macau','澳门'],['phuket','普吉岛'],
    ['bali','巴厘岛'],['jeju','济州岛'],['saipan','塞班岛'],['japan','日本'],['new zealand','新西兰'],['singapore','新加坡'],['europe','欧洲'],
    ['mauritius','毛里求斯'],['maldives','马尔代夫'],['australia','澳大利亚'],['user_writing','自己写'],
]
#, ['user_writing','自己写']

#拍摄场景2
_SHOOTING_SCENE_2 = [
                     ['sea','海景'],['dive','水下'],['pool','泳池园林'],['church','宫殿教堂'],['street','特色街景'],['launch','游艇游轮'],
                     ['cbd','景点地标'],['hotel','酒店内景'],['user_writing','自己写']
                    ]

_QUERY_PRICE = ['-4999','5000-7999','8000-12999','13000-']

_QUERY_PRICE_APP = [{'key':'-4999','value':'4999以下'},
                    {'key':'5000-7999','value':'5000-7999'},
                    {'key':'8000-12999','value':'8000-12999'},
                    {'key':'13000-','value':'13000以上'}]
PAGE_SIZE=20
PAGE_SIZE_APP = 6

SERIES_KEYS = ['Fid','Fmerchant_id','Fpackage_name','Fprice','Fsale_price',
                                                'Fbride_style_count','Fgroom_style_count',
                                                'Fcloth_select_type',
                                                'Fcloth_remark',
                                                'Foutdoor_space',
                                                'Finner_space',
                                                'Fspace_remark',
                                                'Fshot_desc',
                                                'Fphotographer_level',
                                                'Frecommend_photographer',
                                                'Farter_level',
                                                'Frecommend_arter',
                                                'Fphoto_album_desc',
                                                'Fphoto_frame_desc',
                                                'Fmv_desc',
                                                'Fother_desc',
                                                'Fdescription',
                                                'Fother_pay_desc',
                                                'Fcover_img','Ffavorite_count']

WORK_KEYS = [
                'Fid','Fmerchant_id','Fuser_id','Fproduct_type',
                'Fname','Fshot_space','Fshot_space_name','Fstyle_code',
                'Fstyle_name',
                'Fshot_scene_code',
                'Fshot_scene_name',
                'Fmode_style_code',
                'Fmode_style_name',
                'Fsale_price',
                'Ftitle',
                'Fdescription',
                'Fcover_img','Ffavorite_count'
            ]

#婚纱礼服作品分类
_WEDDING_DRESS_CATEGORY = {
    'female_dress': '女士婚纱',
    'male_dress': '男士礼服',
    'evening_dress': '晚礼服',
    'cheongsam': '旗袍'
}

#婚纱礼服作品颜色
_WEDDING_DRESS_COLOR = {
    'white': '白',
    'pink': '粉',
    'purple': '紫',
    'green': '绿',
    'golden': '金'
}

#婚纱礼服作品款式
_WEDDING_DRESS_STYLE = {
    '0': '抹胸', '1': '一字肩', '2': 'V领', '3': '单肩',
    '4': '吊带', '5': '挂脖', '6': '拖尾', '7': '鱼尾',
    '8': '蓬蓬裙', '9': 'A字裙', '10': '前短后拖', '11': '短裙',
    '12': '蕾丝', '13': '水晶', '14': '露背', '15': '镂空'
}

#婚庆公司作品分类
_WEDDING_COMPANY_CATEGORY = {
    'plan': '婚礼策划',
    'vip_plan': '高端婚礼定制'
}

#婚庆公司作品颜色
_WEDDING_COMPANY_COLOR = {
    'white': '白',
    'pink': '粉',
    'purple': '紫',
    'green': '绿',
    'golden': '金'
}

#婚庆公司作品风格
_WEDDING_COMPANY_STYLE = {
    '0': '奢华大气', '1': '唯美', '2': '小清新', '3': '复古',
    '4': '欧式宫廷'
}