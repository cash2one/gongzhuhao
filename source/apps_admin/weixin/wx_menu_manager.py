# encoding:utf-8

__author__ = 'sunlifeng'

import urllib2
import json
import sys

import setting

reload(sys)
sys.setdefaultencoding('utf-8')

EVENT_CONTACT = 'EVENT_CONTACT'

class MenuManager:
    def getAccessToken(self, app_id, app_secret):
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

    def delMenu(self, accessToken):
        '''
        删除菜单
        :param accessToken: 令牌
        :return:错误码
        '''
        url = setting.WX_MENU_DELETE_URL + accessToken
        print(url)
        html = urllib2.urlopen(setting.WX_MENU_DELETE_URL + accessToken) #不能使用url
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]

    def createMenu(self, accessToken, menus):
        url = setting.WX_MENU_CREATE_URL + accessToken, menus.encode('utf-8')
        print menus
        print(url)
        data = urllib2.urlopen(setting.WX_MENU_CREATE_URL + accessToken, menus.encode('utf-8')) #不能使用url

        return data.code

    def getMenu(self, accessToken):
        url = setting.WX_MENU_GET_URL + accessToken
        #print(url)
        html = urllib2.urlopen(setting.WX_MENU_GET_URL + accessToken) #不能使用url
        print(html.read().decode("utf-8"))

    def refreshMenu(self, accessToken, menus):
        '''
        刷新菜单
        :param accessToken:令牌
        :return:状态
        '''

        result = 'ok'   #ok, fail

        #删除
        rtnCode = self.delMenu(accessToken)   #删除菜单
        if rtnCode <> 0:
            result = 'fail'
            return result

        rtnCode = self.createMenu(accessToken, menus)    #创建菜单
        if rtnCode == 200:
            result = 'ok'
            return result
        else:
            result = 'fail'
            return result

if __name__ == "__main__":

    wx = MenuManager()
    dic_accessToken = wx.getAccessToken('wx332996f6681c7e48', 'c49253b721257730db25f1a46a74a157')

    action = 4  #1：删除，2：创建，3，删除&创建

    if action == 1 or action == 3:
        rtnCode = wx.delMenu(dic_accessToken.get("access_token"))   #删除菜单
        if rtnCode == 0:
            print('delete ok!')
        else:
            print('delete error,code=' + rtnCode)

    if action == 2 or action == 3:
        rtnCode = wx.createMenu(dic_accessToken.get("access_token"), '')    #创建菜单
        if rtnCode == 200:
            print('create ok!')
        else:
            print('create error,code=' + rtnCode)

    wx.getMenu(dic_accessToken.get("access_token"))    #获取菜单