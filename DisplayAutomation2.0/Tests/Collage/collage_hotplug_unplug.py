########################################################################################################################
# @file         collage_hotplug_unplug.py
# @brief        Verify switching between collage and non collage mode upon hot plug and hot unplug of collage displays
#
# @author       Praveen Bademi
########################################################################################################################

import logging
import sys
import time
import unittest

from Libs.Core.test_env.test_environment import TestEnvironment

from Tests.Collage.display_collage_base import DisplayCollageBase, DELAY_5000_MILLISECONDS, DELAY_1000_MILLISECONDS


##
# @brief        This class contains runTest function to Verify switching between collage and non collage mode upon hot
#               plug and hot unplug of collage
class CollageHotPlugUnplug(DisplayCollageBase):

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self) -> None:

        dp_port_list = self.get_dp_ports_to_plug()

        if (self.get_number_of_free_dp_ports() >= self.get_number_of_ports()) is False:
            logging.error("Not Enough free ports available.. Exiting....")
            self.fail()

        port_type = ''

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

        # Function call to Unplug a DP Display
        self.set_hpd(port_type, False)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to check if Collage is disabled
        self.is_collage_disabled()

        # Function call to Unplug a DP Display
        self.set_hpd(port_type, True)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to get the supported configuration
        supported_config = self.get_supported_config()

        # Function call to apply collage mode
        self.apply_collage_mode(supported_config)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
