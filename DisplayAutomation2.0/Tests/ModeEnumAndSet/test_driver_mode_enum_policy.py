#######################################################################################################################
# @file         test_driver_mode_enum_policy.py
# @brief        This file is designed to contain set of driver policy mode_enum tests
# @author       Supriya Krishnamurthi
#######################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.ModeEnumAndSet.display_mode_enumeration_base import *


##
# @brief        This class contains set of driver policy mode_enum tests
class DriverModeEnumPolicyTests(ModeEnumAndSetBase):

    ##
    # @brief        This Unit-test runTest function first validates if the modes in xml files are enumerated by the
    #               driver and then validates base block DTD preference by driver in presence higher pixel clock DTD for
    #               same active pixels in extension block. When 2 modes with identical active pixels and different pixel
    #               clock are present in edid, i.e the mode with lower pixel clock is present in base block DTD and the
    #               higher one in CEA extension block DTD, the first DTD in base block (preferred timing mode) should
    #               take the precedence than the DTD in CEA extension block and first DTD in base block should be
    #               reported to OS as preferred timing. This scenario is created to address the below QE issue
    #               QE: https://hsdes.intel.com/appstore/article/#/16014373744
    # @return       None
    # @cond
    @common.configure_test(selective=['BASE_BLOCK_PREFERENCE'])
    # @endcond
    def t_1_prefer_base_block(self):

        # Set Display config is done in setUp phase. Fetch the current mode after setting the display config
        disp_adater_info = self.display_config.get_display_and_adapter_info_ex(self.display)
        current_mode = self.display_config.get_current_mode(disp_adater_info)

        # xml consists of 2 identical modes with different pixel clock. 1st one is with lower pixel clock and later is
        # with higher pixel clock. Verify if current mode is same as 1st mode in xml with lower pixel clock as that is
        # expected to be preferred by the driver
        lower_pixel_clock_mode = list(self.apply_mode_list.values())[0]
        if current_mode == lower_pixel_clock_mode.DisplayMode and \
                current_mode.pixelClock_Hz == lower_pixel_clock_mode.PixelClk:
            logging.info("Pass: Driver preferred lower pixel clock mode present in the base block of the edid")
        else:
            gdhm.report_bug(
                title="[Interfaces][ModeEnum] Fail: Driver failed to prefer the base block DTD mode with lower pixel "
                      "clock in the edid",
                problem_classification=gdhm.ProblemClassification.OTHER,
                component=gdhm.Component.Test.DISPLAY_INTERFACES,
                priority=gdhm.Priority.P1,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Fail: Driver failed to prefer the base block DTD mode with lower pixel clock in the edid")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(DriverModeEnumPolicyTests))
    test_environment.TestEnvironment.cleanup(test_result)
