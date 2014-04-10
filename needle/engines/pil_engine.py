import sys
from itertools import chain
import math

if sys.version_info >= (3, 0):
    izip = zip
else:
    from itertools import izip

from PIL import Image

from needle.engines.base import EngineBase


class Engine(EngineBase):

    def assertSameFiles(self, output_file, baseline_file, threshold):
        output_image = Image.open(output_file).convert('RGB')
        baseline_image = Image.open(baseline_file).convert('RGB')
        diff = ImageDiff(output_image, baseline_image)
        distance = abs(diff.get_distance())
        if distance > threshold:
            raise AssertionError("The new screenshot '%s' did not match "
                                 "the baseline '%s' (by a distance of %.2f)"
                                 % (output_file, baseline_file, distance))


class ImageDiff(object):
    """
    Utility class for performing image comparisons using PIL.
    """

    def __init__(self, image_a, image_b):
        assert image_a.size == image_b.size
        assert image_a.getbands() == image_b.getbands()

        self.image_a = image_a
        self.image_b = image_b

    def get_nrmsd(self):
        """
        Returns the normalised root mean squared deviation of the two images.
        """
        a_values = chain(*self.image_a.getdata())
        b_values = chain(*self.image_b.getdata())
        rmsd = 0
        for a, b in izip(a_values, b_values):
            rmsd += (a - b) ** 2
        rmsd = math.sqrt(float(rmsd) / (
            self.image_a.size[0] * self.image_a.size[1] * len(self.image_a.getbands())
        ))
        return rmsd / 255

    def get_distance(self):
        """
        Returns the distance between the two images in pixels.
        """
        a_values = chain(*self.image_a.getdata())
        b_values = chain(*self.image_b.getdata())
        band_len = len(self.image_a.getbands())
        distance = 0
        for a, b in izip(a_values, b_values):
            distance += abs(float(a) / band_len - float(b) / band_len) / 255
        return distance