# encoding: utf-8
from __future__ import absolute_import
from __future__ import print_function

from warnings import warn
from contextlib import contextmanager
from errno import EEXIST
import os
import sys
import time

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

if sys.version_info >= (3, 0):
    basestring = str

from PIL import Image

from selenium.common.exceptions import WebDriverException

from needle.engines.pil_engine import ImageDiff
from needle.driver import (NeedleFirefox, NeedleChrome, NeedleIe, NeedleOpera,
                           NeedleSafari, NeedleWebElementMixin)

DRIVER_ACQUISITION_TIMEOUT = 5  # seconds


def _object_filename(obj):
    return os.path.abspath(sys.modules[type(obj).__module__].__file__)


def import_from_string(path):
    """
    Utility function to dynamically load a class specified by a string,
    e.g. 'path.to.my.Class'.
    """
    module_name, klass = path.rsplit('.', 1)
    module = __import__(module_name, fromlist=[klass])
    return getattr(module, klass)


class NeedleTestCase(TestCase):
    """
    A `unittest2 <http://www.voidspace.org.uk/python/articles/unittest2.shtml>`_
    test case which provides tools for testing CSS with Selenium.
    """

    driver = None

    capture = False  # Deprecated
    save_baseline = False
    cleanup_on_success = False

    viewport_width = 1024
    viewport_height = 768

    output_directory = None
    baseline_directory = None

    engine_class = 'needle.engines.pil_engine.Engine'

    @classmethod
    def setUpClass(cls):
        if os.environ.get('NEEDLE_CAPTURE'):
            cls.capture = True
        if os.environ.get('NEEDLE_SAVE_BASELINE'):
            cls.save_baseline = True
        if os.environ.get('NEEDLE_CLEANUP_ON_SUCCESS'):
            cls.cleanup_on_success = True

        # Instantiate the diff engine
        klass = import_from_string(cls.engine_class)
        cls.engine = klass()

        cls.driver = cls.get_web_driver()
        cls.driver.set_window_position(0, 0)
        cls.set_viewport_size(cls.viewport_width, cls.viewport_height)
        super(NeedleTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        if isinstance(cls.driver, NeedlePhantomJS):
            # Workaround for https://github.com/SeleniumHQ/selenium/issues/767
            cls.driver.service.send_remote_shutdown_command()
            cls.driver.service._cookie_temp_file = None
        cls.driver.quit()
        super(NeedleTestCase, cls).tearDownClass()

    @classmethod
    def get_web_driver(cls):
        """
        Returns the WebDriver instance to be used. Defaults to `NeedleFirefox()`.
        Override this method if you'd like to control the logic for choosing
        the proper WebDriver instance.
        """
        browser_name = os.environ.get('NEEDLE_BROWSER')
        browser_map = {
            'firefox': NeedleFirefox,
            'chrome': NeedleChrome,
            'ie': NeedleIe,
            'opera': NeedleOpera,
            'safari': NeedleSafari,
            'phantomjs': NeedlePhantomJS,
        }
        browser_class = browser_map.get(browser_name, NeedleFirefox)
        # Allow a few retries to get the driver, in case it isn't quite ready yet
        start_time = time.time()
        while True:
            try:
                browser = browser_class()
                break
            except Exception as e:
                if (not isinstance(e, WebDriverException)) and e.__class__.__name__ != 'WebDriverException':
                    # nose likes to change selenium's WebDriverException to "nose.proxy.WebDriverException"
                    raise
                if time.time() - start_time >= DRIVER_ACQUISITION_TIMEOUT:
                    raise
                time.sleep(1)
        return browser

    def __init__(self, *args, **kwargs):
        super(NeedleTestCase, self).__init__(*args, **kwargs)
        # TODO: should output directory be timestamped?
        if self.output_directory is None:
            self.output_directory = os.environ.get('NEEDLE_OUTPUT_DIR', os.path.realpath(os.path.join(os.getcwd(), 'screenshots')))
        # TODO: Should baseline be a top-level peer to output_directory?
        if self.baseline_directory is None:
            self.baseline_directory = os.environ.get('NEEDLE_BASELINE_DIR', os.path.realpath(os.path.join(os.getcwd(), 'screenshots', 'baseline')))

        # Create the output and baseline directories if they do not yet exist.
        for dirname in (self.baseline_directory, self.output_directory):
            # Recursively create the directory, handling its
            # prior existence as a valid exception.
            # This will guard against race conditions.
            # E.g. when running tests in multithreaded mode
            # they likely have the same directories specified
            # and might encounter this block at the same time.
            try:
                os.makedirs(dirname)
            except OSError as err:
                if err.errno == EEXIST and os.path.isdir(dirname):
                    pass
                else:
                    raise

    @classmethod
    def set_viewport_size(cls, width, height):
        cls.driver.set_window_size(width, height)

        # Measure the difference between the actual document width and the
        # desired viewport width so we can account for scrollbars:
        measured = cls.driver.execute_script("return {width: document.body.clientWidth, height: document.body.clientHeight};")
        delta = width - measured['width']

        cls.driver.set_window_size(width + delta, height)

    def assertScreenshot(self, element_or_selector, file, threshold=0, exclude=None):
        """assert-style variant of compareScreenshot context manager

        compareScreenshot() can be considerably more efficient for recording baselines by avoiding the need
        to load pages before checking whether we're actually going to save them. This function allows you
        to continue using normal unittest-style assertions if you don't need the efficiency benefits
        :param exclude: list of Selectors of the elements to be excluded for image comparison
            (A mask is applied to the elements)
        """

        with self.compareScreenshot(element_or_selector, file, threshold=threshold, exclude=exclude):
            pass

    @contextmanager
    def compareScreenshot(self, element_or_selector, file, threshold=0, exclude=None):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        :param element_or_selector:
            Either a CSS selector as a string or a
            :py:class:`~needle.driver.NeedleWebElementMixin` object that represents
            the element to capture.
        :param file:
            If a string, then assumed to be the filename for the screenshot,
            which will be appended with ``.png``. Otherwise assumed to be
            a file object for the baseline image.
        :param threshold:
            The threshold for triggering a test failure.
        :param exclude: list of Selectors of the elements to be excluded for image comparison.
            (A mask is applied to the elements)
        """

        yield  # To allow using this method as a context manager
        NeedleWebElementMixin.driver = self.driver
        if not isinstance(element_or_selector, NeedleWebElementMixin):
            element = self.driver.find_element_by_css_selector(element_or_selector)
        else:
            element = element_or_selector

        if not isinstance(file, basestring):
            # Comparing in-memory files instead of on-disk files
            baseline_image = Image.open(file).convert('RGB')
            fresh_screenshot = element.get_screenshot(exclude)
            diff = ImageDiff(fresh_screenshot, baseline_image)
            distance = abs(diff.get_distance())
            if distance > threshold:
                raise AssertionError("The new screenshot did not match "
                                     "the baseline (by a distance of %.2f)"
                                     % distance)
        else:
            baseline_file = os.path.join(self.baseline_directory, '%s.png' % file)
            output_file = os.path.join(self.output_directory, '%s.png' % file)

            # Determine whether we should save the baseline image
            save_baseline = False
            if self.save_baseline:
                save_baseline = True
            elif self.capture:
                warn("The 'NeedleTestCase.capture' attribute and '--with-save-baseline' nose option "
                     "are deprecated since version 0.2.0. Use 'save_baseline' and '--with-save-baseline' "
                     "instead. See the changelog for more information.",
                     PendingDeprecationWarning)
                if os.path.exists(baseline_file):
                    self.skipTest('Not capturing %s, its baseline image already exists. If you '
                                  'want to capture this element again, delete %s'
                                  % (file, baseline_file))
                else:
                    save_baseline = True
            if self.driver.capabilities.get('deviceName') is None:
                required_width = self.driver.execute_script('return document.body.parentNode.scrollWidth')
                required_height = self.driver.execute_script('return document.body.parentNode.scrollHeight')
                self.driver.set_window_size(required_width, required_height)
            if save_baseline:
                # Save the baseline screenshot and bail out
                element.get_screenshot(exclude).save(baseline_file)
                return
            else:
                if not os.path.exists(baseline_file):
                    raise IOError('The baseline screenshot %s does not exist. '
                                  'You might want to re-run this test in baseline-saving mode.'
                                  % baseline_file)

                # Save the new screenshot
                element.get_screenshot(exclude).save(output_file)

                try:
                    self.engine.assertSameFiles(output_file, baseline_file, threshold)
                except:
                    raise
                else:
                    if self.cleanup_on_success:
                        os.remove(output_file)