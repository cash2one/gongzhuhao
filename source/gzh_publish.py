#!/usr/bin/python

import os
import stat
import shutil
import time
import zipfile

#常量
zip_name = 'gongzhuhao.zip'
svn_folder_path='./gongzhuhao'
svn_folder_name='gongzhuhao'
temp_folder_path0='./tempsdfaewf'
temp_folder_path=os.path.join(temp_folder_path0, 'gongzhuhao')
delete_file_type=['.Git','.pyc']    #删除指定的文件扩展名的文件
delete_file_name=['.DS_Store', 'simsunb.ttf']    #删除指定的文件名的文件
delete_folder_name=['.Git']    #删除指定的文件目录名的文件
delete_folder_path_name=['docs', 'unit_test', 'temp', '.idea']    #删除相对于svn_folder_path下的目录路径名的文件

#目录路径整理,将相对目录路径变成绝对路径名
for idx in range(0,len(delete_folder_path_name)):
    delete_folder_path_name[idx] = os.path.join(temp_folder_path, delete_folder_path_name[idx])


#消息常量
MSG_NO_SVN_FOLDER=u'没有找到svn工程目录，请拷贝本文件到svn工程目录的同级目录。'
MSG_DELETE_FOLDER_FAIL=u'临时目录删除失败。'

#清空目录
def clean_dir(Dir,is_del_self=True):
    if os.path.isdir( Dir ):
        paths = os.listdir( Dir )
        for path in paths:
            filePath = os.path.join( Dir, path )
            if os.path.isfile( filePath ):
                try:
                    os.remove( filePath )
                except os.error:
                    pass
                    #autoRun.exception( "remove %s error." %filePath )    #引入logging
            elif os.path.isdir( filePath ):
                shutil.rmtree(filePath, True)
    return True

#删除文件
def clean_dir2(Dir):
    for base,dirs,files in os.walk(Dir):
        for filename in files:
            if filename in delete_file_name:    #根据文件名删除指定的文件
                os.remove(os.path.join(base, filename))

            ext_name = os.path.splitext(filename)
            if ext_name in delete_file_type:    #根据文件类型删除指定的文件
                os.remove(os.path.join(base, filename))
        for dirname in dirs:
            absolute_path = os.path.join(base, dirname)
            if dirname in delete_folder_name:    #根据目录名删除指定的目录
                shutil.rmtree(absolute_path,True)
            
            if absolute_path in delete_folder_path_name:    #根据目录路径名删除指定的目录
                shutil.rmtree(absolute_path,True)
    return True

#更新svn
def updateSvn(strUser, strPwd, strUpPath):  
    strExec = "svn update %s --username %s --password %s --no-auth-cache" %(strUpPath, strUser, strPwd);  
    nRet = os.system(strExec);  
    return (0 == nRet);  

#压缩
def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))
            for name in dirs:
                filelist.append(os.path.join(root, name))
         
    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

#主程序
if __name__== '__main__':
    print u"开始"
    #检查
    if not os.path.exists(svn_folder_path):    #没有找到svn工程目录
        print MSG_NO_SVN_FOLDER
        exit()
        
    #svn更新
    print u'svn更新开始'
    ret = updateSvn('sunli', '111111', svn_folder_name)
    if ret:
        print u'svn更新结束'
    else:
        print u'svn更新失败'
        exit()
    
    #清理临时文件夹
    print u'开始清理临时文件夹'
    if os.path.exists(temp_folder_path0):
        if not clean_dir(temp_folder_path0):
        	print MSG_DELETE_FOLDER_FAIL
        	exit()
        shutil.rmtree(temp_folder_path0,True)
    
    time.sleep(3)    #等待3秒钟
    print u'完成清理临时文件夹'
    
    #拷贝svn工程目录到临时文件夹
    print u'开始拷贝svn工程'
    shutil.copytree(svn_folder_path,temp_folder_path)
    time.sleep(3)    #等待3秒钟
    print u'完成拷贝svn工程'
    
    #删除无用文件
    print u'开始删除无用文件'
    clean_dir2(temp_folder_path)
    time.sleep(3)    #等待3秒钟
    print u'完成删除无用文件'
    
    #压缩
    if os.path.exists(os.path.join('.', zip_name)):    #存在zip文件，需删除
        os.remove(os.path.join('.', zip_name))
        time.sleep(3)    #等待3秒钟
    print u'开始压缩'
    zip_dir(temp_folder_path0, os.path.join('.', zip_name))
    print u'完成压缩'
    
    #清理临时文件夹
    print u'开始清理临时文件夹'
    if os.path.exists(temp_folder_path0):
        if not clean_dir(temp_folder_path0):
        	print MSG_DELETE_FOLDER_FAIL
        	exit()
        shutil.rmtree(temp_folder_path0,True)
    
    time.sleep(3)    #等待3秒钟
    print u'完成清理临时文件夹'
    
    print u"完成"

