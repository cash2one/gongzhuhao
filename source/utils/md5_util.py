#encoding:utf-8
'''
Created on 2014-6-1

@author: qiuyan.zwp
'''
import hashlib

def create_md5(args):
    md5_constructor = hashlib.md5
    return md5_constructor(args).hexdigest()
