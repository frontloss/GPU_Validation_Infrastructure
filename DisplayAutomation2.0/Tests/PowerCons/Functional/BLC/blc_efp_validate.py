########################################################################################################################
# @file         blc_efp_validate.py
# @brief        Tests for BLC Basic
#
# @author       Tulika
########################################################################################################################
from Libs.Core.test_env import test_environment

from Tests.PowerCons.Functional.BLC.blc_base import *
from Tests.PowerCons.Functional.BLC.blc_efp_base import BlcEfpBase


##
# @brief        This class contains EFP Blc tests
class BlcEfpBasic(BlcEfpBase):
    ##
    # @brief        Test function is to verify EFP blc with S3 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['S3'])
    # @endcond
    def t_11_blc_efp_power_event_s3(self):
        self.verify_efp_blc(blc.Scenario.POWER_EVENT_S3)

    ##
    # @brief        Test function is to verify EFP blc with CS power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['CS'])
    # @endcond
    def t_12_blc_efp_power_event_cs(self):
        self.verify_efp_blc(blc.Scenario.POWER_EVENT_CS)

    ##
    # @brief        Test function is to verify EFP blc with S4 power event
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['S4'])
    # @endcond
    def t_13_blc_efp_power_event_s4(self):
        self.verify_efp_blc(blc.Scenario.POWER_EVENT_S4)

    ##
    # @brief        Test function is to verify EFP blc with Display TDR
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['DISPLAY_TDR'])
    # @endcond
    def t_14_blc_efp_display_tdr(self):
        self.verify_efp_blc(blc.Scenario.DISPLAY_TDR)

    ##
    # @brief        Test function is to verify EFP blc with Monitor Time Out
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['MONITOR_TIME_OUT'])
    # @endcond
    def t_15_blc_efp_monitor_timeout(self):
        self.verify_efp_blc(blc.Scenario.MONITOR_TIME_OUT)

    ##
    # @brief        Test function is to verify EFP blc with Display Config
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=['DISPLAY_CONFIG'])
    # @endcond
    def t_16_blc_efp_display_config(self):
        self.verify_efp_blc(blc.Scenario.DISPLAY_CONFIG)


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BlcEfpBasic))
    test_environment.TestEnvironment.cleanup(test_result)
