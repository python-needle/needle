from itertools import izip, chain
import math

class ImageDiff(object):
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
        rmsd = math.sqrt(float(rmsd) / (self.image_a.size[0] * self.image_a.size[1] * len(self.image_a.getbands())))
        return rmsd / 255
    

