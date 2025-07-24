########################################################################################################################
# @file         cmtg_power_events.py
# @brief        Contains basic functional tests covering below scenarios:
#               * CMTG verification with CS/S3/S4.
# @author       Bhargav Adigarla
########################################################################################################################

from Libs.Core import display_power, enum
from Libs.Core.test_env import test_environment
from Tests.PowerCons.Functional.CMTG.cmtg_base import *

##
# @brief        Contains CMTG power events tests
class CmtgPowerEvents(CmtgBase):

    ##
    # @brief        This function verifies CMTG with CS resume
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["CS"])
    # @endcond
    def t_10_cmtg_cs(self):
        logging.info("CMTG verification before CS power event")
        self.verify_cmtg()
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is False:
            self.fail("CS is NOT supported on the system(Planning Issue)")
        if self.display_power_.invoke_power_event(display_power.PowerEvent.CS,
                                                  common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event CS')
        logging.info("CMTG verification after CS power event")
        self.verify_cmtg()

    ##
    # @brief        This function verifies CMTG with S3 resume
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S3"])
    # @endcond
    def t_11_cmtg_s3(self):
        logging.info("CMTG verification before S3 power event")
        self.verify_cmtg()
        if self.display_power_.is_power_state_supported(display_power.PowerEvent.CS) is True:
            self.fail("S3 is NOT supported on the system(Planning Issue)")
        if self.display_power_.invoke_power_event(display_power.PowerEvent.S3,
                                                  common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event S3')
        logging.info("CMTG verification after S3 power event")
        self.verify_cmtg()

    ##
    # @brief        This function verifies CMTG with S4 resume
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["S4"])
    # @endcond
    def t_12_cmtg_s4(self):
        logging.info("CMTG verification before S4 power event")
        self.verify_cmtg()
        if self.display_power_.invoke_power_event(display_power.PowerEvent.S4,
                                                  common.POWER_EVENT_DURATION_DEFAULT) is False:
            self.fail('Failed to invoke power event S4')
        logging.info("CMTG verification after S4 power event")
        self.verify_cmtg()


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(CmtgPowerEvents))
    test_environment.TestEnvironment.cleanup(test_result)
