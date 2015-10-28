#encoding:utf-8
__author__ = 'binpo'

f = open('file','rb')
content = f.readline()
while content:
    print "'"+content.split('=')[0].strip()+"',"
    content = f.readline()
