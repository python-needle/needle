from selenium.remote.webdriver import WebDriver
from selenium.remote.webelement import WebElement
import unittest2
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

class NeedleTestCase(unittest2.TestCase):
    driver_url = 'http://127.0.0.1:4444/wd/hub'
    driver_browser = 'firefox'
    driver_platform = None
    driver_version = ''
    driver_javascript_enabled = True

    def __call__(self, *args, **kwargs):
        self.driver = self.get_web_driver()
        super(NeedleTestCase, self).__call__(*args, **kwargs)
        self.driver.close()
    
    def get_web_driver(self):
        return NeedleWebDriver(
            self.driver_url,
            self.driver_browser,
            self.driver_platform,
            self.driver_version,
            self.driver_javascript_enabled,
        )
    

