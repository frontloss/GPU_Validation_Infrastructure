#######################################################################################################################
# @file         dp_tiled_hotplugunplug_tiled_to_nontiled.py
# @brief        This test verifies hot plug / unplug
# @details      This test checks whether Hotplug/ Unplug works on all ports
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiledtoNonTiledHotplugUnplugDuringPM(DisplayPortBase):
    ##
    # @brief        This test plugs required displays, set config, applies max modes, verifies applied modes,
    #               unplugs slave port, applies non tiled mode.
    # @return       None
    def runTest(self):
        ##
        # plug tiled display
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set display configuration with topology as SINGLE for Single Adapter case else EXTENDED
        if not self.ma_flag:
            self.set_config('SINGLE', no_of_combinations=1)
        else:
            self.set_config('EXTENDED', no_of_combinations=1)
        ##
        # Apply 5K3K/8k4k resolution and check for applied mode
        self.apply_tiled_max_modes()
        ##
        # Verify 5K3K/8k4k mode
        self.verify_tiled_mode()
        ##
        # Unplugging slave port of Tiled Display 
        self.plug_master_or_unplug_slave(action="SLAVE_PORT_UNPLUG")
        ##
        # apply and verify whether non tiled 4k mode is applied or not
        self.apply_and_verify_non_tiled_max_mode()
        ##
        # Plugging master port of Tiled Display to the system
        self.tiled_display_helper(action="UNPLUG")
        time.sleep(Delay_5_Secs)
        ##
        # Plugging DP Display to the system after resuming from sleep
        self.tiled_display_helper(action="PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # Apply 5K3K/8k4k resolution and check for applied resolution
        self.apply_tiled_max_modes()
        ##
        # Verify 5K3K/8k4k mode
        self.verify_tiled_mode()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
