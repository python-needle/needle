from __future__ import absolute_import
import subprocess
import unittest
from os import path, devnull

from tests.test_pil_engine import PILEngineTests


class PerceptualdiffEngineTests(PILEngineTests):
    engine_class = 'needle.engines.perceptualdiff_engine.Engine'

    @classmethod
    def setUpClass(cls):
        try:
            subprocess.call(['perceptualdiff', '--version'], stdout=open(devnull), stderr=open(devnull))
        except OSError:
            raise unittest.SkipTest('perceptualdiff is not installed')
        super(PerceptualdiffEngineTests, cls).setUpClass()

    def test_assertScreenshot_failure(self):
        super(PerceptualdiffEngineTests, self).test_assertScreenshot_failure()
        # Check that the diff file was created
        diff_file = path.join(path.dirname(__file__), 'screenshots', 'black-box.diff.png')
        self.assertTrue(path.isfile(diff_file))


# Delete the imported module so it doesn't get executed here.
del PILEngineTests