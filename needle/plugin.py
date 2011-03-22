from nose.plugins import Plugin

class NeedleCapturePlugin(Plugin):
    """
    A nose plugin which causes all calls to 
    ``NeedleTestCase.assertElementEqualsImage`` to capture a screenshot to disk.
    """
    name = 'needle-capture'

    def wantClass(self, cls):
        # Only gather classes which are a needle test case
        return hasattr(cls, 'assertElementEqualsImage')

    def wantFunction(self, f):
        return False

    def beforeTest(self, test):
        if hasattr(test, 'test'):
            test.test.capture = True



