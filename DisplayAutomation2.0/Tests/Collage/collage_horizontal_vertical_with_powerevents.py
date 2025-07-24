########################################################################################################################
# @file         collage_horizontal_vertical_with_powerevents.py
# @brief        Verify the collage feature during power events
#
# @author       Praveen Bademi
########################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core import display_power, enum
from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.display_collage_base import DisplayCollageBase, DELAY_5000_MILLISECONDS, DELAY_1000_MILLISECONDS
from Tests.Collage.display_collage_base import RESUME_TIME



##
# @brief        This class contains runTest function to verify collage persistence during power events
class CollagePowerEvents(DisplayCollageBase):

    ##
    # @brief        verify if collage is enabled during power events
    # @param[in]    power_state: Enum
    #                   Power State to be invoked
    # @return       None
    def verify_collage_status(self, power_state: display_power.PowerEvent) -> None:

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # set DUT to Low Power State
        self.power_event(power_state, RESUME_TIME)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # verify if collage is enabled
        self.is_collage_enabled()

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self):

        dp_port_list = self.get_dp_ports_to_plug()

        if (self.get_number_of_free_dp_ports() >= self.get_number_of_ports()) is False:
            logging.error("Not Enough free ports available.. Exiting....")
            self.fail()

        for index, port_type in enumerate(dp_port_list):

            # Get Topology Type(MST/SST) from the command line
            topology_type = self.get_topology_type(index)

            if topology_type == 'MST' or topology_type == 'SST':
                # Get Topology XML file from command line
                xml_file = self.get_xmlfile(index)

                # Function call to set DP1.2 topology
                self.setnverifydp(port_type, topology_type, xml_file)

        # Function call to get the collage information
        self.get_collage_info()

        # Function call to get the supported configuration
        supported_config = self.get_supported_config()

        # Function call to apply collage mode
        self.apply_collage_mode(supported_config)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        self.verify_collage_status(display_power.PowerEvent.S4)

        # TODO: Currently whenever S5(reboot) is invoked, the GTA machine gets unresponsive.
        # self.verify_collage_status(PowerEventState.POWER_STATE_S5)

        # Verifying whether system supports CS (ConnectedStandby).If yes,then we will validate CS entry/exit.
        # If not, then we will validate S3 entry/exit.
        if self.display_power.is_power_state_supported(display_power.PowerEvent.CS):
            self.verify_collage_status(display_power.PowerEvent.CS)
        else:
            self.verify_collage_status(display_power.PowerEvent.S3)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
