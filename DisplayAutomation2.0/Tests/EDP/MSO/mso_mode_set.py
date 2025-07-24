########################################################################################################################
# @file         mso_mode_set.py
# @addtogroup   EDP
# @section      MSO _Tests
# @brief        This file contains tests to verify mso with modeset
# @details      @ref mso_mode_set.py <br>
#               Test for Mode Set scenario
#               This file implements MSO test for following scenarios
#               1. if panel supports multi RR -> RR switch
#               2. if panel supports single RR -> mode switch
#
# @author       Bhargav Adigarla
########################################################################################################################

from Libs.Core.test_env import test_environment
from Tests.EDP.MSO.mso_base import *


##
# @brief        This file contains tests to verify mso with modeset
class TestModeSet(MsoBase):
    ##
    # @brief        This test verifies mso with modeset
    # @return       None
    # @cond
    @common.configure_test(repeat=True)
    # @endcond
    def t_11_mode_set(self):
        status = True
        enumerated_displays = self.display_config_.get_enumerated_display_info()
        if enumerated_displays is None:
            self.fail("API get_enumerated_display_info() FAILED (Test Issue)")

        ##
        # Apply supported modes on all active edp
        mode_list = []

        for panel in self.mso_panels:
            rr_list = common.get_supported_refresh_rates(panel.target_id)

            if len(rr_list) > 1:
                for rr in rr_list:
                    mode_list.append(common.get_display_mode(panel.target_id, rr))
            else:
                mode_list = common.get_display_mode(panel.target_id, limit=2)

            for mode in mode_list:
                ##
                # Apply mode Set
                if self.display_config_.set_display_mode([mode], False) is False:
                    self.fail("\tFailed to apply display mode = {0} on {1}".format(mode, panel.port))

                current_mode = self.display_config_.get_current_mode(panel.target_id)
                logging.info(
                    "\tApplied mode on {0}=  {1}".format(panel.port, current_mode.to_string(enumerated_displays)))

                ##
                # Verify MSO
                logging.info("Step: Verifying MSO in {0} mode on {1}".format(
                    current_mode.to_string(enumerated_displays), panel.port))
                if mso.verify(panel) is True:
                    logging.info("\tPASS: MSO verification successful for {0}".format(panel.port))
                else:
                    self.fail("\tFAIL: MSO verification failed for {0}".format(panel.port))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(TestModeSet))
    test_environment.TestEnvironment.cleanup(test_result)
