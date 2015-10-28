#encoding:utf-8
__author__ = 'binpo'

#from image_code import ImageHandler
#from common.loginHander import *
#from common.weibo_oauth.weibo_handler import *
#from common.qq_oauth.qq_handler import *
#from msg_handler import MsgSendHandler
#from comment_handler import *
#from errors import *

# from common.weiboHandler import *
# from common.weibo_handler import WeiboAuthHandler

from common.loginHander import *
from img import ImgHandler
handlers = [
    ('/loginout', LogoutHandler),
    ('/gzh/ops/login', AdminLoginHandler),
    ('/common/img/upload/([\w\W]*)', ImgHandler),
]
