Needle
======

Needle is a tool for testing your CSS with [Selenium](http://seleniumhq.org/) 
and [nose](http://somethingaboutorange.com/mrl/projects/nose/).

It checks that CSS renders correctly by taking screenshots of portions of
a website and comparing them against known good screenshots. It also provides
tools for testing calculated CSS values and the position of HTML elements.

Example
-------

This is an example of a test case which will check for regressions in Google's
logo::

    from needle.cases import NeedleTestCase

    class GoogleTest(NeedleTestCase):
        def test_logo(self):
            self.driver.get('http://www.google.com')
            self.assertScreenshot('//*[@id="lga"]', 'google-logo')


Documentation
-------------

Full documentation is on [Read the Docs](http://readthedocs.org/docs/needle/).


Running Needle's test suite
---------------------------

    $ nosetests


