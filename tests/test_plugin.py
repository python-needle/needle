import sys
import os

from needle.plugin import NeedleCapturePlugin, SaveBaselinePlugin, CleanUpOnSuccessPlugin
from nose.plugins import PluginTester

if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase


baseline_filename = 'screenshots/baseline/red_box.png'
screenshot_filename = 'screenshots/red_box.png'
dummy_baseline_content = b'abcd'


class NeedleCaptureTest(PluginTester, TestCase):
    """
    Check that the baseline file gets saved when using the
    --with-needle-capture option.
    """
    activate = '--with-needle-capture'
    plugins = [NeedleCapturePlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def setUp(self):
        self.assertFalse(os.path.exists(baseline_filename))
        super(NeedleCaptureTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_baseline_is_saved(self):
        self.assertTrue(os.path.exists(baseline_filename))
        self.assertTrue(self.nose.success)


class NeedleCaptureOverwriteTest(PluginTester, TestCase):
    """
    Check that an existing baseline file does NOT get overwritten, when using
    the --with-needle-capture option.
    """

    activate = '--with-needle-capture'
    plugins = [NeedleCapturePlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def setUp(self):
        self.assertFalse(os.path.exists(baseline_filename))

        # Create dummy baseline file
        baseline = open(baseline_filename, 'wb')
        baseline.write(dummy_baseline_content)
        baseline.close()

        super(NeedleCaptureOverwriteTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_existing_baseline_not_overwritten(self):
        baseline = open(baseline_filename, 'rb')
        self.assertEqual(baseline.read(), dummy_baseline_content)
        self.assertTrue(self.nose.success)



class SaveBaselineTest(PluginTester, TestCase):
    """
    Check that the baseline file gets saved when using the
    --with-save-baseline option.
    """
    activate = '--with-save-baseline'
    plugins = [SaveBaselinePlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def setUp(self):
        self.assertFalse(os.path.exists(baseline_filename))
        super(SaveBaselineTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_baseline_is_saved(self):
        self.assertTrue(os.path.exists(baseline_filename))
        self.assertTrue(self.nose.success)


class SaveBaselineOverwriteTest(PluginTester, TestCase):
    """
    Check that an existing baseline file DOES get overwritten, when using
    the --with-save-baseline option.
    """

    activate = '--with-save-baseline'
    plugins = [SaveBaselinePlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def setUp(self):
        self.assertFalse(os.path.exists(baseline_filename))

        # Create dummy baseline file
        baseline = open(baseline_filename, 'wb')
        baseline.write(dummy_baseline_content)
        baseline.close()

        super(SaveBaselineOverwriteTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_existing_baseline_is_overwritten(self):
        baseline = open(baseline_filename, 'rb')
        self.assertNotEqual(baseline.read(), dummy_baseline_content)
        self.assertTrue(self.nose.success)


class NeedleCleanupOnSuccessTest(PluginTester, TestCase):
    """
    Check that the screenshot gets removed when using the
    needle-cleanup-on-success option.
    """
    activate = '--with-needle-cleanup-on-success'
    plugins = [CleanUpOnSuccessPlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def setUp(self):
        # Create the baseline
        baseline = open(baseline_filename, 'wb')
        baseline.write(open('tests/test_red_box.png', 'rb').read())
        baseline.close()

        # Make sure the screenshot doesn't exist yet
        self.assertFalse(os.path.exists(screenshot_filename))
        super(NeedleCleanupOnSuccessTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_screenshot_is_cleanedup(self):
        # Make sure the screenshot has been cleaned up
        self.assertFalse(os.path.exists(screenshot_filename))
        self.assertTrue(self.nose.success)
