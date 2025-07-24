########################################################################################################################
# @file         mso_power_event.py
# @addtogroup   EDP
# @section      MSO_Tests
# @brief        This file contains MSO tests for power events CS, S3, S4, Hibernate
#
# @author       Bhargav Adigarla
########################################################################################################################

import time

from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Tests.EDP.MSO.mso_base import *


##
# @brief        This class contains MSO tests for power events CS, S3, S4, Hibernate
class VdscPowerEvent(MsoBase):

    ##
    # @brief        This function verifies MSO with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "CS"])
    # @endcond
    def t_10_power_event_cs(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS):
            self.verify_mso_with_power_event(display_power.PowerEvent.CS)
        else:
            gdhm.report_driver_bug_di(f"{mso.GDHM_MSO_COG} Test needs CS enabled system (planning issue)")
            self.fail("CS is not supported in this platform, aborting the test(Planning Issue)")

    ##
    # @brief        This function verifies MSO with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "S3"])
    # @endcond
    def t_11_power_event_s3(self):
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.verify_mso_with_power_event(display_power.PowerEvent.S3)
        else:
            gdhm.report_driver_bug_di(f"{mso.GDHM_MSO_COG} Test needs CS disabled system (planning issue)")
            self.fail("S3 can not be tested since CS is supported, aborting the test(Planning Issue)")

    ##
    # @brief        This function verifies MSO with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["POST_SI", "S4"])
    # @endcond
    def t_12_power_event_s4(self):
        self.verify_mso_with_power_event(display_power.PowerEvent.S4)

    ##
    # @brief        This is a helper function to verify MSO with given power event
    # @param[in]    power_event member of enum PowerEvent
    # @return       None
    def verify_mso_with_power_event(self, power_event):
        if self.display_power_.invoke_power_event(power_event, common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail("Failed to trigger power event {0}".
                      format(power_event.name))
        time.sleep(20)  # 20 seconds delay to verify mso after power event.
        for panel in self.mso_panels:
            if mso.verify(panel) is True:
                logging.info("\tPASS: MSO verification successful for {0}".format(panel.port))
            else:
                self.fail("\tFAIL: MSO verification failed for {0}".format(panel.port))


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VdscPowerEvent))
    test_environment.TestEnvironment.cleanup(test_result)
