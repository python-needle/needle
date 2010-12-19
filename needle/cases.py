from needle.driver import NeedleWebDriver
import unittest2

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
    

