from selenium.remote.webdriver import WebDriver
from selenium.remote.webelement import WebElement
import urllib

class NeedleWebElement(WebElement):
    def get_dimensions(self):
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

class NeedleWebDriver(WebDriver):
    def get_html(self, html):
        self.get('data:text/html,'+urllib.quote(html))
    
    def create_web_element(self, *args, **kwargs):
        return NeedleWebElement(self, *args, **kwargs)

