# encoding: utf-8
from __future__ import absolute_import

import os
import sys

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

from PIL import Image

from needle.diff import ImageDiff
from needle.driver import NeedleWebDriver


def _object_filename(obj):
    return os.path.abspath(sys.modules[type(obj).__module__].__file__)


class NeedleTestCase(TestCase):
    """
    A `unittest2 <http://www.voidspace.org.uk/python/articles/unittest2.shtml>`_
    test case which provides tools for testing CSS with Selenium.
    """
    #: An instance of :py:class:`~needle.driver.NeedleWebDriver`, created when
    #: each test is run.
    driver = None

    driver_command_executor = 'http://127.0.0.1:4444/wd/hub'
    driver_desired_capabilities = {
        'browserName': os.environ.get('NEEDLE_BROWSER', 'firefox'),
    }
    driver_browser_profile = None

    capture = False

    @classmethod
    def setUpClass(cls):
        if os.environ.get('NEEDLE_CAPTURE'):
            cls.capture = True
        cls.driver = cls.get_web_driver()
        super(NeedleTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(NeedleTestCase, cls).tearDownClass()
        cls.driver.quit()

    @classmethod
    def get_web_driver(cls):
        return NeedleWebDriver(cls.driver_command_executor,
                               cls.driver_desired_capabilities,
                               cls.driver_browser_profile)

    def __init__(self, *args, **kwargs):
        super(NeedleTestCase, self).__init__(*args, **kwargs)
        # TODO: should output directory be timestamped?
        self.output_directory = os.environ.get('NEEDLE_OUTPUT_DIR', os.path.realpath(os.path.join(os.getcwd(), 'screenshots')))
        # TODO: Should baseline be a top-level peer to output_directory?
        self.baseline_directory = os.environ.get('NEEDLE_BASELINE_DIR', os.path.realpath(os.path.join(os.getcwd(), 'screenshots', 'baseline')))

    def assertScreenshot(self, element, name, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        :param element: Either a CSS selector as a string or a
                        :py:class:`~needle.driver.NeedleWebElement` object that
                        represents the element to capture.
        :param name: A name for the screenshot, which will be appended with
                     ``.png``.
        :param threshold: The threshold for triggering a test failure.
        """
        if isinstance(element, basestring):
            element = self.driver.find_element_by_css_selector(element)

        if not isinstance(name, basestring):
            raise NotImplementedError  # This needs to be reconciled below without worsening code-smell
            # names can be filehandles for testing. This sucks - we
            # should write out files to their correct location
            filename = name

        baseline_file = os.path.join(self.baseline_directory, '%s.png' % name)
        output_file = os.path.join(self.output_directory, '%s.png' % name)

        if self.capture:
            if os.path.exists(baseline_file):
                self.skipTest('Not capturing %s, image already exists. If you '
                              'want to capture this element again, delete %s'
                              % (name, baseline_file))
            element.get_screenshot().save(baseline_file)
        else:
            screenshot = element.get_screenshot()
            screenshot.save(output_file)

            baseline_image = Image.open(baseline_file)

            diff = ImageDiff(screenshot, baseline_image)
            distance = abs(diff.get_distance())
            if distance > threshold:
                raise AssertionError("The saved screenshot for '%s' did not match "
                                     "the screenshot captured (by a distance of %.2f)"
                                     % (name, distance))
