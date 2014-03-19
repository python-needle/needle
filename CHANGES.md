Change log
==========

0.2.0 (upcoming)
----------------

- Removed the necessity to run the Selenium server by using a Firefox web
  driver instance by default. This is slightly backwards-incompatible if you
  relied on the now-removed `driver_command_executor`,
  `driver_desired_capabilities` and `driver_browser_profile` attributes.
  To control the logic for selecting the proper web driver, you may simply
  override the `get_web_driver()` method.

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

