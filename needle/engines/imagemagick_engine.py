import os
import subprocess

from needle.engines.base import EngineBase


class Engine(EngineBase):
    compare_path = "compare"
    compare_command = ("{compare} -metric RMSE -subimage-search -dissimilarity-threshold 1.0 {baseline} "
                       "{new} {diff}")

    def assertSameFiles(self, output_file, baseline_file, threshold=0):
        diff_file = output_file.replace('.png', '.diff.png')

        compare_cmd = self.compare_command.format(
            compare=self.compare_path,
            baseline=baseline_file,
            new=output_file,
            diff=diff_file)
        process = subprocess.Popen(compare_cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        compare_stdout, compare_stderr = process.communicate()

        difference = float(compare_stderr.split()[1][1:-1])
        if difference <= threshold:
            os.remove(diff_file)
            return

        raise AssertionError("The new screenshot '{new}' did not match "
                             "the baseline '{baseline}' (See {diff}):\n"
                             "{stdout}{stderr}"
                             .format(new=output_file,
                                     baseline=baseline_file,
                                     diff=diff_file,
                                     stdout=compare_stdout,
                                     stderr=compare_stderr))