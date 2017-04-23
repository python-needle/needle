Needle
======

[![Build Status](https://travis-ci.org/python-needle/needle.png?branch=master)](https://travis-ci.org/python-needle/needle)

Needle is a tool for testing visuals with [Selenium](http://seleniumhq.org/) 
and [nose](https://nose.readthedocs.io/).

It checks that visuals (CSS/fonts/images/SVG/etc.) render correctly by taking
screenshots of portions of a website and comparing them against known good
screenshots. It also provides tools for testing calculated CSS values and the
position of HTML elements.

Example
-------

This is what a Needle test case looks like:

```python
from needle.cases import NeedleTestCase

class BBCNewsTest(NeedleTestCase):
    def test_masthead(self):
        self.driver.get('http://www.bbc.co.uk/news/')
        self.assertScreenshot('#blq-mast', 'bbc-masthead')
```

This example checks for regressions in the appearance of the BBC's masthead.

Documentation
-------------

Full documentation available on [Read the Docs](https://needle.readthedocs.io/).

If you'd like to build the documentation yourself, first install ``sphinx``:

    pip install sphinx
    
Then run:

    cd docs
    make html
    
The documentation will then be available browsable from
``docs/_build/index.html``.

Running Needle's test suite
---------------------------

First install tox (usually via ``pip install tox``).  Then:

    $ tox
