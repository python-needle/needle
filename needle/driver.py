import base64
from PIL import Image
from selenium.remote.webdriver import WebDriver
from selenium.remote.webelement import WebElement
import urllib
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class NeedleWebElement(WebElement):
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


class NeedleWebDriver(WebDriver):
    def load_html(self, html):
        """
        Load a page in the browser with the given HTML.
        """
        self.get('data:text/html,'+urllib.quote(html))

    def get_screenshot_as_image(self):
        """
        Returns a screenshot of the current page as an RGB PIL image.
        """
        fh = StringIO(base64.b64decode(self.get_screenshot_as_base64()))
        return Image.open(fh).convert('RGB')
    
    def create_web_element(self, *args, **kwargs):
        return NeedleWebElement(self, *args, **kwargs)

