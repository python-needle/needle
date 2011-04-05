from needle.cases import NeedleTestCase

class TestWebDriver(NeedleTestCase):
    def test_load_html(self):
        self.driver.load_html('<div id="test">foo</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.text, 'foo')

    def test_load_html_works_with_large_pages(self):
        div = '<div>' + 'a' * 1000 + '</div>'
        html = ''.join(div for _ in range(500)) + '<div id="test">hello</div>'
        self.driver.load_html(html)
        self.assertEqual(
            self.driver.execute_script(
                'return document.getElementsByTagName("div").length'
            ), 
            501
        )
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.text, 'hello')

    def test_load_jquery(self):
        self.driver.load_html('<div></div>')
        self.driver.load_jquery()
        self.assertTrue(self.driver.execute_script("""
            return jQuery !== undefined;
        """))


class TestWebElement(NeedleTestCase):
    def test_get_dimensions(self):
        self.driver.load_html("""
            <style type="text/css">
                #test {
                    position: absolute;
                    left: 50px;
                    top: 100px;
                    width: 150px;
                    height: 200px;
                }
            </style>
            <div id="test">Test</div>
        """)
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_dimensions(), {
            'left': 50,
            'top': 100,
            'width': 150,
            'height': 200,
        })

    def test_get_screenshot(self):
        self.driver.load_html("""
            <style type="text/css">
                #test {
                    position: absolute;
                    left: 50px;
                    top: 100px;
                    width: 150px;
                    height: 200px;
                    background-color: #FF0000;
                }
            </style>
            <div id="test"></div>
        """)
        e = self.driver.find_element_by_id('test')
        im = e.get_screenshot()
        self.assertEqual(im.size, (150, 200))
        for pixel in im.getdata():
            self.assertEqual(pixel, (255, 0, 0))

    def test_get_computed_property(self):
        self.driver.load_html("""
            <style type="text/css">
                #outer {
                    font-size: 10px;
                }
                #inner {
                    font-size: 2em;
                    float: left;
                }
            </style>
            <div id="outer">
                <div id="inner">Hello!</div>
            </div>
        """)
        e = self.driver.find_element_by_id('inner')
        self.assertEqual(e.get_computed_property('font-size'), '20px')
        self.assertEqual(e.get_computed_property('float'), 'left')


