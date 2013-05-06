# encoding: utf-8
from __future__ import absolute_import

from contextlib import contextmanager
import os
import subprocess
import sys

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

from PIL import Image

from needle.diff import ImageDiff
from needle.driver import NeedleWebDriver, NeedleWebElement


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

    # TODO: More robust env handling:
    use_perceptualdiff = os.environ.get('NEEDLE_USE_PERCEPTUALDIFF', False)

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

    def assertScreenshot(self, element_or_selector, filename, threshold=0.1):
        """assert-style variant of compareScreenshot context manager

        compareScreenshot() can be considerably more efficient for recording baselines by avoiding the need
        to load pages before checking whether we're actually going to save them. This function allows you
        to continue using normal unittest-style assertions if you don't need the efficiency benefits
        """

        with self.compareScreenshot(element_or_selector, filename, threshold=threshold):
            pass

    @contextmanager
    def compareScreenshot(self, element_or_selector, filename, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        :param element_or_selector:
            Either a CSS selector as a string or a
            :py:class:`~needle.driver.NeedleWebElement` object that represents
            the element to capture.
        :param name:
            A name for the screenshot, which will be appended with ``.png``.
        :param threshold:
            The threshold for triggering a test failure.
        """

        if not isinstance(filename, basestring):
            raise NotImplementedError

        baseline_file = os.path.join(self.baseline_directory, '%s.png' % filename)
        output_file = os.path.join(self.output_directory, '%s.png' % filename)

        if self.capture and os.path.exists(baseline_file):
            self.skipTest('Not capturing %s, image already exists. If you '
                          'want to capture this element again, delete %s'
                          % (filename, baseline_file))

        yield

        if not isinstance(element_or_selector, NeedleWebElement):
            element = self.driver.find_element_by_css_selector(element_or_selector)
        else:
            element = element_or_selector

        if self.capture:
            element.get_screenshot().save(baseline_file)
            return
        else:
            screenshot = element.get_screenshot()
            screenshot.save(output_file)

            if self.use_perceptualdiff:
                diff_filename = output_file.replace(".png", ".diff.ppm")
                try:
                    # BUG: figure out how best to convert threshold distances to pixel counts
                    subprocess.check_call(["perceptualdiff", "-output", diff_filename,
                                           baseline_file, output_file])
                except subprocess.CalledProcessError:
                    raise AssertionError("The saved screenshot for '%s' did not match "
                                         "the screenshot captured: see %s"
                                         % (filename, diff_filename))
            else:
                baseline_image = Image.open(baseline_file)

                diff = ImageDiff(screenshot, baseline_image)
                distance = abs(diff.get_distance())
                if distance > threshold:
                    raise AssertionError("The saved screenshot for '%s' did not match "
                                         "the screenshot captured (by a distance of %.2f)"
                                         % (filename, distance))
