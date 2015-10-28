#encoding:utf-8
import traceback
import uuid
import sys

import tornado
from models.company_do import Company
from services.company.company_services import CompanyServices
from services.weixin.wx_services import WxService
import setting
from utils import wx_util
from wx_menu_manager import MenuManager
import json

__author__ = 'sunlifeng'

from common.base import AdminBaseHandler

class WeixinListHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, name=None):
        company_db = CompanyServices(self.db)
        query = company_db.get_companys()

        if name:
            query = query.filter(Company.Fcompany_name.like("%"+name+"%"))

        page_data=self.get_page_data(query)
        self.echo('ops/weixin/list.html',{
            'name':name,
            'companies':page_data.result,
            'page_html':'',
        })

class WeixinDetailHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, company_id):
        if not company_id:
            return self.echo('view/login/404.html', layout='')

        company_db = CompanyServices(self.db)
        company = company_db.get_company_by_id(int(company_id))

        app_url = ''
        if company.Fapp_url:
            app_url = company.Fapp_url
        else:
            app_url = setting.WX_APP_URL + '/' + str(company.Fid)  #使用公司id作为app url的关键参数
            company_db.update_company_by_id(company.Fid, Fapp_url=app_url)

        app_token = ''
        if company.Fapp_token:
            app_token = company.Fapp_token
        else:
            uuid_str = uuid.uuid3(uuid.NAMESPACE_DNS, str(company.Fid)+str(company.Fuser_id))   #使用id+user_id生产uuid作为token
            app_token = str(uuid_str)
            app_token = app_token.replace('-', '')
            company_db.update_company_by_id(company.Fid, Fapp_token=app_token)

        self.echo('ops/weixin/detail.html',{
            'company':company,
            'app_url':app_url,
            'app_token':app_token,
        })

    @tornado.web.authenticated
    def post(self, company_id):
        #界面参数解析
        self.get_paras_dict()

        rspDic = {}
        rspDic["stat"] = "ok"   #返回页面的字典,ok,fail
        rspDic["msg"] = ""

        if not company_id:
            rspDic["stat"] = "fail"
            rspDic["msg"] = u"公司不存在"
            return self.write(json.dumps(rspDic))

        try:
            dic_app = {}
            dic_app['Fapp_url'] = self.qdict.get('app_url')
            dic_app['Fapp_token'] = self.qdict.get('app_token')
            app_id = self.qdict.get('app_id')
            dic_app['Fapp_id'] = app_id.strip()
            app_secret = self.qdict.get('app_secret')
            dic_app['Fapp_secret'] = app_secret.strip()

            #check
            menuManager = MenuManager()
            access_Token = menuManager.getAccessToken(dic_app['Fapp_id'], dic_app['Fapp_secret'])
            if access_Token.has_key('errcode'):
                rspDic["stat"] = "fail"
                rspDic["msg"] = u"验证失败"
            else:
                company_db = CompanyServices(self.db)
                company_db.update_company_by_id(int(company_id), **dic_app)
        except Exception, e:
            print e
            rspDic["stat"] = "fail"
            rspDic["msg"] = u"微信绑定失败"

        return self.write(json.dumps(rspDic))

class WeixinDeleteHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, company_id):
        if not company_id:
            return self.echo('view/login/404.html', layout='')

        company_db = CompanyServices(self.db)
        company = company_db.get_company_by_id(int(company_id))

        self.echo('ops/weixin/delete.html',{
            'company':company,
        })

    @tornado.web.authenticated
    def post(self, company_id):
        rspDic = {}
        rspDic["stat"] = "ok"   #返回页面的字典,ok,fail
        rspDic["msg"] = ""

        if not company_id:
            rspDic["stat"] = "fail"
            rspDic["msg"] = u"公司不存在"
            return self.write(json.dumps(rspDic))

        try:
            company_db = CompanyServices(self.db)
            company = company_db.get_company_by_id(int(company_id))
            if company.Fmenu_codes:
                rspDic["stat"] = "fail"
                rspDic["msg"] = u"解除绑定前，请先解除菜单绑定！"
                return self.write(json.dumps(rspDic))

            dic_app = {}
            dic_app['Fapp_url'] = ''
            dic_app['Fapp_token'] = ''
            dic_app['Fapp_id'] = ''
            dic_app['Fapp_secret'] = ''

            company_db = CompanyServices(self.db)
            company_db.update_company_by_id(int(company_id), **dic_app)
        except Exception, e:
            rspDic["stat"] = "fail"
            rspDic["msg"] = u"微信删除失败"

        return self.write(json.dumps(rspDic))

class WeixinMenuHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, company_id):
        if not company_id:
            return self.echo('view/login/404.html', layout='')

        company_db = CompanyServices(self.db)
        query = company_db.get_companys()
        query = query.filter(Company.Fid == int(company_id))
        company = query.scalar()

        #获取menu code对应的菜单名称
        wxService = WxService(self.db)
        company_menu_name = ''
        if company.Fmenu_codes:
            for code in company.Fmenu_codes.split(','):
                if len(code) > 0:
                    company_menu_name = company_menu_name + ',' + wxService.query_name_by_code(code)
            company_menu_name = company_menu_name.strip(',')
        else:
            company.Fmenu_codes = ''

        #查询所有菜单
        wxService = WxService(self.db)
        menus = wxService.query_menus()
        for menu in menus:
            if menu.type == 'view':
                menu.url = setting.WX_APP_URL + menu.url
                print 'menu.url=' + menu.url
                if menu.is_common == 0: #url中存在参数
                    menu.url = menu.url %(company.Fuser_id)

        self.echo('ops/weixin/menu.html',{
            'error':'',
            'company':company,
            'company_menu_name':company_menu_name,
            'menus':menus,
            'page_html':'',
        })

class WeixinMenuBindHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, company_id, menu_code):
        if not company_id:
            return self.echo('view/login/404.html', layout='')

        error = u''
        company_db = CompanyServices(self.db)
        company = company_db.get_company_by_id(int(company_id))
        wxService = WxService(self.db)

        #获取当前menu code对应的菜单名称
        company_menu_name = ''
        if company.Fmenu_codes:
            for code in company.Fmenu_codes.split(','):
                if len(code) > 0:
                    company_menu_name = company_menu_name + ',' + wxService.query_name_by_code(code)
            company_menu_name = company_menu_name.strip(',')

        #查询当前所有菜单
        menus = wxService.query_menus()

        try:
            #获取当前所有的菜单code列表
            '''
            lst_menu_codes = []
            if company.Fmenu_codes:
                for code in company.Fmenu_codes.split(','):
                    if len(code) > 0:
                        lst_menu_codes.append(code)
            else:
                company.Fmenu_codes = ''
            if len(lst_menu_codes) >= 3:
                error = u'当前用户已经绑定3个主菜单，不能再绑定'
                raise error
            '''

            menu_codes = '' #新menu codes
            if company.Fmenu_codes.find(menu_code) > -1:  #已绑定
                menu_codes = company.Fmenu_codes
            else:
                menu_codes = company.Fmenu_codes + ',' + menu_code

            #整理code顺序
            menu_codes_order = ''
            menus = wxService.query_menus()
            for menu in menus:
                if menu_codes.find(menu.code) > -1:
                    menu_codes_order = menu_codes_order + ',' + menu.code
            menu_codes = menu_codes_order.strip(',')

            #更新公众号菜单
            menus = wxService.query_menus()
            all_menu_str = wx_util.getMenuStr(menus, menu_codes, company.Fuser_id)
            print("all_menu_str="+all_menu_str)
            menuManager = MenuManager()
            dic_accessToken = menuManager.getAccessToken(company.Fapp_id, company.Fapp_secret)
            print 'dic_accessToken' + str(dic_accessToken)
            result =  menuManager.refreshMenu(dic_accessToken.get("access_token"), all_menu_str)
            if result <> 'ok':
                error = u'绑定失败'
                raise error

            #更新menu_codes
            if menu_codes <> company.Fmenu_codes:
                company_db.update_company_by_id(int(company_id), Fmenu_codes=menu_codes)

            #获取menu code对应的菜单名称
            company_menu_name = ''
            if menu_codes:
                for code in menu_codes.split(','):
                    if len(code) > 0:
                        company_menu_name = company_menu_name + ',' + wxService.query_name_by_code(code)
                company_menu_name = company_menu_name.strip(',')
            else:
                company.Fmenu_codes = ''

            #查询所有菜单
            menus = wxService.query_menus()
            for menu in menus:
                if menu.type == 'view':
                    menu.url = setting.WX_APP_URL + menu.url
                    if menu.is_common == 0: #url中存在参数
                        menu.url = menu.url %(company.Fuser_id)

            self.echo('ops/weixin/menu.html',{
                'error':error,
                'company':company,
                'company_menu_name':company_menu_name,
                'menus':menus,
                'page_html':'',
            })
        except Exception,e:
            e = sys.exc_info()[0](traceback.format_exc())
            print(e)

            self.echo('ops/weixin/menu.html',{
                'error':error,
                'company':company,
                'company_menu_name':company_menu_name,
                'menus':menus,
                'page_html':'',
            })

class WeixinMenuUnBindHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def get(self, company_id, menu_code):
        if not company_id:
            return self.echo('view/login/404.html', layout='')

        error = u''
        company_db = CompanyServices(self.db)
        company = company_db.get_company_by_id(int(company_id))
        wxService = WxService(self.db)

        #获取当前menu code对应的菜单名称
        company_menu_name = ''
        if company.Fmenu_codes:
            for code in company.Fmenu_codes.split(','):
                if len(code) > 0:
                    company_menu_name = company_menu_name + ',' + wxService.query_name_by_code(code)
            company_menu_name = company_menu_name.strip(',')

        #查询当前所有菜单
        menus = wxService.query_menus()

        try:
            wxService = WxService(self.db)
            error = u''

            company_db = CompanyServices(self.db)
            query = company_db.get_companys()
            query = query.filter(Company.Fid == int(company_id))
            company = query.scalar()

            menu_codes = ''
            if company.Fmenu_codes.find(menu_code) > -1:  #已绑定
                menu_codes = company.Fmenu_codes.replace(menu_code, '')
            else:
                menu_codes = company.Fmenu_codes

            #整理code顺序
            menu_codes_order = ''
            menus = wxService.query_menus()
            for menu in menus:
                if menu_codes.find(menu.code) > -1:
                    menu_codes_order = menu_codes_order + ',' + menu.code
            menu_codes = menu_codes_order.strip(',')

            #更新公众号菜单
            menuManager = MenuManager()
            dic_accessToken = menuManager.getAccessToken(company.Fapp_id, company.Fapp_secret)
            if len(menu_codes) == 0:#
                menuManager.delMenu(dic_accessToken.get("access_token"))
            else:
                menus = wxService.query_menus()
                all_menu_str = wx_util.getMenuStr(menus, menu_codes, company.Fuser_id)
                print("all_menu_str="+all_menu_str)

                result =  menuManager.refreshMenu(dic_accessToken.get("access_token"), all_menu_str)
                if result <> 'ok':
                    error = u'绑定失败'
                    raise error

            #更新menu_codes
            if menu_codes <> company.Fmenu_codes:
                company_db.update_company_by_id(int(company_id), Fmenu_codes=menu_codes)

            #获取menu code对应的菜单名称
            company_menu_name = ''
            if menu_codes:
                for code in menu_codes.split(','):
                    if len(code) > 0:
                        company_menu_name = company_menu_name + ',' + wxService.query_name_by_code(code)
                company_menu_name = company_menu_name.strip(',')
            else:
                company.Fmenu_codes = ''

            #查询所有菜单
            wxService = WxService(self.db)
            menus = wxService.query_menus()
            for menu in menus:
                if menu.type == 'view':
                    menu.url = setting.WX_APP_URL + menu.url
                    if menu.is_common == 0: #url中存在参数
                        menu.url = menu.url %(company.Fuser_id)

            self.echo('ops/weixin/menu.html',{
                'error':error,
                'company':company,
                'company_menu_name':company_menu_name,
                'menus':menus,
                'page_html':'',
            })
        except Exception,e:
            e = sys.exc_info()[0](traceback.format_exc())
            print(e)

            self.echo('ops/weixin/menu.html',{
                'error':error,
                'company':company,
                'company_menu_name':company_menu_name,
                'menus':menus,
                'page_html':'',
            })

class WeixinCheckHandler(AdminBaseHandler):
    @tornado.web.authenticated
    def post(self):
        #界面参数解析
        self.get_paras_dict()

        status = 'ok'
        if not self.qdict.get('app_id') or not self.qdict.get('app_secret'):
            status = 'fail'
        else:
            menuManager = MenuManager()
            app_id = self.qdict.get('app_id')
            app_id = app_id.strip()
            app_secret = self.qdict.get('app_secret')
            app_secret = app_secret.strip()
            access_Token = menuManager.getAccessToken(app_id, app_secret)
            if access_Token.has_key('errcode'):
                status = 'fail'

        self.write(json.dumps({'stat':status}))
