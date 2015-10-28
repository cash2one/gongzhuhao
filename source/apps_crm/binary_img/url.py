from apps_crm.binary_img.binary_img_handler import BinaryImgHandler,UserInoutUrlQrcreaterHandler
handlers=[
    (r'/common/tools/binary_img/([\d]{1,28})/',BinaryImgHandler),
    (r'/common/tools/qrcode/',UserInoutUrlQrcreaterHandler),

]
