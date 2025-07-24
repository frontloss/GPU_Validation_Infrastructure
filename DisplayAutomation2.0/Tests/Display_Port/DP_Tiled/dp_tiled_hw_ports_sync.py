#######################################################################################################################
# @file         dp_tiled_hw_ports_sync.py
# @brief        This test verifies hot plug / unplug
# @details      This test checks whether Hotplug/ Unplug works and applies max mode on tiled display.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledHWPortSync(DisplayPortBase):
    ##
    # @brief        This test plugs required displays, set config, applies max modes, verifies applied modes.
    # @return       None
    def runTest(self):

        ##
        # Setting 10 bpc in registry
        if "-BPC" in sys.argv:
            if self.ma_flag:
                for adapter in self.adapter_list_to_verify:
                    is_success = DSCHelper.set_bpc_in_registry(adapter, self.bpc)
                    self.assertTrue(is_success, "Setting Source BPC Failed for adapter {}".format(is_success))
            else:
                is_success = DSCHelper.set_bpc_in_registry('gfx_0', self.bpc)
                self.assertTrue(is_success, "Setting Source BPC Failed.")

            logging.info("Successfully set BPC to %s", self.bpc)

        ##
        # Plug the Tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids of plugged displays :%s" % plugged_target_ids)

        ##
        # set display configuration with topology as given in cmd line
        self.set_config(self.config, no_of_combinations=1)

        ##
        # Apply 5K3K/8k4k resolution and check for applied mode
        self.apply_tiled_max_modes()

        ##
        # Disabling BPC in the registry
        if "-BPC" in sys.argv:
            if self.ma_flag:
                for adapter in self.adapter_list_to_verify:
                    is_success = DSCHelper.enable_disable_bpc_registry(adapter, enable_bpc=0)
                    self.assertTrue(is_success, "Disabling BPC in registry failed for adapter {}.".format(adapter))
            else:
                is_success = DSCHelper.enable_disable_bpc_registry('gfx_0', enable_bpc=0)
                self.assertTrue(is_success, "Disabling BPC in registry failed.")

            logging.info("Successfully disabled BPC in the registry")


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
