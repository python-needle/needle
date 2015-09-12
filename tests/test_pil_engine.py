from __future__ import absolute_import
import os
from os import path

from needle.cases import NeedleTestCase
from tests import ImageTestCaseMixin


class PILEngineTests(ImageTestCaseMixin, NeedleTestCase):
    engine_class = 'needle.engines.pil_engine.Engine'
    output_directory = 'tests/screenshots/'
    baseline_directory = 'tests/screenshots/baseline/'

    def setUp(self):
        # Remove all screeshots from previous test runs
        screenshots_path = path.join(path.dirname(__file__), 'screenshots')
        screenshots = [ f for f in os.listdir(screenshots_path) if f.endswith(".png") ]
        for screenshot in screenshots:
            os.remove(path.join(screenshots_path, screenshot))
        super(PILEngineTests, self).setUp()

    def test_assertScreenshot_success(self):
        self.load_black_div()
        self.assertScreenshot(
            self.driver.find_element_by_id('black-box'),
            'black-box'
        )

    def test_assertScreenshot_failure(self):
        with self.assertRaises(AssertionError):
            self.load_black_div('hello')
            self.assertScreenshot(
                self.driver.find_element_by_id('black-box'),
                'black-box'
            )