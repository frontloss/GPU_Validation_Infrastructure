#################################################################################################
# @file         elp_persistence_with_reboot.py
# @brief        This scripts enables HDR and performs verification on all the pipes
#               The script then performs a system reboot. After the system successfully reboots,
#               HDR persistence is verified by performing ETL and register level verification
#               Verification Details:
#               The test script verifies the DisplayCaps from the ETL for HDR support in the EDID.
#               Post enabling HDR, the status_code returned from the OS API is decoded and verified.
#               Pipe_Misc register is also verified for HDR_Mode
#               Plane and Pipe Verification is performed by iterating through each of the displays
#               Metadata verification, by comparing the Default and Flip Metadata is performed,
#               along with register verification
# Sample CommandLines:  python elp_persistence_with_reboot.py -edp_a SINK_EDP50 -scenario POWER_EVENT_S5
# @author       Smitha B
#################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Color.Features.ELP.elp_test_base import *
from Libs.Core import reboot_helper


##
# @brief - To perform persistence verification for Quantisation reboot scenario
class elpPersistenceWithReboot(ELPTestBase):

    ##
    # @brief Unittest test_before_reboot function - To enable and verify before reboot scenario
    # @param[in] self
    # @return None
    def test_before_reboot(self):
        ##
        # Enable Optimization level on all the supported panels and perform verification
        logging.info("*** Step 1 : Enable the optimization on all supported panels and verify ***")
        if self.enable_elp_optimization_and_verify(self.user_opt_level) is False:
            self.fail()

        if reboot_helper.reboot(self, 'test_after_reboot') is False:
            self.fail("Failed to reboot the system")

    ##
    # @brief Unittest test_after_reboot function - To perform register verification after reboot scenario
    # @param[in] self
    # @return None
    def test_after_reboot(self):
        logging.info("*** Step 2 : Resume from PowerEvent S5 and verify ***")
        logging.info("Successfully resumed from PowerEvent S5 state")
        color_properties.update_feature_caps_in_context(self.context_args)
        for gfx_index, adapter in self.context_args.adapters.items():
            for port, panel in adapter.panels.items():
                if panel.is_active and panel.is_lfp and panel.FeatureCaps.ELPSupport is True:
                    if perform_elp_verification(gfx_index, panel, port, self.user_opt_level) is False:
                        self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    logging.info("Test purpose: Enable HDR and perform verification on all panels")
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('elpPersistenceWithReboot'))
    TestEnvironment.cleanup(outcome)
