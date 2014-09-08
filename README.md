Needle
======

[![Build Status](https://travis-ci.org/bfirsh/needle.png?branch=master)](https://travis-ci.org/bfirsh/needle)

Needle is a tool for testing your CSS with [Selenium](http://seleniumhq.org/) 
and [nose](http://somethingaboutorange.com/mrl/projects/nose/).

It checks that CSS renders correctly by taking screenshots of portions of
a website and comparing them against known good screenshots. It also provides
tools for testing calculated CSS values and the position of HTML elements.

Example
-------

This is what a Needle test case looks like:

    from needle.cases import NeedleTestCase

    class BBCNewsTest(NeedleTestCase):
        def test_masthead(self):
            self.driver.get('http://www.bbc.co.uk/news/')
            self.assertScreenshot('#blq-mast', 'bbc-masthead')

This example checks for regressions in the appearance of the BBC's masthead.

Documentation
-------------

Full documentation is on [Read the Docs](http://needle.readthedocs.org/).


Running Needle's test suite
---------------------------

    $ nosetests


Running an individual test file
-------------------------------

To run a needle test against an already captured screenshot, use this:

    $ nosetests mytest.py


To run a test in "capture-mode" without any risk of overwriting any images you already have:

    $ nosetests mytest.py --with-needle-capture

To run a test in "capture-mode" overwriting any images you already have:

    $ nosetests mytest.py --with-save-baseline
