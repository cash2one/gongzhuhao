#encoding:utf-8
__author__ = 'binpo'

# PASSWD_TEMPLATE='亲爱的客户，您在微信公众号“公主号”中查看订单排期的登陆密码:%s 登陆账号为%s【公主号】'
PASSWD_TEMPLATE = '%s已为您开通微信客服，关注微信《公主号》并登陆，即可查看您的拍摄信息。用户名:%s ,密码:%s 【公主号】'
CHECK_CODE_TEMPLATE='验证码:%s 【公主号】'

ORDER_CONFIRM_TEMPLATE='亲爱的客户，"%s"精修图已发送，请在微信公众号"公主号"中打开"我的照片"查看。【公主号】'   #订单通知

SCHEDULE_TEMPLATE='%s已为您设定%s排期,请关注微信《公主号》并用手机号登陆系统查看排期'

PHONE_REG_TEMPLATE='公主号注册验证码:%s 【公主号】'
PHONE_LOGIN_TEMPLATE='公主号登陆验证码:%s 【公主号】'



#微信模版#	拍摄服务提醒	其他	其他	详情   删除
WEIXIN_TEMPLATES={'shot_confirm':{
    'TEMPLATE_ID':'8tNOMZ8XMqeF3ocYhll-ZkwfoizLTnROCcmRaE4xMKM',
    'jsonText':'''{
    "touser": "touser_value",
    "template_id": "template_id_value",
    "url": "url_value",
    "topcolor": "#000000",
    "data": {
        "first": {
            "value": "first_value",
            "color": "first_color"
        },
        "keyword1": {
            "value": "keyword1_value",
            "color": "keyword1_color"
        },
        "keyword2": {
            "value": "keyword2_value",
            "color": "keyword2_color"
        },
        "keyword3": {
            "value": "keyword3_value",
            "color": "keyword3_color"
        },
        "remark": {
            "value": "remark_value",
            "color": "remark_color"
        }
    }
}'''
},
    'photo_confirm':{
    'TEMPLATE_ID':'CWOgu7mLVG-aWhc4gpSuFyWyaVNa2FhS7540LqeWGOA',
    'jsonText':'''{
    "touser": "touser_value",
    "template_id": "template_id_value",
    "url": "url_value",
    "topcolor": "#000000",
    "data": {
        "first": {
            "value": "first_value",
            "color": "#000000"
        },
        "keyword1": {
            "value": "keyword1_value",
            "color": "#000000"
        },
        "keyword2": {
            "value": "keyword2_value",
            "color": "#000000"
        },
        "keyword3": {
            "value": "keyword3_value",
            "color": "#000000"
        },
        "remark": {
            "value": "remark_value",
            "color": "#000000"
        }
    }
}'''

},
    'new_order_confirm':{
    'TEMPLATE_ID':'O7dogUBwWs1rqLFbYwqzFGDUkC7ZPEm6s9vEzv9lEW8',
    'jsonText': '''{
    "touser": "touser_value",
    "template_id": "template_id_value",
    "url": "url_value",
    "topcolor": "#000000",
    "data": {
        "first": {
            "value": "first_value",
            "color": "first_color"
        },
        "keyword1": {
            "value": "keyword1_value",
            "color": "keyword1_color"
        },
        "keyword2": {
            "value": "keyword2_value",
            "color": "keyword2_color"
        },
        "keyword3": {
            "value": "keyword3_value",
            "color": "keyword3_color"
        },
        "keyword4": {
            "value": "keyword4_value",
            "color": "keyword4_color"
        },
        "keyword5": {
            "value": "keyword5_value",
            "color": "keyword5_color"
        },
        "remark": {
            "value": "remark_value",
            "color": "remark_color"
        }
    }
}'''
},
    'order_change_confirm':{
    'TEMPLATE_ID':'YNXtBDjxklI74_G12UPRn5_fUdIhhoIb7HL-__kgnTQ',
    'jsonText':'''{
    "touser": "touser_value",
    "template_id": "template_id_value",
    "url": "url_value",
    "topcolor": "#000000",
    "data": {
        "first": {
            "value": "first_value",
            "color": "first_color"
        },
        "OrderSn": {
            "value": "OrderSn_value",
            "color": "OrderSn_color"
        },
        "OrderStatus": {
            "value": "OrderStatus_value",
            "color": "OrderStatus_color"
        },
        "remark": {
            "value": "remark_value",
            "color": "remark_color"
        }
    }
}'''
}
}
