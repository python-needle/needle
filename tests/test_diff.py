import math
import sys

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase


from needle.diff import ImageDiff
from . import ImageTestCaseMixin

class TestImageDiff(ImageTestCaseMixin, TestCase):
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



