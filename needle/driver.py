# encoding: utf-8
from __future__ import absolute_import

import base64
import os
import sys

if sys.version_info >= (3, 0):
    from urllib.parse import quote
    from io import BytesIO as IOClass
else:
    from urllib import quote
    try:
        from cStringIO import StringIO as IOClass
    except ImportError:
        from StringIO import StringIO as IOClass


from PIL import Image

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.firefox.webdriver import WebDriver as Firefox
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.ie.webdriver import WebDriver as Ie
from selenium.webdriver.opera.webdriver import WebDriver as Opera
from selenium.webdriver.safari.webdriver import WebDriver as Safari
from selenium.webdriver.phantomjs.webdriver import WebDriver as PhantomJS
from selenium.webdriver.remote.webdriver import WebDriver as Remote

try:
    # Added in selenium 3.0.0.b3
    from selenium.webdriver.firefox.webelement import FirefoxWebElement
except ImportError:
    from selenium.webdriver.remote.webelement import WebElement as FirefoxWebElement


class NeedleWebElementMixin(object):
    """
    An element on a page that Selenium has opened.

    It is a Selenium :py:class:`~selenium.webdriver.remote.webelement.WebElement`
    object with some extra methods for testing CSS.
    """
    def get_dimensions(self):
        """
        Returns a dictionary containing, in pixels, the element's ``width`` and
        ``height``, and it's ``left`` and ``top`` position relative to the document.
        """
        location = self.location
        size = self.size
        return {
            "top": location['y'],
            "left": location['x'],
            "width": size['width'],
            "height": size['height']
        }

    def get_screenshot(self):
        """
        Returns a screenshot of this element as a PIL image.
        """
        d = self.get_dimensions()
        devicePixelRatio = int(self._parent.execute_script("return window.devicePixelRatio"))
        
        # Cast values to int in order for _ImageCrop not to break
        d['left'] = int(d['left'])
        d['top'] = int(d['top'])
        d['width'] = int(d['width']) * devicePixelRatio
        d['height'] = int(d['height']) * devicePixelRatio

        try:
            # For selenium >= 2.46.1, W3C WebDriver spec drivers (like geckodriver)
            fh = IOClass(self.screenshot_as_png)
            image = Image.open(fh).convert('RGB')
            # Make sure it isn't actually a full-page screenshot (PhantomJS)
            if image.size == (d['width'], d['height']):
                return image
        except (AttributeError, WebDriverException):
            # Fall back to cropping a full page screenshot
            image = self._parent.get_screenshot_as_image()

        return image.crop((
            d['left'],
            d['top'],
            d['left'] + d['width'],
            d['top'] + d['height'],
        ))


class NeedleWebDriverMixin(object):
    """
    Selenium WebDriver mixin with some extra methods for testing CSS.
    """
    def load_html(self, html):
        """
        Similar to :py:meth:`get`, but instead of passing a URL to load in the
        browser, the HTML for the page is provided.
        """
        self.get('data:text/html,' + quote(html))

    def get_screenshot_as_image(self):
        """
        Returns a screenshot of the current page as an RGB
        `PIL image <http://www.pythonware.com/library/pil/handbook/image.htm>`_.
        """
        fh = IOClass(base64.b64decode(self.get_screenshot_as_base64().encode('ascii')))
        return Image.open(fh).convert('RGB')

    def load_jquery(self):
        """
        Loads jQuery onto the current page so calls to
        :py:meth:`execute_script` have access to it.
        """
        if (self.execute_script('return typeof(jQuery)') == 'undefined'):
            self.execute_script(open(
                os.path.join(self._get_js_path(), 'jquery-1.11.0.min.js')
            ).read() + '\nreturn "";')

    def _get_js_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js')

    def create_web_element(self, element_id, *args, **kwargs):
        if isinstance(self, NeedleFirefox):
            return NeedleFirefoxWebElement(self, element_id, w3c=self.w3c, *args, **kwargs)
        else:
            return NeedleWebElement(self, element_id, w3c=self.w3c, *args, **kwargs)


class NeedleRemote(NeedleWebDriverMixin, Remote):
    """
    The same as Selenium's remote WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedlePhantomJS(NeedleWebDriverMixin, PhantomJS):
    """
    The same as Selenium's PhantomJS WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedleFirefox(NeedleWebDriverMixin, Firefox):
    """
    The same as Selenium's Firefox WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedleChrome(NeedleWebDriverMixin, Chrome):
    """
    The same as Selenium's Chrome WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedleIe(NeedleWebDriverMixin, Ie):
    """
    The same as Selenium's Internet Explorer WebDriver, but with
    NeedleWebDriverMixin's functionality.
    """

class NeedleOpera(NeedleWebDriverMixin, Opera):
    """
    The same as Selenium's Opera WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedleSafari(NeedleWebDriverMixin, Safari):
    """
    The same as Selenium's Safari WebDriver, but with NeedleWebDriverMixin's
    functionality.
    """

class NeedleWebElement(NeedleWebElementMixin, WebElement):
    """
    The same as Selenium's WebElement, but with NeedleWebElementMixin's
    functionality.
    """

class NeedleFirefoxWebElement(NeedleWebElementMixin, FirefoxWebElement):
    """
    The same as Selenium's FirefoxWebElement, but with NeedleWebElementMixin's
    functionality.
    """
