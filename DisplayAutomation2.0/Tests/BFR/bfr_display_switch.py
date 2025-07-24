########################################################################################################################
# @file         bfr_display_switch.py
# @brief        Contains basic functional tests for BFR in different display configs
# @details      Basic functional tests are covering below scenarios:
#               * BFR verification in MAXIMIZED mode in different display configurations
#               * All tests will be executed on VRR panel with VRR enabled. BFR is expected to be working in all above
#               scenarios.
#
# @author       Gopikrishnan R
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.BFR.bfr_base import *
from Libs.Core import display_essential, enum
import time


##
# @brief        This class contains basic functional tests for BFR in different display configs
#               This class inherits the BfrBase class.
class BfrDisplaySwitch(BfrBase):

    ############################
    # Test Function
    ############################

    ##
    # @brief        BFR verification in MAXIMISED mode
    # @param[in]    power_event        : indicates the power event to go before running bfr workload
    # @return       None
    @common.configure_test(repeat=True, selective=["DISPLAY_SWITCH"], critical=False)
    # @endcond
    def t_11_display_switch(self):
        display_list = []
        lfp_ports = []
        primary_display = []
        secondary_display_list = []
        flag = True

        ##
        # Get display details
        for adapter in dut.adapters.values():
            for panel in adapter.panels.values():
                display_list.append(panel.display_info.DisplayAndAdapterInfo)
                if panel.is_lfp:
                    lfp_ports.append(panel.port)
                    primary_display = panel.display_info.DisplayAndAdapterInfo
                else:
                    secondary_display_list.append(panel.display_info.DisplayAndAdapterInfo)

        toplogy_dict = {"primary_single": enum.SINGLE, "clone": enum.CLONE, "extended": enum.EXTENDED,
                        "secondary_single": enum.SINGLE}

        comb_list = ["primary_single", "clone", "extended", "secondary_single", "primary_single"]
        result_list = []
        #comb_list = ["secondary_single"]

        negative = False
        for comb in comb_list:
            html.step_start(f"Running BFR for {comb}")
            if comb == "secondary_single":
                display_test_list = secondary_display_list[:1]
            elif comb == "primary_single":
                display_test_list = [primary_display]
            else:
                display_test_list = [primary_display] + secondary_display_list

            # @todo Keeping clone mode as negative as there is a known issue with modeset.
            if comb in ["clone", "secondary_single"]:
                negative = True
            else:
                negative = False

            if self.display_config_.set_display_configuration_ex(
                    toplogy_dict[comb], display_test_list):
                logging.info(f"Successfully applied display configuration {comb}")
                # Wait for 10 seconds after display switch
                time.sleep(10)
            else:
                self.fail("Failed to display configuration")

            if self.bfr_basic(negative=negative, target_ids=[display_test_list[0].TargetID]) is False:
                logging.error(f"FAIL : Basic Test : BFR verification failed for {comb}")
                result_list.append((comb, False))
                flag = False
            else:
                logging.info(f"\tPASS: BASIC Test : BFR verification for {comb} passed successfully")
                result_list.append((comb, True))

        if not flag:
            for comb, result in result_list:
                logging.error(f"FAIL : Basic Test : BFR verification failed for {comb}")
            self.fail("FAIL: BFR Verification failed")


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(BfrDisplaySwitch))
    TestEnvironment.cleanup(test_result)
