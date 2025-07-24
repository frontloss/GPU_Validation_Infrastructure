########################################################################################################################
# @file         vrr_vbt.py
# @section      Tests
# @brief        Contains vbt check for VRR
#
# @author       Rohit Kumar
########################################################################################################################
from Libs.Core.test_env.test_environment import TestEnvironment
from Libs.Core.vbt import vbt
from Tests.VRR.vrr_base import *


##
# @brief        This class contains VRR VBT tests. This class inherits the VrrBase class.
#               This class contains methods to check if VRR is working as expected with VBT
class VrrVbtTest(VrrBase):

    ##
    # @brief        This class method is the entry point for any VRR VBT test cases. Helps to initialize some of
    #               the parameters required for VRR test execution with VBT.
    # @return       None
    @classmethod
    def setUpClass(cls):
        super(VrrVbtTest, cls).setUpClass()

        for gfx_index, adapter in dut.adapters.items():
            if adapter.is_vrr_supported is False:
                continue

            gfx_vbt = vbt.Vbt(gfx_index)
            if gfx_vbt.version < 233:
                raise Exception("VRR VBT test is only supported on VBT 233 onwards")

    ##
    # @brief        Test function to check if VRR is working as expected with VBT
    # @return       None
    # @cond
    @common.configure_test(repeat=True, selective=["FULL_SCREEN", "LOW_HIGH_FPS"])
    # @endcond
    def t_41_vbt_enabled(self):
        # Verify VRR in default VBT settings
        if self.verify_vrr(True) is False:
            self.fail(f"VRR is not working with default VBT settings")
        logging.info("\tPASS: VRR verification passed successfully")

        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue

            # Disable VRR for eDP A
            if vrr.update_vbt(adapter, 'DP_A', False) is False:
                self.fail("Failed to set VRR settings in VBT")

            dut.refresh_panel_caps(adapter)

            for panel in adapter.panels.values():
                if panel.is_lfp and panel.port == 'DP_A':
                    # Verify that VRR is not getting enabled
                    if self.verify_vrr(True, negative=True, expected_vrr=False) is False:
                        self.fail(f"VRR is working with VBT VRR field disabled")
                    logging.info("\tPASS: VRR verification passed successfully")
                else:
                    # Verify VRR is working for other panels
                    if self.verify_vrr(True) is False:
                        self.fail(f"VRR is not working for {panel.port} after disabling VBT for DP_A")
                    logging.info("\tPASS: VRR verification passed successfully")

    ##
    # @brief        This method is the exit point for all VRR VBT test cases. This enables back VRR in VBT
    # @return       None
    @classmethod
    def tearDownClass(cls):
        status = True
        for adapter in dut.adapters.values():
            if adapter.is_vrr_supported is False:
                continue
            if vrr.update_vbt(adapter, 'DP_A', True) is False:
                logging.error("Failed to set VRR settings in VBT")
                status &= False
        assert status, "Failed to set VRR settings in VBT"
        super(VrrVbtTest, cls).tearDownClass()


if __name__ == '__main__':
    TestEnvironment.initialize()
    runner = unittest.runner.TextTestRunner(resultclass=common.get_test_result_class)
    test_result = runner.run(common.get_test_suite(VrrVbtTest))
    TestEnvironment.cleanup(test_result)
