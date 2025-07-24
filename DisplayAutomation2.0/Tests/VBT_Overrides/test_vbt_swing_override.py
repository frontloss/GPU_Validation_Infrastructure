######################################################################################
# @file         test_vbt_swing_override.py
# @brief        Validate Vswing Override in VBT for any display port
# @details      Displays are external displays dp_b, dp_c, hdmi_b, hdmi_c, etc
# @author       Kumar V, Arun
######################################################################################

from Libs.Core import enum
from Libs.Core.test_env import test_environment
from Libs.Feature.display_engine.de_base import display_phy_buffer
from Tests.VBT_Overrides.vbt_override_base import *



##
# @brief        TestVbtSwingOverride base class : To be used in VBT Override tests
class TestVbtSwingOverride(VbtOverrideBase):


    ##
    # @brief        test_vbt_swing_override function.
    #               Entry point to the test, calls functions that verify all the steps in the verification
    # @return       None
    def test_vbt_swing_override(self):
        logging.debug("Entry: test_vbt_swing_override()")
        for display_port in self.input_display_list:
            # Ignore HPD request for Internal Displays
            if display_utility.get_vbt_panel_type(display_port, 'gfx_0') in \
                    [display_utility.VbtPanelType.LFP_DP, display_utility.VbtPanelType.LFP_MIPI]:
                logging.debug("Skipping : Internal Display {} is not Pluggable Display".format(display_port))
                continue

            logging.info("Pre-Step : Get EFP support and index in VBT Block2 for {}".format(display_port))
            status, index = self.get_port_status_vbt(display_port)
            if status is True:
                logging.info("STEP 1 : Enable Vswing override table in VBT for EFP Panel Index {}".format(index))
                self.assertTrue(self.vbt_enable_vswing_override(index), "Step1 Failed")

                logging.info("STEP 2 : Plug Display on {}".format(display_port))
                self.assertTrue(display_utility.plug_display(display_port, self.cmd_line_param), "Step2 Failed")

                logging.info("STEP 3 : Set single display configuration on {}".format(display_port))
                self.assertTrue(self.config.set_display_configuration_ex(enum.SINGLE, [display_port]), "Step3 Failed")

                logging.info("STEP 4 : Verify Phy Buffer Values on {}".format(display_port))
                self.assertTrue(self.vbt_override_verify_phy_buffer(display_port), "Step4 Failed")

            else:
                self.assertTrue(status, "Pre-Step Failed")

        logging.debug("Exit: test_vbt_swing_override()")

    ##
    # @brief        This method verifies mmio programming against vbt values
    # @param[in]    display_port - Name of display port (ex: DP_A, MIPI_A, etc).
    # @return       bool - True if request is success else False.
    def vbt_override_verify_phy_buffer(self, display_port):
        phy_list = [display_phy_buffer.DisplayPhyBuffer(display_port)]
        return display_phy_buffer.VerifyPhyBufferProgramming(phy_list, vbt_override=True, gfx_vbt=self.gfx_vbt)

    ##
    # @brief teardown to reset vbt values
    # @return None
    def tearDown(self):

        # call base class teardown
        super(TestVbtSwingOverride, self).tearDown()

        # Clear/ Reset VBT - Reset VBT Call has some issue and does not reset properly, so ensuring test does it
        self.assertTrue(self.vbt_disable_vswing_override(), "Reset Vbt failed")

        logging.info('Reset VBT passed')
        logging.info("Test Completed")
        logging.debug("EXIT: TearDown")


if __name__ == '__main__':
    test_environment.TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('TestVbtSwingOverride'))
    test_environment.TestEnvironment.cleanup(outcome)
