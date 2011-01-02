from __future__ import with_statement
from needle.cases import NeedleTestCase
from PIL import Image
from . import ImageTestCaseMixin

class NeedleTestCaseTest(ImageTestCaseMixin, NeedleTestCase):
    def create_div(self):
        self.driver.load_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 100px; height: 100px; background-color: black"></div>')

    def test_assertAlmostEqual(self):
        self.create_div()
        self.assertElementEqualsImage(
            self.driver.find_element_by_id('test'), 
            self.save_image_to_fh(self.get_black_image())
        )

    def test_assertAlmostEqual_fails(self):
        self.create_div()
        im = self.get_black_image()
        # Create one red pixel
        im.putpixel((0, 0), (255, 0, 0))
        with self.assertRaises(AssertionError):
            # Default threshold for error is 0
            self.assertElementEqualsImage(
                self.driver.find_element_by_id('test'), 
                self.save_image_to_fh(im)
            )

    def test_assertAlmostEqual_does_not_fail_with_threshold(self):
        self.create_div()
        im = self.get_black_image()
        # Create one red pixel
        im.putpixel((0, 0), (255, 0, 0))
        self.assertElementEqualsImage(
            self.driver.find_element_by_id('test'), 
            self.save_image_to_fh(im),
            threshold=1
        )

    def test_assertAlmostEqual_fails_with_threshold(self):
        self.create_div()
        im = self.get_black_image()
        # Create two white pixels
        im.putpixel((0, 0), (255, 255, 255))
        im.putpixel((1, 0), (255, 255, 255))
        with self.assertRaises(AssertionError):
            self.assertElementEqualsImage(
                self.driver.find_element_by_id('test'), 
                self.save_image_to_fh(im),
                threshold=1
            )


