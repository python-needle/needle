from __future__ import absolute_import
import subprocess
import unittest
from os import devnull

from tests.test_perceptualdiff_engine import PerceptualdiffEngineTests


class ImageMagickEngineTests(PerceptualdiffEngineTests):
    engine_class = 'needle.engines.imagemagick_engine.Engine'

    @classmethod
    def setUpClass(cls):
        try:
            subprocess.call(['compare', '--version'], stdout=open(devnull), stderr=open(devnull))
        except OSError:
            raise unittest.SkipTest('ImageMagick is not installed')
        super(ImageMagickEngineTests, cls).setUpClass()


# Delete the imported module so it doesn't get executed here.
del PerceptualdiffEngineTests