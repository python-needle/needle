Change log
==========

0.2.0 (Upcoming)
----------------

 - The `--with-needle-capture` and `NeedleTestCase.capture` options were
   deprecated and will be removed in version 0.4.0. Instead, you should now
   respectively use the new, more explicit `--with-save-baseline` and
   `NeedleTestCase.save_baseline` options. Note that those new options will
   systematically cause the baseline image files to be saved on disk,
   overwriting potentially existing baseline files.

0.1.0 (2014-02-20)
------------------

 - Add `set_viewport_size()` method to `NeedleTestCase`
 - Calculate the dimensions of elements more accurately with jQuery
 - Only load jQuery if it hasn't already been loaded

Thanks @jphalip!

0.0.2 (2013-10-24)
------------------

 - Allow needle to be used with custom web driver
 - Replace PIL with pillow

Thanks @treyhunner!

0.0.1 (2013-05-07)
------------------

Initial release.

