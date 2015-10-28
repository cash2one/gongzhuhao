#encoding:utf-8
__author__ = 'binpo'

from setting import MARK_IMG
try:
    import Image, ImageEnhance
except:
    from PIL import Image, ImageEnhance


POSITION = ('LEFTTOP','RIGHTTOP','CENTER','LEFTBOTTOM','RIGHTBOTTOM')
PADDING = 18
MARKIMAGE = MARK_IMG


def water_img_check(imageW):
    if imageW < 150:
        k = '15.png'
    elif imageW < 400:
        k = '20.png'
    elif imageW < 800:
        k = '40.png'
    elif imageW < 1200:
        k = '60.png'
    # elif imageW < 1200:
    #     k = 100
    # elif imageW < 1400:
    #     k =128
    # elif imageW < 1800:
    #     k= 156
    # elif imageW < 2200:
    #     k = 192
    # elif imageW < 2600:
    #     k = 256
    else:
        k = '150.png'
    return k



def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im

def watermark(im, original_witdh, position=POSITION[3], opacity=0.8):
    """Adds a watermark to an image."""
    #im = Image.open(imagefile)

    #水印图片宽高

    #original_witdh, original_height= Image.open(im).size
    #

    mark_prefix = 'static/water_mark/'+water_img_check(original_witdh)
    mark = Image.open(mark_prefix)

    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    # create a transparent layer the size of the image and draw the
    # watermark in that layer.
    layer = Image.new('RGBA', im.size, (0,0,0,0))
    if position == 'title':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))
    elif position == 'scale':
        # scale, but preserve the aspect ratio
        ratio = min(
            float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
        w = int(mark.size[0] * ratio)
        h = int(mark.size[1] * ratio)
        mark = mark.resize((w, h))
        layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))

    elif position == POSITION[0]:
        #lefttop
        position = (PADDING,PADDING)
        layer.paste(mark, position)

    elif position == POSITION[1]:
        #righttop
        position = (im.size[0] - mark.size[0]-PADDING, PADDING)
        layer.paste(mark, position)

    elif position == POSITION[2]:
        #center
        position = ((im.size[0] - mark.size[0])/2,(im.size[1] - mark.size[1])/2)
        layer.paste(mark, position)
    elif position == POSITION[3]:
        #left bottom
        position = (PADDING,im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
    else:
        #right bottom (default)
        position = (im.size[0] - mark.size[0]-PADDING, im.size[1] - mark.size[1]-PADDING,)
        layer.paste(mark, position)
    # composite the watermark with the layer

    return Image.composite(layer, im, layer)



def test():

    # watermark('1.jpg',MARKIMAGE,POSITION[0],opacity=0.7).save("watermarked_lt.jpg",quality=90)
    # watermark('1.jpg',MARKIMAGE,POSITION[1],opacity=0.7).save("watermarked_rt.jpg",quality=90)
    # watermark('1.jpg',MARKIMAGE,POSITION[2],opacity=0.7).save("watermarked_center.jpg",quality=90)
    watermark('1.jpg',MARKIMAGE,POSITION[3],opacity=0.9).save("watermarked_lb1.jpg")
    # watermark('1.jpg',MARKIMAGE,POSITION[4],opacity=0.7).save("watermarked_rb.jpg",quality=90)
    # watermark('1.jpg',MARKIMAGE,'title',opacity=0.7).save("watermarked_title.jpg",quality=90)
    # watermark('1.jpg',MARKIMAGE,'scale',opacity=0.7).save("watermarked_scale.jpg",quality=90)
if __name__ == '__main__':
    test()
