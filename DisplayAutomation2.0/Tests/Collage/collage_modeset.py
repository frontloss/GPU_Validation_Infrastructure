########################################################################################################################
# @file         collage_modeset.py
# @brief        Set the different modes for collage displays.
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
# @brief        This class contains runTest function to Set the different modes for collage displays.
class CollageModeSet(DisplayCollageBase):

    ##
    # @brief        runTest() executes the actual test steps.
    # @return       None
    def runTest(self) -> None:

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

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to get the supported configuration
        supported_config = self.get_supported_config()

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)

        # Function call to apply collage mode with mode set
        # second parameter is the flag for mode set
        self.apply_collage_mode(supported_config, True)

        # Wait for the simulation driver to reflect the MST connection status in CUI
        time.sleep(DELAY_5000_MILLISECONDS / DELAY_1000_MILLISECONDS)


if __name__ == '__main__':
    TestEnvironment.initialize()
    outcome = unittest.main(exit=False, argv=[sys.argv[0]])
    TestEnvironment.cleanup(outcome.result)
