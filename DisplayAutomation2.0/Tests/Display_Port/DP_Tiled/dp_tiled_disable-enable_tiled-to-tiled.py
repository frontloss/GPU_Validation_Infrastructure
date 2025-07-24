#######################################################################################################################
# @file         dp_tiled_disable-enable_tiled-to-tiled.py
# @brief        This test verifies tiled modes with driver restart.
# @details      Verifies tiled mode able to apply after reset (disable followed with enable) of Graphics driver.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################
from Libs.Core import display_essential
from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledDisableEnableGfxDriver(DisplayPortBase):

    ##
    # @brief        This test method plugs the required displays, set display config, applies tiled max modes,
    #               restarts driver and verifies applied max modes.
    # @return       None
    def runTest(self):
        if not reboot_helper.is_reboot_scenario():
            ##
            # Plug the Tiled display
            self.tiled_display_helper(action="PLUG")
            ##
            # get the target ids of the plugged displays
            plugged_target_ids = self.display_target_ids()
            logging.info("Target ids :%s" % plugged_target_ids)
            ##
            # set display configuration with topology as SINGLE
            self.set_config(self.config, no_of_combinations=1)
            ##
            # Apply 5K3K/8k4k resolution and check for applied mode
            self.apply_tiled_max_modes()

            ##
            # disable and enable gfx driver
            status, reboot_required = display_essential.restart_gfx_driver()
            if status:
                logging.info("Successfully restarted driver.")
            elif status is False and reboot_required is True:
                logging.info("\tRebooting system as requested by OS.")
                if reboot_helper.reboot(self, 'runTest') is False:
                    self.fail("Failed to reboot the system")
            else:
                self.fail("Failed to restart display driver")

        ##
        # check current mode
        flag = self.verify_tiled_mode()
        if flag:
            logging.info("Current mode is same as before Graphics disable/enable")
        else:
            logging.error("Current mode is not same as before Graphics disable/enable. Exiting .....")
            ##
            # gdhm bug reported in verify_tiled_mode
            self.fail()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.TextTestRunner(verbosity=2).run(reboot_helper.get_test_suite('DPTiledDisableEnableGfxDriver'))
    TestEnvironment.cleanup(outcome)
