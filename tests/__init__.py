from PIL import Image, ImageDraw
from StringIO import StringIO

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

    def save_image_to_fh(self, im):
        fh = StringIO()
        im.save(fh, 'PNG')
        fh.seek(0)
        return fh

