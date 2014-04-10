Change log
==========

0.2.1 (2014-04-10)
------------------

 - Fixed a regression in the PIL engine.

0.2.0 (2014-04-07)
------------------

 - Added support for Python 3.
 - Changed default threshold from 0.1 to 0.
 - Added configurable way of plugging external diff engines like PerceptualDiff.
 - Removed the necessity to run the Selenium server by using a Firefox web
   driver instance by default. This is slightly backwards-incompatible if you
   relied on the now-removed `driver_command_executor`,
   `driver_desired_capabilities` and `driver_browser_profile` attributes.
   To control the logic for selecting the proper web driver, you may simply
   override the `get_web_driver()` method.
 - The `--with-needle-capture` and `NeedleTestCase.capture` options were
   deprecated and will be removed in version 0.4.0. Instead, you should now
   respectively use the new, more explicit `--with-save-baseline` and
   `NeedleTestCase.save_baseline` options. Note that those new options will
   systematically cause the baseline image files to be saved on disk,
   overwriting potentially existing baseline files.
 - Removed the `NeedleWebElement.get_computed_property()` method. Instead, you
   may use Selenium's built-in `value_of_css_property()` method.
 - Upgraded vendored jQuery to version 11.0.

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

