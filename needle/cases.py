from needle.diff import ImageDiff
from needle.driver import NeedleWebDriver
import os
from PIL import Image
import sys
import unittest2

def _object_filename(obj):
    return os.path.abspath(sys.modules[type(obj).__module__].__file__)

class NeedleTestCase(unittest2.TestCase):
    driver_url = 'http://127.0.0.1:4444/wd/hub'
    driver_browser = 'firefox'
    driver_platform = None
    driver_version = ''
    driver_javascript_enabled = True

    capture = False

    def __call__(self, *args, **kwargs):
        self.driver = self.get_web_driver()
        super(NeedleTestCase, self).__call__(*args, **kwargs)
        self.driver.close()
    
    def get_web_driver(self):
        return NeedleWebDriver(
            self.driver_url,
            self.driver_browser,
            self.driver_platform,
            self.driver_version,
            self.driver_javascript_enabled,
        )

    def assertElementEqualsImage(self, element, name, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        A name is required for the screenshot, which will be appended with ``.png``.
        """
        filename = os.path.join(
            os.path.dirname(_object_filename(self)),
            '%s.png' % name
        )
        if self.capture:
            if os.path.exists(filename):
                self.skipTest('Not capturing %s, image already exists. If you '
                              'want to capture this element again, delete %s'
                              % (name, filename))
            element.get_screenshot().save(filename)
        else:
            image = Image.open(filename)
            diff = ImageDiff(element.get_screenshot(), image)
            self.assertAlmostEqual(diff.get_distance(), 0, delta=threshold)


    

