from wand.image import Image
from needle.engines.base import EngineBase


class Engine(EngineBase):
    

    def assertSameFiles(self, output_file, baseline_file, threshold=0):

        diff_file = output_file.replace('.png', '.diff.png')

        img_base = Image(filename=os.path.abspath(baseline_file))
        img_out =  Image(filename=os.path.abspath(output_file))

        img_base.normalize()
        img_out.normalize()

        comparison, difference = img_base.compare(img_out, metric='root_mean_square')
            
        if difference <= threshold:
            return
        else:
            comparison.save(diff_file)

        raise AssertionError("The new screenshot '{new}' did not match "
                             "the baseline '{baseline}' (See {diff}):\n"
                             .format(new=output_file,
                                     baseline=baseline_file,
                                     diff=diff_file))