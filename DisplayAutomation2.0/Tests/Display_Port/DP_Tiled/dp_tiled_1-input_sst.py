#######################################################################################################################
# @file         dp_tiled_1-input_sst.py
# @brief        This test applies non-tiled mode on tiled display
# @details      This test plugs only Master port. The maximum resolution that can be supported by the one
#    			tile should be enumerated and should get applied without any visual anomalies.
#
# @author       Amanpreet Kaur Khurana, Ami Golwala
#######################################################################################################################

from Libs.Core.test_env.test_environment import TestEnvironment
from Tests.Display_Port.DP_Tiled.display_port_base import *


##
# @brief        This class contains a test function which implements the mentioned test scenario / test steps.
class DPTiled1InputSST(DisplayPortBase):
    ##
    # @brief        This test method plugs the required displays, set display config
    #               and verifies not tiled mode on tiled display.
    # @return       None
    def runTest(self):
        ##
        # Plug only the Master Port of Tiled display
        self.plug_master_or_unplug_slave(action="MASTER_PORT_PLUG")
        ##
        # get the target ids of the plugged displays
        plugged_target_ids = self.display_target_ids()
        logging.info("Target ids :%s" % plugged_target_ids)
        ##
        # set display configuration with topology as given in cmd line
        self.set_config(self.config, no_of_combinations=1)
        ##
        # Apply 4k Non-Tiled resolution and Verify applied mode
        self.apply_and_verify_non_tiled_max_mode()


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
