# encoding: utf-8
from __future__ import absolute_import

import base64
import os
import urllib

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from PIL import Image

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


class NeedleWebElement(WebElement):
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
        return self._parent.execute_script("""
            var e = arguments[0];
            var dimensions = {
                'width': e.offsetWidth,
                'height': e.offsetHeight,
                'left': 0,
                'top': 0
            };
            do {
                dimensions['left'] += e.offsetLeft;
                dimensions['top'] += e.offsetTop;
            } while (e = e.offsetParent)
            return dimensions;
        """, self)

    def get_screenshot(self):
        """
        Returns a screenshot of this element as a PIL image.
        """
        d = self.get_dimensions()
        return self._parent.get_screenshot_as_image().crop((
            d['left'],
            d['top'],
            d['left'] + d['width'],
            d['top'] + d['height'],
        ))

    def get_computed_property(self, prop):
        """
        Returns the computed value of a CSS property.
        """
        self._parent.load_jquery()
        return self._parent.execute_script("""
            return $(arguments[0]).css(arguments[1]);
        """, self, prop)


class NeedleWebDriver(WebDriver):
    """
    A browser window that Selenium has opened.

    It is a Selenium :py:class:`~selenium.webdriver.remote.webdriver.WebDriver`
    object with some extra methods for testing CSS. See
    `Selenium's documentation <http://seleniumhq.org/docs/03_webdriver.html>`_
    for more information.
    """
    def load_html(self, html):
        """
        Similar to :py:meth:`get`, but instead of passing a URL to load in the
        browser, the HTML for the page is provided.
        """
        self.get('data:text/html,'+urllib.quote(html))

    def get_screenshot_as_image(self):
        """
        Returns a screenshot of the current page as an RGB
        `PIL image <http://www.pythonware.com/library/pil/handbook/image.htm>`_.
        """
        fh = StringIO(base64.b64decode(self.get_screenshot_as_base64()))
        return Image.open(fh).convert('RGB')

    def load_jquery(self):
        """
        Loads jQuery 1.5 onto the current page so calls to
        :py:meth:`execute_script` have access to it.
        """
        # Bug in 1.5.1 means we can't load on data URL pages.
        # Should be fixed in 1.5.2
        # https://github.com/jquery/jquery/pull/269
        self.execute_script(open(
            os.path.join(self._get_js_path(), 'jquery-1.5.min.js')
        ).read() + '\nreturn "";')

    def _get_js_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js')

    def create_web_element(self, *args, **kwargs):
        return NeedleWebElement(self, *args, **kwargs)

