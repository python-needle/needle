needle
======

Needle is a tool for testing your CSS with [Selenium](http://seleniumhq.org/) 
and [nose](http://somethingaboutorange.com/mrl/projects/nose/).

It checks that CSS renders correctly by taking screenshots of portions of
a website and comparing them against known good screenshots. It also provides
tools for testing calculated CSS values and the position of HTML elements.


Install
-------

If you haven't got [pip](http://www.pip-installer.org/) installed:

    $ sudo easy_install pip

As root, or in a [virtualenv](http://www.virtualenv.org/):

    $ pip install -r requirements.txt
    $ python setup.py install


Download [selenium-server-standalone-2.0b3.jar](http://selenium.googlecode.com/files/selenium-server-standalone-2.0b3.jar). By default, Selenium requires [Firefox 4](http://getfirefox.com).


Getting started
---------------

Run the Selenium server:

    $ java -jar selenium-server-standalone-2.0b3.jar

Create ``test_google.py``:

    from needle.cases import NeedleTestCase

    class GoogleTest(NeedleTestCase):
        def test_logo(self):
            self.driver.get('http://www.google.com')
            self.assertScreenshot('//*[@id="lga"]', 'google-logo')

This is a test case which tells the Selenium server to open Google, then check
the logo looks correct. ``assertScreenshot`` take two arguments: an XPath to
the element we are capturing and a filename for the image.

To create an initial screenshot of the logo, we need to run Needle in capture mode:

    $ nosetests test_google.py --with-needle-capture

This will create ``google-logo.png``. Open it up and check it looks okay.

Now if we run our tests, it will capture the same screenshot and check it against
this screenshot on disk: 

    $ nosetests test_google.py

If they are significantly different, the test will fail.



