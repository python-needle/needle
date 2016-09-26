import subprocess
import os

from PIL import Image

from needle.engines.base import EngineBase


class Engine(EngineBase):

    perceptualdiff_path = 'perceptualdiff'
    perceptualdiff_output_png = True

    def assertSameFiles(self, output_file, baseline_file, threshold):
        # Calculate threshold value as a pixel number instead of percentage.
        width, height = Image.open(output_file).size
        threshold = int(width * height * threshold)

        diff_ppm = output_file.replace(".png", ".diff.ppm")
        cmd = "%s -threshold %d -output %s %s %s" % (
            self.perceptualdiff_path, threshold, diff_ppm, baseline_file, output_file)
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        perceptualdiff_stdout, _ = process.communicate()

        # Sometimes perceptualdiff returns a false positive with this exact message:
        # 'FAIL: Images are visibly different\n0 pixels are different\n\n'
        # We catch that here.
        if process.returncode == 0 or b'\n0 pixels are different' in perceptualdiff_stdout:
            # No differences found, but make sure to clean up the .ppm in case it was created.
            if os.path.exists(diff_ppm):
                os.remove(diff_ppm)
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
