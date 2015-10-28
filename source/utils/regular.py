#encoding:utf-8

__author__ = 'binpo'


import re

class Regular(object):

    @classmethod
    def check_phone(cls,phone):
        pattern = re.compile(r'^1[3|4|7|5|8][0-9]\d{4,8}$')#r'^1\d{10}$|^(0\d{2,3}-?|\(0\d{2,3}\))?[1-9]\d{4,7}(-\d{1,8})?$'
                             #^'1[3|4|5|8][0-9]\d{4,8}$' )
        match = pattern.match(phone)
        if match and match.group():
            return True
        return False

    @classmethod
    def check_email(self,email):
        # pattern = re.compile(r'(www\.)?\w+@\w+\.\w+\.?\w*')
        pattern = re.compile(r'^[\w\d]+[\d\w\_\.]+@([\d\w]+)\.([\d\w]+)(?:\.[\d\w]+)?$')
        match = pattern.match(email)
        if match and match.group():
            return True
        return False

    @classmethod
    def check_birthday(self,email):
        pattern = re.compile(r'(\d{4})-\d{2}-\d{2}$')
        match = pattern.match(email)
        if match and match.group():
            years = int(match.groups()[0])
            if years < 1900 or years > 2015:
                return False
            else:
                return True
        return False

    @classmethod
    def is_zh(cls,content):
        '''
        :todo 判断字符串是否有中文
        '''
        content = content.decode('utf-8')
        hpattern = re.compile(u'[\u4e00-\u9fa5]+')
        match = hpattern.search(content)
        if match and match.group():
            return True
        else:
            return False

    @classmethod
    def is_num(cls, content):
        '''
        :todo 判断输入字符串是否全为数字，返回int
        '''
        m = re.match(r'^(\d+)$', content)
        if m:
            return int(m.groups()[0])
        else:
            return False

if __name__=='__main__':
    # pattern = re.compile(r'^1\d{10}$|^(0\d{2,3}-?|\(0\d{2,3}\))?[1-9]\d{4,7}(-\d{1,8})?$')
    # match = pattern.match('18268802385')
    # if match:
    #     print match.group()
    #print Regular.check_phone('18269882s385')
    #print Regular.check_email('www.213_@163.www.cn')
    #print Regular.check_birthday('1912-23-23')
    #print Regular.is_zh('aaa中国asdsds')
    print Regular.is_num('s1232311213')

