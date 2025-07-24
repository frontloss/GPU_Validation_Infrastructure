##################################################################################################################
# @file         assr_lid_events.py
# @addtogroup   EDP_ASSR
# @section      Tests
# @brief        assr_lid_events.py contains ASSR tests for lid switching with
#               do_nothing, sleep, hibernate
#
# @author       Vinod D S, Rohit Kumar
##################################################################################################################

import time

from Libs.Core import display_power
from Libs.Core.hw_emu import she_utility
from Libs.Core.test_env import test_environment
from Tests.EDP.ASSR.assr_base import *


##
# @brief        This class contains ASSR tests with lid events
class AssrLidEvents(AssrBase):
    lid_switch_close_delay = 5
    lid_switch_open_delay = 30
    lid_resume_delay = 90
    she_utility_ = she_utility.SHE_UTILITY()

    ############################
    # Test Functions
    ############################

    ##
    # @brief        This test is specific to Post-Si requirements, it checks if SHE tool is connected or not
    # @return       None
    # @cond
    @common.configure_test(selective=["LID", "POST_SI"], critical=True)
    # @endcond
    def t_01_post_si_requirements(self):
        ##
        # Check whether SHE tool is connected
        result = self.she_utility_.intialize()
        self.assertNotEqual(result, 0, "SHE tool is NOT connected(Planning Issue)")

    ##
    # @brief        This test verifies ASSR with Do Nothing
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID"])
    # @endcond
    def t_11_p_assr_do_nothing(self):
        self.check_assr_lid(display_power.LidSwitchOption.DO_NOTHING)

    ##
    # @brief        This test verifies ASSR with Sleep
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID"])
    # @endcond
    def t_12_p_assr_sleep(self):
        self.check_assr_lid(display_power.LidSwitchOption.SLEEP)

    ##
    # @brief        This test verifies ASSR with Hibernate
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID"])
    # @endcond
    def t_13_p_assr_hibernate(self):
        self.check_assr_lid(display_power.LidSwitchOption.HIBERNATE)

    ##
    # @brief        This function verifies ASSR with Do Nothing
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID", "LEGACY", "BLOCKED"])
    # @endcond
    def t_21_n_assr_do_nothing(self):
        self.check_assr_lid(display_power.LidSwitchOption.DO_NOTHING, False)

    ##
    # @brief        This function verifies ASSR with Sleep
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID", "LEGACY", "BLOCKED"])
    # @endcond
    def t_22_n_assr_sleep(self):
        self.check_assr_lid(display_power.LidSwitchOption.SLEEP, False)

    ##
    # @brief        This function verifies ASSR with Hibernate
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["LID", "LEGACY", "BLOCKED"])
    # @endcond
    def t_23_n_assr_hibernate(self):
        self.check_assr_lid(display_power.LidSwitchOption.HIBERNATE, False)

    ############################
    # Helper Functions
    ############################

    ##
    # @brief        This is a helper function used to check/verify ASSR with specified lid event
    # @param[in]   lid_switch_state member of enum LidSwitchOption
    # @param[in]   enabled boolean, indicates expected Driver ASSR status
    # @return       None
    def check_assr_lid(self, lid_switch_state: display_power.LidSwitchOption, enabled=True):
        ##
        # Setting lid switch state
        result = self.display_power_.set_lid_switch_power_state(lid_switch_state)
        self.assertEquals(result, True, "Set lid switch state failed")
        gdhm.report_driver_bug_di(f"{GDHM_EDP_ASSR} Set lid switch state failed")
        logging.info(
            "Set lid switch power state is successful for %s", lid_switch_state.name)

        ##
        # Lid close and open
        result = self.she_utility_.lid_switch(lid_switch_state)
        self.assertEquals(result, True, "LidSwitchButtonPress failed")
        gdhm.report_driver_bug_di(f"{GDHM_EDP_ASSR} LidSwitchButtonPress failed")
        logging.info("Lid is closed for %s", lid_switch_state.name)

        ##
        # Wait till the system resumes
        time.sleep(self.lid_resume_delay)

        ##
        # Check ASSR
        test_status = True
        for edp_panel in self.edp_panels:
            if self.verify_assr(edp_panel, enabled) is False:
                test_status = False
        self.assertEquals(test_status, True, "ASSR verification failed")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(
        common.get_test_suite(AssrLidEvents, ['0', '1', '2', '3']))
    test_environment.TestEnvironment.cleanup(test_result)
