from needle.plugin import NeedleCapturePlugin, SaveBaselinePlugin
from nose.plugins import PluginTester
import os
import unittest2


baseline_filename = 'screenshots/baseline/red_box.png'
dummy_baseline_content = 'abcd'


class NeedleCaptureTest(PluginTester, unittest2.TestCase):
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


class NeedleCaptureOverwriteTest(PluginTester, unittest2.TestCase):
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
        baseline = open(baseline_filename, 'w')
        baseline.write(dummy_baseline_content)
        baseline.close()

        super(NeedleCaptureOverwriteTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_existing_baseline_not_overwritten(self):
        baseline = open(baseline_filename, 'r')
        self.assertEqual(baseline.read(), dummy_baseline_content)
        self.assertTrue(self.nose.success)



class SaveBaselineTest(PluginTester, unittest2.TestCase):
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


class SaveBaselineOverwriteTest(PluginTester, unittest2.TestCase):
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
        baseline = open(baseline_filename, 'w')
        baseline.write(dummy_baseline_content)
        baseline.close()

        super(SaveBaselineOverwriteTest, self).setUp()

    def tearDown(self):
        os.remove(baseline_filename)

    def test_existing_baseline_is_overwritten(self):
        baseline = open(baseline_filename, 'r')
        self.assertNotEqual(baseline.read(), dummy_baseline_content)
        self.assertTrue(self.nose.success)