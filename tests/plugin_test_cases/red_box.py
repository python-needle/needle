from needle.cases import NeedleTestCase
from tests import ImageTestCaseMixin

class RedBoxTestCase(ImageTestCaseMixin, NeedleTestCase):
    def test_red_box(self):
        self.driver.load_html("""
            <style type="text/css">
                #test {
                    position: absolute;
                    left: 50px;
                    top: 100px;
                    width: 100px;
                    height: 100px;
                    background-color: red;
                }
            </style>
            <div id="test"></div>
        """)
        self.assertScreenshot(self.driver.find_element_by_id('test'), 'red_box')