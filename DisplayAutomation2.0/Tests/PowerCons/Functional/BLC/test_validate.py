########################################################################################################################
# @file         test_validate.py
# @brief        Tests for BLC and CABC
#
# @author       Simran Setia
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.test_base import *

##
# @brief        This class contains BLC and CABC tests
class BlcCabcBasic(TestBase):
    ##
    # @brief        Test function is to verify BLC and CABC with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['S3'])
    # @endcond
    def t_11_test_power_event_s3(self):
        self.verify_blc_and_cabc(blc.Scenario.POWER_EVENT_S3)

    ##
    # @brief        Test function is to verify BLC and CABC with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['CS'])
    # @endcond
    def t_12_test_power_event_cs(self):
        self.verify_blc_and_cabc(blc.Scenario.POWER_EVENT_CS)

    ##
    # @brief        Test function is to verify BLC and CABC with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['S4'])
    # @endcond
    def t_13_test_power_event_s4(self):
        self.verify_blc_and_cabc(blc.Scenario.POWER_EVENT_S4)

    ##
    # @brief        Test function is to verify BLC and CABC with AC-DC switch
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['AC_DC_SWITCH'])
    # @endcond
    def t_14_test_ac_dc_switch(self):
        self.verify_blc_and_cabc(blc.Scenario.AC_DC_SWITCH)

    ##
    # @brief        Test function is to verify BLC and CABC with SDR-HDR toggle
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['TOGGLE_SDR_HDR'])
    # @endcond
    def t_15_test_toggle_sdr_hdr(self):
        self.verify_blc_and_cabc(blc.Scenario.TOGGLE_SDR_HDR)

    ##
    # @brief        Test function is to verify BLC and CABC with Display Config
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['DISPLAY_CONFIG'])
    # @endcond
    def t_16_test_display_config(self):
        self.verify_blc_and_cabc(blc.Scenario.DISPLAY_CONFIG)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BlcCabcBasic))
    test_environment.TestEnvironment.cleanup(test_result)
