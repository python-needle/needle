from needle.cases import NeedleTestCase

class TestWebDriver(NeedleTestCase):
    def test_load_html(self):
        self.driver.load_html('<div id="test">foo</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_text(), 'foo')

    def test_load_html_works_with_large_pages(self):
        div = '<div>' + 'a' * 1000 + '</div>'
        html = ''.join(div for _ in range(1000)) + '<div id="test">hello</div>'
        self.driver.load_html(html)
        self.assertEqual(
            self.driver.execute_script(
                'return document.getElementsByTagName("div").length'
            ), 
            1001
        )
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_text(), 'hello')


class TestWebElement(NeedleTestCase):
    def test_get_dimensions(self):
        self.driver.load_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 150px; height: 200px">Test</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_dimensions(), {
            'left': 50,
            'top': 100,
            'width': 150,
            'height': 200,
        })

    def test_get_screenshot(self):
        self.driver.load_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 150px; height: 200px; background-color: #FF0000"></div>')
        e = self.driver.find_element_by_id('test')
        im = e.get_screenshot()
        self.assertEqual(im.size, (150, 200))
        for pixel in im.getdata():
            self.assertEqual(pixel, (255, 0, 0))




