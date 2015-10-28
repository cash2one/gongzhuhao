#encoding:utf-8

__author__ = 'sunlifeng'

import urllib2
import json

import setting


def getMenuStr(menus, menu_codes, user_id):
    all_menu_str = ""
    for menu in menus:
        if menu_codes.find(menu.code) > -1:
            menu_str = ''
            if menu.is_sub == 1:#子菜单
                exist_parent = False
                #查找父菜单
                if all_menu_str.find("\"name\":\"" + str(menu.parent_name)) > -1:
                    exist_parent = True

                if exist_parent:#存在父菜单
                    the_left_1 = all_menu_str[:all_menu_str.index("\"name\":\"" + str(menu.parent_name))]
                    the_right_1 = all_menu_str[all_menu_str.index("\"name\":\"" + str(menu.parent_name)):]
                    the_right_1_left_1 = the_right_1[:the_right_1.index("}")+1]
                    the_left = the_left_1 + the_right_1_left_1
                    the_right = all_menu_str[len(the_left):]

                    menu_str = menu_str + "\"type\":\"" + str(menu.type) + "\","
                    menu_str = menu_str + "\"name\":\"" + str(menu.name) + "\","
                    if menu.type == "view":
                        if menu.is_common == 0: #非公共，需关联id
                            menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url %(user_id)) + "\""
                        else:
                            menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url) + "\""
                    elif menu.type == "click":
                        menu_str = menu_str + "\"key\":\"" + str(menu.key) + "\""
                    menu_str = "{" + menu_str + "}"
                    all_menu_str = the_left + "," + menu_str + the_right
                else:
                    #先添加父菜单
                    menu_parent_str = ""
                    menu_parent_str = menu_parent_str + "\"name\":\"" + str(menu.parent_name) + "\","
                    menu_parent_str = menu_parent_str + "\"sub_button\":[%s]"

                    #再添加当前子菜单
                    menu_str = menu_str + "\"type\":\"" + str(menu.type) + "\","
                    menu_str = menu_str + "\"name\":\"" + str(menu.name) + "\","
                    if menu.type == "view":
                        if menu.is_common == 0: #非公共，需关联id
                            menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url %(user_id)) + "\""
                        else:
                            menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url) + "\""
                    elif menu.type == "click":
                        menu_str = menu_str + "\"key\":\"" + str(menu.key) + "\""

                    menu_str = "{" + menu_str + "}"
                    menu_parent_str = menu_parent_str %(menu_str)
                    menu_parent_str = "{" + menu_parent_str + "}"
                    if all_menu_str == '' or all_menu_str.endswith(","):
                        all_menu_str = all_menu_str + menu_parent_str
                    else:
                        all_menu_str = all_menu_str + "," + menu_parent_str
            else:
                menu_str = menu_str + "\"type\":\"" + str(menu.type) + "\","
                menu_str = menu_str + "\"name\":\"" + str(menu.name) + "\","
                if menu.type == "view":
                    if menu.is_common == 0: #非公共，需关联id
                        menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url %(user_id)) + "\""
                    else:
                        menu_str = menu_str + "\"url\":\"" + str(setting.WX_APP_URL + menu.url) + "\""
                elif menu.type == "click":
                    menu_str = menu_str + "\"key\":\"" + str(menu.key) + "\""
                menu_str = "{" + menu_str + "}"
                if all_menu_str == '' or all_menu_str.endswith(","):
                    all_menu_str = all_menu_str + menu_str
                else:
                    all_menu_str = all_menu_str + "," + menu_str

    all_menu_str = '{"button":[' + all_menu_str + ']}'
    all_menu_str = all_menu_str.replace("},]", "}]")
    all_menu_str = all_menu_str.replace(",\"sub_button\":[]", "")

    return all_menu_str

def getAccessToken(app_id, app_secret):
        '''
        获取令牌
        :param app_id:微信分配的应用id
        :param app_secret:微信分配的应用密钥
        :return:微信服务器返回的结果json
        '''
        f = urllib2.urlopen(setting.WX_ACCESS_URL %(app_id, app_secret))
        access_j = f.read().decode("utf-8")
        access_Token = json.loads(access_j)
        return access_Token

def get_jsapi_ticket(access_Token):
        '''
        获取jsapi_ticket
        :param app_id:微信分配的access_Token
        :return:微信服务器返回的结果json
        '''
        f = urllib2.urlopen(setting.WX_JSAPI_TICKET %(access_Token))
        jsapi_ticket = f.read().decode("utf-8")
        jsapi_ticket = json.loads(jsapi_ticket)
        return jsapi_ticket

def send_template_msg(access_token, msg):
    '''
    发送模板数据
    :param access_token
    :return:msg:数据，需json格式
    '''
    f = urllib2.urlopen(SEND_TEMPLATE_MESSAGE %(access_token), msg)
    result = f.read().decode("utf-8")
    result = json.loads(result)
    return result

def send_msg_to_owner(access_token,open_id,jsonText,exception_capture=None,**kargs):
    '''
    :todo 发送模版消息
    :param access_token:
    :param open_id:
    :param kargs:
        template_id  模版ID
        link         点击链接
        keyword1     关键字1
        keyword2     关键字2
        keyword3     关键字3
        keyword4     关键字4
        remark       描述
    :return:
    '''

    # 2，准备数据


    jsonText= jsonText.replace("touser_value", open_id)
    jsonText= jsonText.replace("template_id_value",  kargs.get('template_id','_HOPHNeIoaMa8AXvXERn4BQfVmSUdhArZ1MMSGdrUHg'))

    jsonText= jsonText.replace("url_value", kargs.get('link'))

    if kargs.get('first'):
        jsonText= jsonText.replace("first_value", kargs.get('first',''))
        jsonText= jsonText.replace("first_color", '#000000')

    if kargs.get('keyword1'):
        jsonText= jsonText.replace("keyword1_value", kargs.get('keyword1'))
        jsonText= jsonText.replace("keyword1_color", '#000000')
    if kargs.get('keyword2'):
        jsonText= jsonText.replace("keyword2_value", kargs.get('keyword2'))
        jsonText= jsonText.replace("keyword2_color", '#000000')

    if kargs.get('keyword3'):
        jsonText= jsonText.replace("keyword3_value", kargs.get('keyword3'))
        jsonText= jsonText.replace("keyword3_color", '#000000')
    if kargs.get('keyword4'):
        jsonText= jsonText.replace("keyword4_value", kargs.get('keyword4'))
        jsonText= jsonText.replace("keyword4_color", '#000000')

    if kargs.get('keyword5'):
        jsonText= jsonText.replace("keyword5_value", kargs.get('keyword5'))
        jsonText= jsonText.replace("keyword5_color", '#000000')

    if kargs.get('OrderSn'):
        jsonText= jsonText.replace("OrderSn_value", kargs.get('OrderSn'))
        jsonText= jsonText.replace("OrderSn_color", '#000000')

    if kargs.get('OrderSn'):
        jsonText= jsonText.replace("OrderSn_value", kargs.get('OrderSn'))
        jsonText= jsonText.replace("OrderSn_color", '#000000')

    if  kargs.get('remark'):
        jsonText= jsonText.replace("remark_value", kargs.get('remark','祝您在拍摄期间心情愉快，准备的详情信息请点击‘详情’'))
        jsonText= jsonText.replace("remark_color", '#000000')

    # 3，发送
    dic_result = send_template_msg(access_token, str(jsonText))
    if dic_result and dic_result.get('errmsg')=='ok':
        pass
    else:#发送失败，则另外发送短信
        pass

#常量地址
SEND_TEMPLATE_MESSAGE = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s'
