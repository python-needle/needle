from needle.cases import NeedleTestCase

class TestWebDriver(NeedleTestCase):
    def test_get_html(self):
        self.driver.get_html('<div id="test">foo</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_text(), 'foo')


class TestWebElement(NeedleTestCase):
    def test_get_dimensions(self):
        self.driver.get_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 150px; height: 200px">Test</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_dimensions(), {
            'left': 50,
            'top': 100,
            'width': 150,
            'height': 200,
        })

    def test_get_screenshot(self):
        self.driver.get_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 150px; height: 200px; background-color: #FF0000"></div>')
        e = self.driver.find_element_by_id('test')
        im = e.get_screenshot()
        self.assertEqual(im.size, (150, 200))
        for pixel in im.getdata():
            self.assertEqual(pixel, (255, 0, 0, 255))




