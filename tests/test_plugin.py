import sys
import os

from nose.plugins import PluginTester

from needle.plugin import NeedleCapturePlugin


if sys.version_info > (2, 7):
    from unittest import TestCase
else:
    from unittest2 import TestCase


class BasePluginTest(PluginTester, TestCase):
    activate = '--with-needle-capture'
    plugins = [NeedleCapturePlugin()]
    suitepath = 'tests/plugin_test_cases/red_box.py'

    def tearDown(self):
        os.remove('screenshots/baseline/red_box.png')


class TestPlugin(BasePluginTest):
    def test_screenshot_is_captured(self):
        self.assertTrue(os.path.exists('screenshots/baseline/red_box.png'))
        self.assertTrue(self.nose.success)


class TestPluginWithExistingCapture(BasePluginTest):
    def setUp(self):
        open('screenshots/baseline/red_box.png', 'a').close()
        super(TestPluginWithExistingCapture, self).setUp()

    def test_existing_capture_is_skipped(self):
        self.assertTrue(self.nose.success)