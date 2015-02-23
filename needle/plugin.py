from nose.plugins import Plugin


class NeedleCapturePlugin(Plugin):
    """
    A nose plugin which causes all calls to
    ``NeedleTestCase.assertScreenshot`` to save a baseline screenshot to disk,
    unless the baseline file already exists.
    """
    name = 'needle-capture'

    def wantClass(self, cls):
        # Only gather classes which are a needle test case
        return hasattr(cls, 'assertScreenshot')

    def wantFunction(self, f):
        return False

    def beforeTest(self, test):
        if hasattr(test, 'test'):
            test.test.capture = True


class SaveBaselinePlugin(Plugin):
    """
    A nose plugin which causes all calls to ``NeedleTestCase.assertScreenshot``
    to save the baseline screenshot to disk.
    """
    name = 'save-baseline'

    def add_options(self, parser, env=None):
        super(SaveBaselinePlugin, self).add_options(parser, env)

    def wantClass(self, cls):
        # Only gather classes which are a needle test case
        return hasattr(cls, 'assertScreenshot')

    def wantFunction(self, f):
        return False

    def beforeTest(self, test):
        if hasattr(test, 'test'):
            test.test.save_baseline = True


class CleanUpOnSuccessPlugin(Plugin):
    """
    A nose plugin that causes all successful ``NeedleTestCase.assertScreenshot``
    calls to delete the non-baseline file from disk.
    """
    name = 'needle-cleanup-on-success'

    def add_options(self, parser, env=None):
        super(CleanUpOnSuccessPlugin, self).add_options(parser, env)

    def wantClass(self, cls):
        # Only gather classes which are a needle test case
        return hasattr(cls, 'assertScreenshot')

    def wantFunction(self, f):
        return False

    def beforeTest(self, test):
        if hasattr(test, 'test'):
            test.test.cleanup_on_success = True
