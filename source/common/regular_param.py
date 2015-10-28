# encoding:utf-8
import re
from tenjin_base import TenjinBase

# 批量模板 如: shd_date_0 --> shd_date_4
_PATTERNS_ENUM = {
    "shd_date_":        u'^[\d: -]{8,28}$',
    "shd_site_":        u'[^|&\'\"\\$;=]{0,128}',
    "shd_tips_":        u'[^|&\'\"\\$;=]{0,128}',
    "shd_stff_id_":     u'^[\d|&]{1,16}$',
    "shd_stff_tt_":     u'^[\u4e00-\u9fa5\w\s|&]{1,64}$',
    "shd_stff_nm_":     u'^[\u4e00-\u9fa5\w\s|&]{1,64}$',
    "ismodify_":        u'^[01]$',
    }

# 模板列表
_PATTERNS = {
    "_xsrf":            u'^[\w|]{16,512}',
    "user_name":        u'^[\u4e00-\u9fa5\w\s]{1,16}$',
    "user_name_ex":     u'^[\u4e00-\u9fa5\w\s]{1,16}$',
    "user_mobi":        u'^[0-9_-]{4,16}$',
    "user_mobi_ex":     u'^[0-9_-]{4,16}$',
    "user_birth":       u'^(\d{4})-\d{2}-\d{2}$',
    "user_birth_ex":    u'^(\d{4})-\d{2}-\d{2}$',
    "order_id":         u'^\d{1,28}$',
    "order_type":       u'^\d{1,2}$',
    "amount":           u'^[0-9]{1,12}(\.[0-9]{1,2})?$',
    "uid_stf":          u'^[0-9&]{1,64}$',
    "comment":          u'^[^|&\'\"\\$;=]{0,512}$',

    "Fcompany_name":    u'^[\u4e00-\u9fa5\w\s]{1,128}$',
    "Fprovince":        u'^[0-9]{1,7}$',
    "Fcity":            u'^[0-9]{1,7}$',
    "Farea":            u'^[0-9]{1,7}$',
    "Fdetail_address":  u'^[^|&\'\"\\$;=]{0,128}$',
    "Fcontact":         u'^[^|&\'\"\\$;=]{0,128}$',
    "Fphone":           u'^[0-9]{5,11}$',
    "Fqq":              u'^[1-9][0-9]{3,10}$',
    "Fmail":            u'^[\w@.]{1,64}$',
    "Fdescription":     u'^[^|\'\"$;]{0,128}$',
    "Fphoto_url":       u'^[\w:/.?=&]{0,512}$',

    "Fbirthday":        u'^(\d{4})-\d{2}-\d{2}$',
    "Femail":           u'^[\w@.]{1,64}$',
    "Fweibo":           u'^[^|&\'\"\\$;=]{0,128}$',
    "Fweixin":          u'^[^|&\'\"\\$;=]{0,128}$',
    "Fuser_pwd":        u'^[^|&\'\"\\$;=]{0,128}$',

    "Finfo":            u'^[^|&\'\"\\$;=]{0,128}$',
    }


class CheckHandler(TenjinBase):
    """HTTP参数检查"""

    def check_args(self, *args, **kwargs):
        """check requests arguments
        check rules:
            0 如果args和kwargs为空,检查request.arguments中所有参数
            1 不检查参数值与kwargs中的默认值相等的参数
            2 不检查在_PATTERNS中没有配正则的参数
            3 如果碰到不匹配的参数 返回此参数名
        args: 需要检查的字段列表
        kwargs: 包含默认值的字典
        """
        args_req = {a: None for a in args}
        if not args_req:  # check all of request args
            args_req = {a: None for a in self.request.arguments}
        args_req.update(kwargs)
        return self._do_check(args_req)

    def check_args_all(self):
        args_req = {a: None for a in self.request.arguments}
        return self._do_check(args_req)

    def _do_check(self, args_req):
        self.patterns_prepare()
        for name, default in args_req.items():
            if name not in _PATTERNS:
                continue
            val = self.get_argument(name) if default is None else \
                self.get_argument(name, default)
            if val == default:  # do not check default
                continue

            patt = re.compile(_PATTERNS[name])
            match = patt.match(val)
            if match and match.group():
                continue
            else:
                return name

    def patterns_prepare(self):
        patterns_new = {}
        for key, val in _PATTERNS_ENUM.items():
            for i in range(4):
                patterns_new[key+str(i)] = val
        _PATTERNS.update(patterns_new)
