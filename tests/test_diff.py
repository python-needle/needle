import math
from needle.diff import ImageDiff
from PIL import Image, ImageDraw
import unittest2

class TestImageDiff(unittest2.TestCase):
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

    def test_nrmsd_all_channels(self):
        diff = ImageDiff(self.get_white_image(), self.get_black_image())
        self.assertEqual(diff.get_nrmsd(), 1)

    def test_nrmsd_one_channel(self):
        diff = ImageDiff(self.get_image((255, 0, 0)), self.get_black_image())
        self.assertEqual(diff.get_nrmsd(), math.sqrt(1.0 / 3))

    def test_nrmsd_half_filled(self):
        diff = ImageDiff(self.get_black_image(), self.get_half_filled_image())
        self.assertEqual(diff.get_nrmsd(), math.sqrt(0.5))

    def test_distance_all_channels(self):
        diff = ImageDiff(self.get_white_image(), self.get_black_image())
        self.assertAlmostEqual(diff.get_distance(), 100 * 100, delta=0.001)

    def test_distance_one_channel(self):
        diff = ImageDiff(self.get_image((255, 0, 0)), self.get_black_image())
        self.assertAlmostEqual(diff.get_distance(), 10000.0 / 3, delta=0.001)

    def test_distance_half_filled(self):
        diff = ImageDiff(self.get_black_image(), self.get_half_filled_image())
        self.assertAlmostEqual(diff.get_distance(), 10000.0 / 2, delta=0.001)



