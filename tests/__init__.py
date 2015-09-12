import sys

from PIL import Image, ImageDraw

if sys.version_info >= (3, 0):
    from io import BytesIO as IOClass
else:
    try:
        from cStringIO import StringIO as IOClass
    except ImportError:
        from StringIO import StringIO as IOClass


class ImageTestCaseMixin(object):

    def get_image(self, colour):
        return Image.new('RGB', (100, 100), colour)

    def get_black_image(self):
        return self.get_image((0, 0, 0))

    def get_white_image(self):
        return self.get_image((255, 255, 255))

    def get_half_filled_image(self):
        im = self.get_black_image()
        draw = ImageDraw.Draw(im)
        draw.rectangle(
            ((0, 0), (49, 100)),
            fill=(255, 255, 255)
        )
        return im

    def load_black_div(self, text=''):
        self.driver.load_html('''
            <style type="text/css">
                #black-box {
                    position: absolute;
                    left: 50px;
                    top: 100px;
                    width: 100px;
                    height: 100px;
                    background-color: black;
                    color: white;
                }
            </style>
            <div id="black-box">%s</div>
        ''' % text)

    def save_image_to_fh(self, im):
        fh = IOClass()
        im.save(fh, 'PNG')
        fh.seek(0)
        return fh