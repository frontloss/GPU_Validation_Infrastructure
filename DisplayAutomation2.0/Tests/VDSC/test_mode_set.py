########################################################################################################################
# @file         test_mode_set.py
# @brief        Test to check VDSC programming by switching RR or min and max mode supported by the VDSC display.
# @details      Test Scenario:
#               1. if panel supports multi RR -> RR switch or if panel supports single RR -> mode switch
#               2. Verify VDSC programming for the VDSC displays in current topology.
#               This test can be planned with EDP and DP VDSC displays
#
# @author       Bhargav Adigarla, Praburaj Krishnan
########################################################################################################################
import logging
import unittest

from Libs.Core.test_env import test_environment
from Libs.Feature.vdsc import dsc_verifier
from Tests.PowerCons.Modules import common
from Tests.VDSC.vdsc_base import VdscBase


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class TestModeSet(VdscBase):

    ##
    # @brief        This test method applies min and max mode or applies mode with different RR and verifies VDSC
    #               programming for each of the mode applied.
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_mode_set(self) -> None:
        status = True
        enumerated_displays = VdscBase._display_config.get_enumerated_display_info()
        if enumerated_displays is None:
            self.fail("API get_enumerated_display_info() FAILED (Test Issue)")

        # Apply supported modes on all active VDSC panels
        mode_list = []

        for adapter_display_dict in VdscBase.vdsc_panels:
            # Each dictionary inside vdsc_panel list will be of length 1, hence iterating dictionary is not needed
            [(gfx_index, panel)] = adapter_display_dict.items()
            rr_list = common.get_supported_refresh_rates(VdscBase.target_ids[panel])

            if len(rr_list) > 1:
                for rr in rr_list:
                    mode_list.append(common.get_display_mode(VdscBase.target_ids[panel], rr))
            else:
                mode_list = common.get_display_mode(VdscBase.target_ids[panel], limit=2)

            for mode in mode_list:
                ##
                # Apply mode Set
                if VdscBase._display_config.set_display_mode([mode], False) is False:
                    logging.error("\tFAILED to apply display mode = {0} on {1}".format(mode, panel))
                    status = False
                    continue

                current_mode = VdscBase._display_config.get_current_mode(VdscBase.target_ids[panel])
                logging.info(
                    "\tApplied mode on {0}=  {1}".format(panel, current_mode.to_string(enumerated_displays)))

                # Verify VDSC
                logging.info("Step: Verifying VDSC in {0} mode on {1}".format(
                    current_mode.to_string(enumerated_displays), panel))

                is_success = dsc_verifier.verify_dsc_programming(gfx_index, panel)
                self.assertTrue(is_success, "VDSC verification at {} on {} Expected = PASS Actual = FAIL".format(
                    panel, gfx_index))

                logging.info("VDSC verification at {} on {} Expected = PASS Actual = PASS".format(panel, gfx_index))

        if status is False:
            self.fail("VDSC verification FAILED")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestModeSet))
    test_environment.TestEnvironment.cleanup(test_result)
