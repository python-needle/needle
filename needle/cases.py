# encoding: utf-8
from __future__ import absolute_import
from __future__ import print_function

from warnings import warn
from contextlib import contextmanager
import os
import subprocess
import sys

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase

if sys.version_info >= (3, 0):
    basestring = str


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

    capture = False  # Deprecated
    save_baseline = False

    viewport_width = 1024
    viewport_height = 768

    # TODO: More robust env handling:
    use_perceptualdiff = os.environ.get('NEEDLE_USE_PERCEPTUALDIFF', False)
    perceptualdiff_path = 'perceptualdiff'
    perceptualdiff_output_png = True

    @classmethod
    def setUpClass(cls):
        if os.environ.get('NEEDLE_CAPTURE'):
            cls.capture = True
        if os.environ.get('NEEDLE_SAVE_BASELINE'):
            cls.save_baseline = True
        cls.driver = cls.get_web_driver()
        cls.driver.set_window_position(0, 0)
        cls.set_viewport_size(cls.viewport_width, cls.viewport_height)
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

        for i in (self.baseline_directory, self.output_directory):
            if not os.path.exists(i):
                print('Creating %s' % i, file=sys.stderr)
                os.makedirs(i)

    @classmethod
    def set_viewport_size(cls, viewport_width, viewport_height):
        cls.driver.set_window_size(viewport_width, viewport_height)

        # Measure the difference between the actual document width and the
        # desired viewport width so we can account for scrollbars:
        measured = cls.driver.execute_script("return {width: document.body.clientWidth, height: document.body.clientHeight};")
        delta = viewport_width - measured['width']

        cls.driver.set_window_size(viewport_width + delta, viewport_height)

    def assertScreenshot(self, element_or_selector, file, threshold=0.1):
        """assert-style variant of compareScreenshot context manager

        compareScreenshot() can be considerably more efficient for recording baselines by avoiding the need
        to load pages before checking whether we're actually going to save them. This function allows you
        to continue using normal unittest-style assertions if you don't need the efficiency benefits
        """

        with self.compareScreenshot(element_or_selector, file, threshold=threshold):
            pass

    @contextmanager
    def compareScreenshot(self, element_or_selector, file, threshold=0.1):
        """
        Assert that a screenshot of an element is the same as a screenshot on disk,
        within a given threshold.

        :param element_or_selector:
            Either a CSS selector as a string or a
            :py:class:`~needle.driver.NeedleWebElement` object that represents
            the element to capture.
        :param file:
            If a string, then assumed to be the filename for the screenshot,
            which will be appended with ``.png``. Otherwise assumed to be
            a file object for the baseline image.
        :param threshold:
            The threshold for triggering a test failure.
        """

        yield  # To allow using this method as a context manager

        if not isinstance(element_or_selector, NeedleWebElement):
            element = self.driver.find_element_by_css_selector(element_or_selector)
        else:
            element = element_or_selector

        if isinstance(file, basestring):
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

            if save_baseline:
                element.get_screenshot().save(baseline_file)
                return
            else:
                if not os.path.exists(baseline_file):
                    raise IOError('The baseline screenshot %s does not exist. '
                                  'You might want to re-run this test in baseline-saving mode.'
                                  % baseline_file)

                baseline_image = Image.open(baseline_file)

                fresh_screenshot = element.get_screenshot()
                fresh_screenshot.save(output_file)

                if self.use_perceptualdiff:
                    # TODO: figure out how best to convert threshold distances to pixel counts
                    diff_ppm = output_file.replace(".png", ".diff.ppm")
                    cmd = "%s -output %s %s %s" % (self.perceptualdiff_path, diff_ppm, baseline_file, output_file)
                    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    perceptualdiff_stdout, _ = process.communicate()
                    if process.returncode == 0:
                        # No differences found
                        return
                    else:
                        if os.path.exists(diff_ppm):
                            if self.perceptualdiff_output_png:
                                # Convert the .ppm output to .png
                                diff_png = diff_ppm.replace("diff.ppm", "diff.png")
                                Image.open(diff_ppm).save(diff_png)
                                os.remove(diff_ppm)
                                diff_file_msg = ' (See %s)' % diff_png
                            else:
                                diff_file_msg = ' (See %s)' % diff_ppm
                        else:
                            diff_file_msg = ''
                        raise AssertionError("The new screenshot '%s' did not match "
                                             "the baseline '%s'%s:\n%s"
                                             % (output_file, baseline_file, diff_file_msg, perceptualdiff_stdout))

        else:
            baseline_image = Image.open(file).convert('RGB')
            fresh_screenshot = element.get_screenshot()

        diff = ImageDiff(fresh_screenshot, baseline_image)
        distance = abs(diff.get_distance())
        if distance > threshold:
            raise AssertionError("The given screenshot did not match the "
                                 "screenshot captured (by a distance of %.2f)"
                                 % distance)
