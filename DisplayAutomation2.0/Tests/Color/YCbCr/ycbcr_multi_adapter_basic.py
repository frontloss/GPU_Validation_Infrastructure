##############################################################################################
# \file
# \addtogroup Test_Color
# \section ycbcr_multi_adapter_basic
# \remarks
# \ref ycbcr_multi_adapter_basic.py \n
# This script performs basic color functionality such as enable/disable YCbCr on each display
# across multiple adapter.It also checks for the output color space is YUV when YCbCr is enabled and
# RGB when YCbCr is disabled
#
# CommandLine: python ycbcr_multi_adapter_basic.py -gfx_0 -hdmi_b HDMI_Dell_U2709_YCBCR.EDID -gfx_1 -hdmi_c
#              HDMI_Dell_U2709_YCBCR.EDID
#
# \author Vimalesh D
###############################################################################################

import logging
import unittest
import sys
from Libs.Core.test_env import test_environment
from Libs.Core.logger import gdhm
from Tests.Color.color_multi_adapter_base import ColorMultiAdapterBase
from Tests.Color import color_verification
from Libs.Core import display_config, driver_escape
from Libs.Core import enum
from Libs.Core.display_config import display_config_enums


class YCbCrMultiAdapterBasic(ColorMultiAdapterBase):
    display = 0

    def verify_registers(self):
        ##
        # Get the output colorspace
        logging.info(self.getStepInfo() + "Verifying output color space for display %s" % self.display)
        colorspace_status = color_verification.get_pipe_output_colorspace(self.display, 'PIPE_MISC', 'YUV')
        if colorspace_status != "YUV":
            gdhm.report_bug(
                title="[Color][YCbCrMultiAdapter]Verification of pipe output color "
                      "space failed with programmed csc{0}".format(colorspace_status),
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Pipe output color space mismatch for display: %s" % self.display)

        ##
        # Get the cursor status verification
        color_verification.get_cursor_status(self.display, 'CUR_CTL')

        ##
        # Get the plane CSC usage
        logging.info(self.getStepInfo() + "Verifying Plane CSC status for display %s" % self.display)
        csc_usage = color_verification.get_plane_csc_usage(self.display, 'PLANE_CTL_1', 'PLANE_COLOR_CTL_1',
                                                           'PIPE_BOTTOM_COLOR')
        if not csc_usage:
            gdhm.report_bug(
                title="[Color][YCbCrMultiAdapter]Verification of plane output color space failed",
                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                priority=gdhm.Priority.P2,
                exposure=gdhm.Exposure.E2
            )
            self.fail("Failed to get plane csc usage")

    def runTest(self):
        config = display_config.display_config.DisplayConfiguration()
        for gfx_index, value in self.display_details.items():
            logging.info(self.getStepInfo() + "Checking for YCbCr support in connected panels: {0}: {1} ".format(
                          self.display_details[gfx_index], self.display_details[value]))
            self.target_id = config.get_target_id(self.display_details[value], self.enumerated_displays)
            ##
            # Check if YCbCr is supported
            ycbcr_supported = driver_escape.is_ycbcr_supported(self.target_id)

            if ycbcr_supported:
                self.display = self.display_details[value]
                logging.info("YCbCr is supported on panel %s" % self.display)
                topology = enum.SINGLE
                if config.set_display_configuration_ex(topology, [self.display]) is True:
                    logging.info(self.getStepInfo() + "Applied the configuration as {0} {1}".format(
                        display_config_enums.DisplayConfigTopology(topology).name,
                        self.get_display_configuration([self.display])))
                    ##
                    # Enables YCbCr
                    logging.info(self.getStepInfo() + "Enabling YCbCr")
                    self.ycbcr_enable_status = driver_escape.configure_ycbcr(self.target_id, True)
                    if not self.ycbcr_enable_status:
                        gdhm.report_bug(
                            title="[Color][YCbCrMultiAdapter]Escape call to enable YCbCr failed",
                            problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                            component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                            priority=gdhm.Priority.P2,
                            exposure=gdhm.Exposure.E2
                        )
                        self.fail("Failed to enable YCbCr")
                    else:
                        logging.info("Successfully enabled YCbCr")
                        ##
                        # Verify the registers
                        self.verify_registers()
                        ##
                        # Disables YCbCr
                        logging.info(self.getStepInfo() + "Disabling YCbCr")
                        disable_status = driver_escape.configure_ycbcr(self.target_id, False)
                        if not disable_status:
                            gdhm.report_bug(
                                title="[Color][YCbCrMultiAdapter]Escape call to disable YCbCr failed",
                                problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                                component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                                priority=gdhm.Priority.P2,
                                exposure=gdhm.Exposure.E2
                            )
                            self.fail("Failed to disable YCbCr")
                        else:
                            logging.info("Successfully disabled YCbCr")
            else:
                gdhm.report_bug(
                    title="[Color][YCbCrMultiAdapter]Test Failed due to yCbCr not supported on connected "
                          "panels:{0}{1}".format(self.display_details[gfx_index], self.display_details[value]),
                    problem_classification=gdhm.ProblemClassification.FUNCTIONALITY,
                    component=gdhm.Component.Test.DISPLAY_OS_FEATURES,
                    priority=gdhm.Priority.P2,
                    exposure=gdhm.Exposure.E2
                )
                self.fail("yCbCr not supported on connected panels")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    logging.info(
        "Test purpose: Enables YCbCr on supported panels and check for YUV output color space when YCbCr is enabled.")
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    test_environment.TestEnvironment.cleanup(outcome.result)
