from needle.cases import NeedleTestCase

class TestAssertions(NeedleTestCase):
    def test_get_html(self):
        self.driver.get_html('<div id="test">foo</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_text(), 'foo')

    def test_dimensions(self):
        self.driver.get_html('<div id="test" style="position: absolute; left: 50px; top: 100px; width: 150px; height: 200px">Test</div>')
        e = self.driver.find_element_by_id('test')
        self.assertEqual(e.get_dimensions(), {
            'left': 50,
            'top': 100,
            'width': 150,
            'height': 200,
        })


