import sys
from itertools import chain
import subprocess
import os
import math

from PIL import Image

if sys.version_info >= (3, 0):
    izip = zip
else:
    from itertools import izip


class DiffEngine(object):
    """
    Base class for diff engines.
    """

    def assertSameFiles(self, output_file, baseline_file, threshold):
        raise NotImplemented


class PerceptualDiffEngine(DiffEngine):

    perceptualdiff_path = 'perceptualdiff'
    perceptualdiff_output_png = True

    def assertSameFiles(self, output_file, baseline_file, threshold):
        # Calculate threshold value as a pixel number instead of percentage.
        width, height = Image.open(open(output_file)).size
        threshold = int(width * height * threshold)

        diff_ppm = output_file.replace(".png", ".diff.ppm")
        cmd = "%s -threshold %d -output %s %s %s" % (
            self.perceptualdiff_path, threshold, diff_ppm, baseline_file, output_file)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        perceptualdiff_stdout, _ = process.communicate()

        if process.returncode == 0:
            # No differences found
            return
        else:
            if os.path.exists(diff_ppm):
                if self.perceptualdiff_output_png:
                    # Convert the .ppm output to .png
                    diff_png = diff_ppm.replace("diff.ppm", "diff.png")
                    Image.open(diff_ppm).save(diff_png)
                    os.remove(diff_ppm)
                    diff_file_msg = ' (See %s)' % diff_png
                else:
                    diff_file_msg = ' (See %s)' % diff_ppm
            else:
                diff_file_msg = ''
            raise AssertionError("The new screenshot '%s' did not match "
                                 "the baseline '%s'%s:\n%s"
                                 % (output_file, baseline_file, diff_file_msg, perceptualdiff_stdout))


class PILEngine(DiffEngine):

    def assertSameFiles(self, output_file, baseline_file, threshold):
        diff = ImageDiff(output_file, baseline_file)
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