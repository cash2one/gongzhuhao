# encoding:utf-8
__author__ = 'sunlifeng'

from contants import Constant

import urllib2
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MenuManager:
    accessUrl = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx35567001c17ac9a1&secret=9fa4da870bb86024193991c99790f3eb"
    delMenuUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token="
    createUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token="
    getMenuUri = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token="
    USER_ID = '1'

    def getAccessToken(self):
        f = urllib2.urlopen(self.accessUrl)
        accessT = f.read().decode("utf-8")
        jsonT = json.loads(accessT)
        return jsonT["access_token"]

    def delMenu(self, accessToken):
        html = urllib2.urlopen(self.delMenuUrl + accessToken)
        result = json.loads(html.read().decode("utf-8"))
        return result["errcode"]

    def createMenu(self, accessToken):
        menu = '{"button":[' \
                    '{"type":"view","name":"精品案例","url":"http://test-yijiaren.zenmez.com/weixin/merchants/product/index/%s/lastest"},' \
                    '{"type":"view","name":"业主日记","url":"http://test-yijiaren.zenmez.com/weixin/merchants/article/index/%s"},' \
                    '{"name":"更多","sub_button":[' \
                            '{"type":"click","name":"联系我们","key":"%s"}' \
                            ']' \
                    '}' \
                    ']' \
                '}' %(self.USER_ID, self.USER_ID, Constant.EVENT_CONTACT)

        print self.createUrl + accessToken+menu.encode('utf-8')
        data = urllib2.urlopen(self.createUrl + accessToken, menu.encode('utf-8'))

        return data.code

    def getMenu(self, accessToken):
        html = urllib2.urlopen(self.getMenuUri + accessToken)
        print(html.read().decode("utf-8"))


if __name__ == "__main__":
    wx = MenuManager()
    accessToken = wx.getAccessToken()

    action = 3  #1：删除，2：创建，3，删除&创建

    if action == 1 or action == 3:
        rtnCode = wx.delMenu(accessToken)   #删除菜单
        if rtnCode == 0:
            print('delete ok!')
        else:
            print('delete error,code=' + rtnCode)

    if action == 2 or action == 3:
        rtnCode = wx.createMenu(accessToken)    #创建菜单
        if rtnCode == 200:
            print('create ok!')
        else:
            print('create error,code=' + rtnCode)

    wx.getMenu(accessToken)    #获取菜单