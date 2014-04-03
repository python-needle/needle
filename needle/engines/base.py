class EngineBase(object):
    """
    Base class for diff engines.
    """

    def assertSameFiles(self, output_file, baseline_file, threshold):
        raise NotImplementedError