import math
from needle.diff import ImageDiff
from PIL import Image, ImageDraw
import unittest2

class TestImageDiff(unittest2.TestCase):
    def test_nrmsd_all_channels(self):
        image_a = Image.new('RGB', (100, 100), (255, 255, 255))
        image_b = Image.new('RGB', (100, 100), (0, 0, 0))
        diff = ImageDiff(image_a, image_b)
        self.assertEqual(diff.get_nrmsd(), 1)

    def test_nrmsd_half_filled(self):
        image_a = Image.new('RGB', (100, 100), (0, 0, 0))
        image_b = Image.new('RGB', (100, 100), (0, 0, 0))
        # Fill in half one rectangle
        draw_b = ImageDraw.Draw(image_b)
        draw_b.rectangle(
            ((0, 0), (49, 100)),
            fill=(255, 255, 255)
        )
        diff = ImageDiff(image_a, image_b)
        self.assertEqual(diff.get_nrmsd(), math.sqrt(0.5))

    def test_nrmsd_one_channel(self):
        image_a = Image.new('RGB', (100, 100), (255, 0, 0))
        image_b = Image.new('RGB', (100, 100), (0, 0, 0))
        diff = ImageDiff(image_a, image_b)
        self.assertEqual(diff.get_nrmsd(), math.sqrt(1.0/3.0))


