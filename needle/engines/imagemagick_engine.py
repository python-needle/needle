import os
import subprocess

from needle.engines.base import EngineBase


class Engine(EngineBase):
    cmp_path = "cmp"
    cmp_command = "{cmp} {baseline} {new}"
    compare_path = "compare"
    compare_command = ("{compare} -metric RMSE -subimage-search {baseline} "
                       "{new} {diff}")

    def assertSameFiles(self, output_file, baseline_file, threshold=0):
        diff_file = output_file.replace('.png', '.diff.png')

        cmp_cmd = self.cmp_command.format(cmp=self.cmp_path,
                                          baseline=baseline_file,
                                          new=output_file)
        if subprocess.call(cmp_cmd, shell=True) == 0:
            os.remove(output_file)
            # remove a possible earlier diff file
            os.remove(diff_file)
            return

        compare_cmd = self.compare_command.format(
            compare=self.compare_path,
            baseline=baseline_file,
            new=output_file,
            diff=diff_file)
        process = subprocess.Popen(compare_cmd, shell=True,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        compare_stdout, compare_stderr = process.communicate()

        if process.returncode != 0:
            raise RuntimeError("{compare} returned a non-zero exit status.\n"
                               "{cmd}\n"
                               "{stdout}{stderr}"
                               .format(compare=self.compare_path,
                                       cmd=compare_cmd,
                                       stdout=compare_stdout,
                                       stderr=compare_stderr))

        difference = float(compare_stderr.split()[1][1:-1])

        if difference <= threshold:
            os.remove(diff_file)
            os.remove(output_file)
            return

        raise AssertionError("The new screenshot '{new}' did not match "
                             "the baseline '{baseline}' (See {diff}):\n"
                             "{stdout}{stderr}"
                             .format(new=output_file,
                                     baseline=baseline_file,
                                     diff=diff_file,
                                     stdout=compare_stdout,
                                     stderr=compare_stderr))
