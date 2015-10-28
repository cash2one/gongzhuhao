#encoding:utf-8
__author__ = 'sunlifeng'


def is_mobile(user_agent):
    '''
    是否来源手机
    :param useragent:
    :return:
    '''
    user_agent = user_agent.lower()


    #微信
    is_weixin = user_agent.find('micromessenger') > -1
    if is_weixin:
        return 3

    #iphone
    is_iphone = user_agent.find('iphone') > -1
    if is_iphone:
        return 1

    #android
    is_android = user_agent.find('android') > -1
    if is_android:
        return 2

    return 0

def get_url_source_example(useragent):
    '''
    获取访问来源样例
    :param useragent:
    :return:
    '''
    #iphone
    is_iphone = useragent.find('iphone') > -1
    if is_iphone:
        return 'iphone'

    #android
    is_android = useragent.find('android') > -1
    if is_android:
        return 'android'

    #微信
    is_weixin = useragent.find('micromessenger') > -1
    if is_weixin:
        return 'weixin'

    #ipad
    is_ipad = useragent.find('ipad') > -1
    if is_ipad:
        return 'ipad'

    #ipod
    is_ipod = useragent.find('ipod') > -1
    if is_ipod:
        return 'ipod'

    #pc电脑
    is_pc = useragent.find('windows nt') > -1
    if is_pc:
        return 'pc'

    return 'other'
